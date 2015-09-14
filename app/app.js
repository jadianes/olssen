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
    'angularFileUpload',
    'olssenApp.mainView',
    'olssenApp.aboutView',
    'olssenApp.statsView',
    'olssenApp.searchView',
    'olssenApp.olssenStatsDirective',
    'olssenApp.olssenWSService'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .otherwise({
        redirectTo: '/'
      });
  });
