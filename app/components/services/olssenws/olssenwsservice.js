'use strict';

var olssenWsUrl = "http://jupiter:5432";


/**
 * @ngdoc service
 * @name olssenApp.olssenWSService
 * @description
 * # olssenWSService
 * Factory in the olssenApp.
 */
var olssenWsService = angular.module('olssenApp.olssenWSService', ['ngResource']);

olssenWsService.factory('OlssenWSStatsService', ['$resource', 
  function ($resource) {
    // Public API here
    return $resource(
      olssenWsUrl + '/stats',
      {},
      {
        list: {
          isArray: true,
        }
      }
    );
  }
]);

olssenWsService.factory('OlssenWSSearchService', ['$resource',
  function ($resource) {
    // Public API here
    return $resource(
      olssenWsUrl + '/search',
      {},
      {
        search: {
          method: 'POST',
          isArray: true,
        }
      }
    );
  }
]);
