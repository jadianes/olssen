'use strict';

describe('Directive: olssStats', function () {

  // load the directive's module
  beforeEach(module('onlineSpectralSearchGuiApp'));

  var element,
    scope;

  beforeEach(inject(function ($rootScope) {
    scope = $rootScope.$new();
  }));

  it('should make hidden element visible', inject(function ($compile) {
    element = angular.element('<olss-stats></olss-stats>');
    element = $compile(element)(scope);
    expect(element.text()).toBe('this is the olssStats directive');
  }));
});
