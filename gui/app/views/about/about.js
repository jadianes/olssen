'use strict';

/**
 * @ngdoc function
 * @name olssenApp.view:AboutView
 * @description
 * # AboutViewCtrl
 * View and Controller with routing of the olssenApp about view
 */
var aboutView = angular.module('olssenApp.aboutView', ['ngRoute']);

aboutView.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/about', {
            templateUrl: 'views/about/about.html',
            controller: 'AboutViewCtrl'
        });
    }
]);
aboutView.controller('AboutViewCtrl', function () {

});

