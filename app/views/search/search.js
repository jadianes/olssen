'use strict';

/**
 * @ngdoc function
 * @name onlineSpectralSearchGuiApp.controller:SearchformCtrl
 * @description
 * # SearchformCtrl
 * Controller of the onlineSpectralSearchGuiApp
 */
angular.module('onlineSpectralSearchGuiApp')
  .controller('SearchformCtrl', function () {
      $scope.result = {};

      $scope.update = function(search) {
        $scope.result = angular.copy(search);
      };

      $scope.reset = function() {
        $scope.search = angular.copy($scope.master);
      };

      $scope.reset();
  });
