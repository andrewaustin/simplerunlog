$(document).ready(function() {

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });

    $( "#week_cal" )
        .append(function() {
            var result = '';
            var d = new Date();
            var startday = d.getDate() - (d.getDay() + 7) % 7;
            result += '<table id="weekcal" class="bordered">\n';
            result += '<thead>\n';
            result += '<tr><th>Sunday</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th></tr>\n';
            result += '</thead>\n';
            result += '<tr>\n';
            result += '<td><div class="day">' + startday + '</div></td>';
            result += '<td><div class="day">' + (startday+1) + '</div>boo!</td>';
            result += '<td><div class="day">' + (startday+2) + '</div></td>';
            result += '<td><div class="day">' + (startday+3) + '</div></td>';
            result += '<td><div class="day">' + (startday+4) + '</div></td>';
            result += '<td><div class="day">' + (startday+5) + '</div></td>';
            result += '<td><div class="day">' + (startday+6) + '</div></td>';
            result += '\n';
            result += '</tr>\n';
            result += '</table>\n';
            return result;
        });
});
