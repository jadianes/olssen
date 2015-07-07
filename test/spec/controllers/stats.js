'use strict';

describe('Controller: StatsCtrl', function () {

  // load the controller's module
  beforeEach(module('onlineSpectralSearchGuiApp'));

  var StatsCtrl;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    StatsCtrl = $controller('StatsCtrl', {
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(StatsCtrl.awesomeThings.length).toBe(3);
  });
});
