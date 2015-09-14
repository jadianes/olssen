'use strict';

/**
 * @ngdoc function
 * @name olssenApp.view:StatsView
 * @description
 * # StatsViewCtrl
 * View and Controller with routing of the olssenApp stats view
 */
var statsView = angular.module('olssenApp.statsView', ['ngRoute']);

statsView.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/stats', {
            templateUrl: 'views/stats/stats.html',
            controller: 'StatsViewCtrl'
        });
    }
]);
statsView.controller('StatsViewCtrl', function () {

});

