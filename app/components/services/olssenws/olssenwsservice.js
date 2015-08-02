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
