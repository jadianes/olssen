'use strict';

/**
 * @ngdoc directive
 * @name onlineSpectralSearchGuiApp.directive:olssStats
 * @description
 * # olssStats
 */
angular.module('onlineSpectralSearchGuiApp')
  .directive('olssStats', function () {
    return {
      template: '<div>Stats</div>',
      restrict: 'E',
      link: function postLink(scope, element, attrs) {
        element.text('this is the olssStats directive');
      }
    };
  });
