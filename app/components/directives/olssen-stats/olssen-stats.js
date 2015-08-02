'use strict';

/**
 * @ngdoc directive
 * @name olssenApp.directive:olssenStats
 * @description
 * # olssenStats
 */
var olssenStatsDirective = angular.module('olssenApp.olssenStatsDirective', [])

olssenStatsDirective.directive('olssenStats', function () {
    return {
      templateUrl: 'components/directives/olssen-stats/olssen-stats.html',
      restrict: 'E',
      controller: 'OlssenStatsDirectiveCtrl'
    };
});

olssenStatsDirective.controller('OlssenStatsDirectiveCtrl', ['$scope', 'OlssenWSStatsService',
    function($scope, OlssenWSService) {
      OlssenWSService.list(
        {},
        function (stats) {
          $scope.allStats = angular.fromJson(stats);
        }
      );
    }
]);
