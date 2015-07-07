'use strict';

/**
 * @ngdoc overview
 * @name onlineSpectralSearchGuiApp
 * @description
 * # onlineSpectralSearchGuiApp
 *
 * Main module of the application.
 */
angular
  .module('onlineSpectralSearchGuiApp', [
    'ngAnimate',
    'ngResource',
    'ngRoute'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutCtrl',
        controllerAs: 'about'
      })
      .otherwise({
        redirectTo: '/'
      });
  });
