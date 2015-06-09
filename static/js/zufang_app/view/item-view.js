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

        initialize: function(options) {
            this.key_word = options.key_word;
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

            $('#messages').css({'left':($(window).width() - $('#messages').width())/2, 'top':10}).removeClass('hide');
            setTimeout(function() { $('#messages').addClass('hide'); }, time);
        },

        getLocalTime: function(timestamp) {
            var d = new Date(timestamp * 1000),
                year = d.getFullYear(),
                month = d.getMonth() + 1,
                day = d.getDate(),
                hour = d.getHours(),
                minute = d.getMinutes();

            if (month < 10) {
                month = '0' + month;
            }

            if (day < 10) {
                day = '0' + day;
            }

            if (hour < 10) {
                hour = '0' + hour;
            }

            if (minute < 10) {
                minute = '0' + minute;
            }

            return year + '-' + month + '-' + day + ' ' + hour + ':' + minute;
        },

        HTMLescape: function(html) {
            return document.createElement('div')
                .appendChild(document.createTextNode(html))
                .parentNode
                .innerHTML;
        },

        render: function () {
            var data = this.model.toJSON(),
                key_word = this.key_word;

            data['reply_time'] = this.getLocalTime(data['timestamp']);

            if (key_word != 'undefined') {
                if (data['topic_title'].indexOf(key_word) > -1) {
                    data['topic_title'] = data['topic_title'].replace(key_word, "<span class='highlight'>" + this.HTMLescape(key_word) + "</span>")
                }
            }

            this.$el.html(this.template(data));
            return this;
        }
    });

    return ItemView;
});
