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

    function date_to_string(date) {
        return date.getFullYear() + '-' + (date.getMonth()+1) + '-' + date.getDate();
    }

    $( "#week_cal" )
        .append(function() {
            var result = '';

            var startdate = new Date();
            startdate.setDate(startdate.getDate() - (startdate.getDay() + 7) % 7);

            var datearray = Array();
            for (var i = 0; i < 7; i++) {
                var newDate = new Date();
                newDate.setDate(startdate.getDate() + i );
                datearray.push(newDate);
            }

            getData = 'date__gte=' + date_to_string(datearray[0]) + '&date__lte=' + date_to_string(datearray[datearray.length-1]);

            $.ajax({
                url: '/api/v1/run/',
                data: getData,
                dataType: 'json'
            });

            result += '<table id="weekcal" class="bordered">\n';
            result += '<thead>\n';
            result += '<tr><th>Sunday</th><th>Monday</th><th>Tuesday</th><th>Wednesday</th><th>Thursday</th><th>Friday</th><th>Saturday</th></tr>\n';
            result += '</thead>\n';
            result += '<tr>\n';
            for (var i = 0; i < datearray.length; i++) {
                result += '<td><div class="day">' + datearray[i].getDate() + '</div></td>';
            }
            result += '\n';
            result += '</tr>\n';
            result += '</table>\n';

            return result;
        });
});
