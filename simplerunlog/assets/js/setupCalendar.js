$(document).ready(function() {
    $('#calendar').fullCalendar({
        editable: false,
        events: "/run/",
    });
});

