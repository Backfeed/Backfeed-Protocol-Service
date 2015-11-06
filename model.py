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
Agent - schema definition:
"""
agent_table = schema.Table('agent', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('agent_seq_id', optional=True), primary_key=True),

    schema.Column('name', types.Unicode(255)),
    schema.Column('fullName', types.Unicode(255)),
    schema.Column('imgUrl', types.Unicode(255)),
)


agent_handle_table = schema.Table('agent_handle', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('agent_seq_id', optional=True), primary_key=True),

    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id'),nullable=False),
    schema.Column('handleName', types.Unicode(255)),
    schema.Column('handleType', types.Unicode(255)),
)

"""
Network - schema definition:
"""
network_table = schema.Table('network', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('network_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id'),nullable=False),                              
    schema.Column('name', types.Unicode(255),nullable=False),
    schema.Column('description', types.Unicode(255)),
    schema.Column('protocol', types.Unicode(255),nullable=False),
)

"""
Agent networks - schema definition:
"""
agent_network_table = schema.Table('agent_network', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('agent_network_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id')),
    schema.Column('networkId', types.Integer,
        schema.ForeignKey('network.id')),
)


"""
Collaboration - schema definition:
"""
collaboration_table = schema.Table('collaboration', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('collaboration_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id'),nullable=False),
    schema.Column('networkId', types.Integer,
        schema.ForeignKey('network.id'),nullable=False),
    schema.Column('protocol',types.Unicode(2000)),
    schema.Column('tokenName', types.Unicode(60)),
    schema.Column('name', types.Unicode(255),nullable=False),
    schema.Column('description', types.Unicode(255),nullable=False),
    schema.Column('tokenSymbol', types.Unicode(3)),
    schema.Column('tokenTotal', types.Integer),
    schema.Column('comment', types.Unicode(2000)),
    schema.Column('status', types.Unicode(100),default=u'Open'),
    schema.Column('similarEvaluationRate', types.Integer),
    schema.Column('passingResponsibilityRate', types.Integer),
)

"""
Agent collaborations - schema definition:
"""
agent_collaboration_table = schema.Table('agent_collaboration', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('agent_collaboration_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id')),
    schema.Column('collaborationId', types.Integer,
        schema.ForeignKey('collaboration.id')),
    schema.Column('tokens', types.Float),
    schema.Column('reputation',  types.Float),   
)

"""
collaboration hanldes - schema definition:
"""
collaboration_handle_table = schema.Table('collaboration_handle', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('collaboration_handle_seq_id', optional=True), primary_key=True),
    schema.Column('collaborationId', types.Integer,
        schema.ForeignKey('collaboration.id')),
    schema.Column('handleName', types.Unicode(255)),
    schema.Column('handleType', types.Unicode(255)),   
)




"""
Contribution - schema definition:
"""
contribution_table = schema.Table('contribution', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('contribution_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id')),
    schema.Column('agentCollaborationId', types.Integer,
        schema.ForeignKey('agent_collaboration.id')),
    schema.Column('timeCreated', types.DateTime(), default=now),
    schema.Column('comment', types.Unicode(2000)),
    schema.Column('type', types.Unicode(340)),
    schema.Column('status', types.Unicode(100),default=u'Open'),
    schema.Column('currentValuation',  types.Float,default=0),
    schema.Column('valueIndic',  types.Integer,default=0),
    schema.Column('content',  types.Unicode(10000)),
)


"""
Contribution Contributors List - schema definition:
"""
contribution_contributor_table = schema.Table('contribution_contributor', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('contribution_contributor_seq_id', optional=True), primary_key=True),
    schema.Column('contributionId', types.Integer,
        schema.ForeignKey('contribution.id')),
    schema.Column('contributorId', types.Integer,
        schema.ForeignKey('agent.id')),
    schema.Column('percentage', types.FLOAT),   
)
   

"""
Contribution value- schema definition:
"""
contribution_value_table = schema.Table('contributionValue', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('contribution_value_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id')),
    schema.Column('agentCollaborationId', types.Integer,
        schema.ForeignKey('agent_collaboration.id')),
    schema.Column('contributionId', types.Integer,
        schema.ForeignKey('contribution.id')),
    schema.Column('reputationGain',  types.Float,default=0),
    schema.Column('reputation',  types.Float,default=0),
)

"""
Evaluation - schema definition:
"""
evaluation_table = schema.Table('evaluation', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('evaluation_seq_id', optional=True), primary_key=True),
    schema.Column('agentId', types.Integer,
        schema.ForeignKey('agent.id')),   
    schema.Column('contributionId', types.Integer,
        schema.ForeignKey('contribution.id')),
    schema.Column('tokens', types.Float),
    schema.Column('stake', types.Float),
    schema.Column('reputation',  types.Float),
    schema.Column('contributionValueAfterEvaluation',  types.Float),
    schema.Column('timeCreated', types.DateTime(), default=now),
    schema.Column('comment', types.Unicode(2000)),

)



"""
Tag - schema definition:
"""
tag_table = schema.Table('tag', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('tag_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(255),nullable=False),
)

"""
Link - schema definition:
"""
link_table = schema.Table('link', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('link_seq_id', optional=True), primary_key=True),
    schema.Column('name', types.Unicode(255),nullable=False),
)

"""
Tag LINK - schema definition:
"""
tag_link_table = schema.Table('tag_link', metadata,
    schema.Column('id', types.Integer,
        schema.Sequence('tag_link_seq_id', optional=True), primary_key=True),
    schema.Column('tagId', types.Integer,
        schema.ForeignKey('tag.id'),nullable=False),
    schema.Column('linkId', types.Integer,
        schema.ForeignKey('link.id'),nullable=False), 
    schema.Column('contributionId', types.Integer,
        schema.ForeignKey('contribution.id'),nullable=False),                                                       
)


"""
Relationships - definitions
"""

orm.mapper(cls.Agent, agent_table, properties={
    'agentHandles':orm.relation(cls.AgentHandle, backref='agent'),
    'agentNetworks':orm.relation(cls.AgentNetwork, backref='agent'),
    'agentCollaborations':orm.relation(cls.AgentCollaboration, backref='agent'),
    'agentContributions':orm.relation(cls.Contribution, backref='agent'),
    'agentEvaluations':orm.relation(cls.Evaluation, backref='agent'),
})

orm.mapper(cls.AgentHandle, agent_handle_table)

orm.mapper(cls.AgentNetwork, agent_network_table)

orm.mapper(cls.Network, network_table, properties={
    'agentNetworks':orm.relation(cls.AgentNetwork, backref='network'),  
    'agent':orm.relation(cls.Agent, backref='network'),
    'collaborations':orm.relation(cls.Collaboration, backref='network'),                                                
})


orm.mapper(cls.Collaboration, collaboration_table, properties={
    'agentCollaborations':orm.relation(cls.AgentCollaboration, backref='collaboration'),  
    'handles':orm.relation(cls.CollaborationHandle, backref='collaboration'),
    'agent':orm.relation(cls.Agent, backref='collaboration'),                                                
})

orm.mapper(cls.AgentCollaboration, agent_collaboration_table, properties={
        'contributions':orm.relation(cls.Contribution),                                                              
})

orm.mapper(cls.CollaborationHandle, collaboration_handle_table)

orm.mapper(cls.Tag, tag_table)

orm.mapper(cls.LINK, link_table)

orm.mapper(cls.TagLINK, tag_link_table, properties={
    'tag':orm.relation(cls.Tag, backref='links'),  
    'link':orm.relation(cls.LINK, backref='tags'),  
    'contribution':orm.relation(cls.Contribution, backref='taglink'),                                                 
    
})

orm.mapper(cls.Contribution, contribution_table, properties={
    'evaluations':orm.relation(cls.Evaluation, backref='contribution'),  
    'contributors':orm.relation(cls.ContributionContributor, backref='contribution'),                                                  
    'agentCollaboration':orm.relation(cls.AgentCollaboration),
    'contributionValues':orm.relation(cls.ContributionValue),
    
})

orm.mapper(cls.ContributionContributor, contribution_contributor_table, properties={
    'agent':orm.relation(cls.Agent, backref='contributor'),                                                
})

orm.mapper(cls.ContributionValue, contribution_value_table)

orm.mapper(cls.Evaluation, evaluation_table)






