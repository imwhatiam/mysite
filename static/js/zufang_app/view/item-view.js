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
            'click .like': 'like'
        },

        initialize: function() {
            this.listenTo(this.model, "change", this.render);
        },

        like: function () {
            var _this = this;
            this.model.save(null, {
                success: function (data) {
                    if (_this.model.get('like_success')) {
                        alert('Success');
                    } else {
                        alert('Already like this');
                    }
                }
            });
        },

        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return ItemView;
});
