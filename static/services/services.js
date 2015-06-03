'use strict';
var bfAPIServices = angular.module('BFAPIServices', ['ngResource']);

bfAPIServices.factory('Contributions', ['$resource',
                                   function($resource){
                                     return $resource('contribution/all', {}, {
                                       getAllContributions: {method:'GET', params:{}, isArray:true}
                                     });
}]);

bfAPIServices.factory('ContributionDetail', ['$resource',
                                                function($resource){
                                                  return $resource('contribution/:contributionId', {}, {
                                                    getDetail: {method:'GET', params:{}, isArray:false}
                                               });
          }]); 

bfAPIServices.factory('SaveContribution', ['$resource',
                                           function($resource){
   											return $resource('contribution', {}, {
                                               save: {method:'POST', params:{}, isArray:false}
                                          });
     }]);