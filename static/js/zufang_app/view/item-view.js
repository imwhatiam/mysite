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
                        _this.feedback('Success', 'success');
                    } else {
                        _this.feedback('Already like this', 'error');
                    }
                }
            });
        },

        feedback: function(con, type) {
            var time = 5000;

            if ($('#messages').length > 0) {
                $('#messages').html('<span class="' + type + '">' + con + '</span>');
            } else {
                var html = '<div id="messages"><span class="' + type + '">' + con + '</span></div>';
                $('#zufang').append(html);
            }

            console.log($(window).width())
            console.log($('#messages').width())
            $('#messages').css({'left':($(window).width() - $('#messages').width())/2, 'top':10}).removeClass('hide');
            setTimeout(function() { $('#messages').addClass('hide'); }, time);
        },


        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        }
    });

    return ItemView;
});
