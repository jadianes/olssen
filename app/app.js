'use strict';

/**
 * @ngdoc overview
 * @name olssenApp
 * @description
 * # olssenApp
 *
 * Main module of the application.
 */
angular
  .module('olssenApp', [
    'ngAnimate',
    'ngResource',
    'ngRoute',
    'olssenApp.mainView',
    'olssenApp.aboutView',
    'olssenApp.statsView',
    'olssenApp.olssenStatsDirective',
    'olssenApp.olssenWSService'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .otherwise({
        redirectTo: '/'
      });
  });
