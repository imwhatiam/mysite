define([
    'jquery',
    'backbone',
    'zufang_app/view/app-view'
], function($, Backbone, View) {
    "use strict";

    var Router = Backbone.Router.extend({
        routes: {
            // Default
            '*path': 'showList'
        },

        initialize: function() {
            console.log('zufang_app/router.js: router init');
            this.view = new View();
        },

        showList: function() {
            console.log('zufang_app/router.js: show zufang list');
        },
    });

    return Router;
});
