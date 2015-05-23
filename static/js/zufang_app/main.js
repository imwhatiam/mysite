define([
    'zufang_app/router'
], function(Router){
    console.log('zufang_app/main.js: router start');
    var router = new Router();
    Backbone.history.start();
});
