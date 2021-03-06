from sqlalchemy import orm
import datetime
from sqlalchemy import schema, types
import classes as cls

metadata = schema.MetaData()


def now():
    return datetime.datetime.now()

"""
Tables - schema definition:
"""

"""
User - schema definition:
"""
user_table = schema.Table('user', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('user_seq_id', optional=True), primary_key=True),

    schema.Column('name', types.Unicode(255)),
    schema.Column('real_name', types.Unicode(255)),
    schema.Column('url', types.Unicode(255)),
)

"""
Bid - schema definition:
"""
bid_table = schema.Table('bid', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('bid_seq_id', optional=True), primary_key=True),
    schema.Column('owner', types.Integer,
        schema.ForeignKey('user.id')),   
    schema.Column('contribution_id', types.Integer,
        schema.ForeignKey('contribution.id')),
    schema.Column('tokens', types.Float),
    schema.Column('stake', types.Float),
    schema.Column('reputation',  types.Float),
    schema.Column('current_rep_to_return', types.Float),
    schema.Column('contribution_value_after_bid',  types.Float),
    schema.Column('time_created', types.DateTime(), default=now),

)


"""
Contribution - schema definition:
"""
contribution_table = schema.Table('contribution', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('contribution_seq_id', optional=True), primary_key=True),
    schema.Column('owner', types.Integer,
        schema.ForeignKey('user.id')),
    schema.Column('users_organizations_id', types.Integer,
        schema.ForeignKey('users_organizations.id')),
    schema.Column('min_reputation_to_close',  types.Integer,nullable=True),
    schema.Column('time_created', types.DateTime(), default=now),
    schema.Column('file', types.Text()),
    schema.Column('title', types.Text()),
    schema.Column('status', types.String(100),default='Open'),
)

"""
Contribution Contributers List - schema definition:
"""
contribution_contributer_table = schema.Table('contribution_contributer', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('contribution_contributer_seq_id', optional=True), primary_key=True),
    schema.Column('contribution_id', types.Integer,
        schema.ForeignKey('contribution.id')),
    schema.Column('contributer_id', types.Integer,
        schema.ForeignKey('user.id')),
    schema.Column('contributer_percentage', types.INTEGER),   
)

"""
Organization - schema definition:
"""
organization_table = schema.Table('organization', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('organization_seq_id', optional=True), primary_key=True),

    schema.Column('token_name', types.Unicode(255),nullable=False),
    schema.Column('slack_teamid', types.Unicode(255)),
    schema.Column('name', types.Unicode(255),nullable=False),
    schema.Column('code', types.Unicode(255),nullable=False),
)

"""
User Organizations - schema definition:
"""
users_organizations_table = schema.Table('users_organizations', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('users_organizations_seq_id', optional=True), primary_key=True),
    schema.Column('user_id', types.Integer,
        schema.ForeignKey('user.id')),
    schema.Column('organization_id', types.Integer,
        schema.ForeignKey('organization.id')),
    schema.Column('org_tokens', types.Float),
    schema.Column('org_reputation',  types.Float),   
)


"""
Relationships - definitions
"""
orm.mapper(cls.User, user_table, properties={
    'userOrganizations':orm.relation(cls.UserOrganization, backref='user'),
})

orm.mapper(cls.UserOrganization, users_organizations_table, properties={
          'contributions':orm.relation(cls.Contribution),                                                              
                                                                        })

orm.mapper(cls.Contribution, contribution_table, properties={
    'contribution_owner':orm.relation(cls.User, backref='contribution'),
    'bids':orm.relation(cls.Bid, backref='contribution'),  
    'contributionContributers':orm.relation(cls.ContributionContributer, backref='contribution'),                                                  
    'userOrganization':orm.relation(cls.UserOrganization),
})

orm.mapper(cls.ContributionContributer, contribution_contributer_table, properties={
    'contribution_user':orm.relation(cls.User, backref='contributer'),                                                
})


orm.mapper(cls.Bid, bid_table, properties={
    'bid_owner':orm.relation(cls.User, backref='bid'),    
})

orm.mapper(cls.Organization, organization_table, properties={
    'userOrganizations':orm.relation(cls.UserOrganization, backref='organization'),                                                  
})



"""
# BELOW is an example of relations between objects, (for when you dont have just a simple object that holds data)
# in this example we see "comments", and "tags" tables which have an additional column  which relates back  to a "page" object. 

page_table = schema.Table('page', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('page_seq_id', optional=True), primary_key=True),
    schema.Column('content', types.Text(), nullable=False),
    schema.Column('posted', types.DateTime(), default=now),
    schema.Column('title', types.Unicode(255), default=u'Untitled Page'),
    schema.Column('heading', types.Unicode(255)),
)
comment_table = schema.Table('comment', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('comment_seq_id', optional=True), primary_key=True),
    schema.Column('pageid', types.Integer,
        schema.ForeignKey('page.id'), nullable=False),
    schema.Column('content', types.Text(), default=u''),
    schema.Column('name', types.Unicode(255)),
    schema.Column('email', types.Unicode(255), nullable=False),
    schema.Column('created', types.TIMESTAMP(), default=now()),
)
pagetag_table = schema.Table('pagetag', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('pagetag_seq_id', optional=True), primary_key=True),
    schema.Column('pageid', types.Integer, schema.ForeignKey('page.id')),
    schema.Column('tagid', types.Integer, schema.ForeignKey('tag.id')),
)
tag_table = schema.Table('tag', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('tag_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(20), nullable=False, unique=True),
)

class Page(object):
    pass

class Comment(object):
    pass

class Tag(object):
    pass

orm.mapper(Page, page_table, properties={
    'comments':orm.relation(Comment, backref='page'),
    'tags':orm.relation(Tag, secondary=pagetag_table)
})
orm.mapper(Comment, comment_table)
orm.mapper(Tag, tag_table)
"""