define([
    'backbone',
    'zufang_app/model/model'
], function(Backbone, Model) {
    'use strict';

    console.log('zufang_app/collection/collection.js: collection extend');
    var Collection = Backbone.Collection.extend({
        model: Model,
        url: '/api/zufang-items/'
    });

    return Collection;
});
