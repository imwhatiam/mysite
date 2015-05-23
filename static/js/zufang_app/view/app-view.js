define([
    'jquery',
    'backbone',
    'zufang_app/view/item-view',
    'zufang_app/collection/collection'
], function($, Backbone, Item, Collection) {
    'use strict';

    var AppView = Backbone.View.extend({

        el: $('#zufang-table'),

        initialize: function() {
            console.log('zufang_app/view/app-view.js: app-view init');
            this.$tableBody = this.$('tbody');

            this.collection = new Collection();
            this.listenTo(this.collection, 'reset', this.reset);
            this.collection.fetch({reset: true});
        },

        addOne: function(model) {
            var view = new Item({model: model});
            this.$tableBody.append(view.render().el);
        },

        reset: function() {
            console.log('zufang_app/view/app-view.js: collection reset');
            this.collection.each(this.addOne, this);
        }

    });

    return AppView;
});
