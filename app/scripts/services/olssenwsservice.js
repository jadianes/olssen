'use strict';

var olssenWsUrl = "http://jupiter:5432";


/**
 * @ngdoc service
 * @name onlineSpectralSearchGuiApp.olssenWSService
 * @description
 * # olssenWSService
 * Factory in the onlineSpectralSearchGuiApp.
 */
var olssenWsService = angular.module('onlineSpectralSearchGuiApp.olssenWSService', ['ngResource']);

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
