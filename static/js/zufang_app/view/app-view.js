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

        accessCountTemplate: _.template($('#access-count-tmpl').html()),

        initialize: function() {
            console.log('zufang_app/view/app-view.js: app-view init');
            this.$tableBody = this.$('tbody');
            this.$accessCount = this.$('#access-count');

            this.collection = new Collection();
            this.listenTo(this.collection, 'reset', this.reset);
            this.collection.fetch({reset: true});
            this.getAccessCount();
        },

        events: {
            'click #search-submit': 'inputSearch',
            'click #show-all': 'reset',
            'click .direct-search': 'directSearch'
        },

        getAccessCount: function() {
            var _this = this;
            $.ajax({
                url: '/api/zufang-access-count/',
                success: function(data) {
                    _this.$accessCount.html(_this.accessCountTemplate(data));
                }
            });
        },

        directSearch: function(e) {
            var value = $(e.currentTarget).text();
            this.search(value);
            return false
        },

        inputSearch: function() {
            var value = $('#search-input').val();
            this.search(value);
            return false
        },

        search: function(value) {
            var _this = this,
                result = [];

            this.collection.each(function (model) {
                var title = model.get('topic_title');
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
