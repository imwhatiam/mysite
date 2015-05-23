define([
    'jquery',
    'backbone',
    'underscore',
    'zufang_app/view/item-view',
    'zufang_app/collection/collection'
], function($, Backbone, _, Item, Collection) {
    'use strict';

    var AppView = Backbone.View.extend({

        el: $('#zufang'),

        initialize: function() {
            console.log('zufang_app/view/app-view.js: app-view init');
            this.$tableBody = this.$('tbody');

            this.collection = new Collection();
            this.listenTo(this.collection, 'reset', this.reset);
            this.collection.fetch({reset: true});
        },

        events: {
            'click #search-submit': 'search',
            'click #show-all': 'reset'
        },

        search: function() {
            var value = $('#search-input').val(),
                _this = this,
                result = [];

            this.collection.each(function (model) {
                var title = model.get('title');
                if (title.indexOf(value) > -1) {
                    result.push(model);
                }
            });

            this.$tableBody.empty();

            _.each(result, function (item) {
                _this.addOne(item);
            });

            return false;
        },

        addOne: function(model) {
            var view = new Item({model: model});
            this.$tableBody.append(view.render().el);
        },

        reset: function() {
            console.log('zufang_app/view/app-view.js: collection reset');
            this.$tableBody.empty();
            this.collection.each(this.addOne, this);
            return false;
        }

    });

    return AppView;
});
