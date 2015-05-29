require.config({
    // The shim config allows us to configure dependencies for
    // scripts that do not call define() to register a module
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: ['underscore', 'jquery'],
            exports: 'Backbone'
        },
    },
    paths: {
        backbone: 'lib/backbone-1.1.2',
        underscore: 'lib/underscore-1.7.0',
        bootstrap: 'lib/bootstrap.min',
        jquery: 'lib/jquery-2.1.3'
    }
});
console.log('main.js of require.js');
require(['zufang_app/main']);
