define([
    'backbone'
], function(Backbone) {
    'use strict';

    console.log('zufang_app/model/model.js: model extend');
    var Model = Backbone.Model.extend({
        url: function() {
            var original_url = Backbone.Model.prototype.url.call( this );
            var parsed_url = original_url + ( original_url.charAt( original_url.length - 1 ) == '/' ? '' : '/' );

            return parsed_url;
        }
    });

    return Model;
});
