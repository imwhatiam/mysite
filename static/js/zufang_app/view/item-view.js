define([
    'jquery',
    'underscore',
    'backbone'
], function($, _, Backbone) {
    'use strict';

    var ItemView = Backbone.View.extend({
        tagName: 'tr',

        template: _.template($('#zufang-item-tmpl').html()),

        events: {
        },

        initialize: function() {
        },

        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return ItemView;
});
