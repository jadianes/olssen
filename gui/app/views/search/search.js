'use strict';

/**
 * @ngdoc function
 * @name olssenApp.searchView
 * @description
 * # SearchViewCtrl
 * View and Controller of the olssenApp search view
 */
var searchView = angular.module('olssenApp.searchView', ['ngRoute', 'angularFileUpload']);

searchView.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.when('/search', {
            templateUrl: 'views/search/search.html',
            controller: 'SearchViewCtrl'
        });
    }
]);

searchView.controller('SearchViewCtrl', ['$scope', 'FileUploader', 'OlssenWSSearchService', 
    function ($scope, FileUploader, OlssenWSSearchService) {
        var uploader = $scope.uploader = new FileUploader({
            url: 'http://jupiter:5432/search'
        });

        // FILTERS

        uploader.filters.push({
            name: 'customFilter',
            fn: function(item /*{File|FileLikeObject}*/, options) {
                return this.queue.length < 10;
            }
        });

        // CALLBACKS

        uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
            console.info('onWhenAddingFileFailed', item, filter, options);
        };
        uploader.onAfterAddingFile = function(fileItem) {
            console.info('onAfterAddingFile', fileItem);
        };
        uploader.onAfterAddingAll = function(addedFileItems) {
            console.info('onAfterAddingAll', addedFileItems);
        };
        uploader.onBeforeUploadItem = function(item) {
            console.info('onBeforeUploadItem', item);
        };
        uploader.onProgressItem = function(fileItem, progress) {
            console.info('onProgressItem', fileItem, progress);
        };
        uploader.onProgressAll = function(progress) {
            console.info('onProgressAll', progress);
        };
        uploader.onSuccessItem = function(fileItem, response, status, headers) {
            $scope.result = response
            console.info('onSuccessItem', fileItem, response, status, headers);
        };
        uploader.onErrorItem = function(fileItem, response, status, headers) {
            console.info('onErrorItem', fileItem, response, status, headers);
        };
        uploader.onCancelItem = function(fileItem, response, status, headers) {
            console.info('onCancelItem', fileItem, response, status, headers);
        };
        uploader.onCompleteItem = function(fileItem, response, status, headers) {
            console.info('onCompleteItem', fileItem, response, status, headers);
        };
        uploader.onCompleteAll = function() {
            console.info('onCompleteAll');
        };

        console.info('uploader', uploader);
    }
]);
