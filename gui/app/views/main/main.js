'use strict';

/**
 * @ngdoc function
 * @name olssenApp.view:MainView
 * @description
 * # MainCtrl
 * View and Controller with routing of the olssenApp main view
 */
var mainView = angular.module('olssenApp.mainView', ['ngRoute']);

mainView.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/', {
            templateUrl: 'views/main/main.html',
            controller: 'MainViewCtrl'
        });
    }
]);
mainView.controller('MainViewCtrl', function () {

});
