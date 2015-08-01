'use strict';

/**
 * @ngdoc directive
 * @name onlineSpectralSearchGuiApp.directive:olssenStats
 * @description
 * # olssenStats
 */
var olssenStatsDirective = angular.module('onlineSpectralSearchGuiApp.olssenStatsDirective', [])

olssenStatsDirective.directive('olssenStats', function () {
    return {
      templateUrl: 'scripts/directives/olssen-stats.html',
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
