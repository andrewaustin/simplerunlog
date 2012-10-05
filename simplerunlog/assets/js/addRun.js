$(document).ready(function() {
    var date = $( "#id_date" ),
        distance = $( "#id_distance" ),
        hours = $( "#id_hours" ),
        minutes = $( "#id_minutes" ),
        seconds = $( "#id_seconds" ),
        allFields = $( [] ).add( date ).add( distance ).add( hours ).add( minutes ).add( seconds ),
        tips = $( ".validateTips" );

    function updateTips( t ) {
        tips
        .text( t )
        .addClass( "ui-state-highlight" );
        setTimeout(function() {
            tips.removeClass( "ui-state-highlight", 1500 );
        }, 500 );
    }

    function checkLength( o, n, min, max ) {
        if ( o.val().length > max || o.val().length < min ) {
            o.addClass( "ui-state-error" );
            updateTips( "Length of " + n + " must be between " +
                min + " and " + max + "." );
            return false;
        } else {
            return true;
        }
    }

    function checkRegexp( o, regexp, n ) {
        if ( !( regexp.test( o.val() ) ) ) {
            o.addClass( "ui-state-error" );
            updateTips( n );
            return false;
        } else {
            return true;
        }
    }

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

    $( "#dialog-form" ).dialog({
        autoOpen: false,
        height: 400,
        width: 400,
        modal: true,
        buttons: {
            "Add Run": function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );

                bValid = bValid && checkLength( date, "date", 10, 10 );
                bValid = bValid && checkLength( distance, "distance", 0, 100 );
                bValid = bValid && checkLength( hours, "hours", 0, 2 );
                bValid = bValid && checkLength( minutes, "minutes", 0, 2 );
                bValid = bValid && checkLength( seconds, "seconds", 0, 2 );

                //bValid = bValid && checkRegexp( name, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                //bValid = bValid && checkRegexp( password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );

                if ( bValid ) {
                    that = $( this )
                    $.ajax({
                        url: "/add/",
                        type: "POST",
                        data: $( "#dialog-form-data" ).serialize(),
                        success:function(data) {
                            if(data.hasOwnProperty("id")) {
                                that.dialog( "close" );
                            } else {
                                $.each(data, function(key, value) {
                                    updateTips(value);
                                });
                            }
                        }
                    });
                }
            },
            Cancel: function() {
                $( this ).dialog( "close" );
            }
        },
        close: function() {
            allFields.val( "" ).removeClass( "ui-state-error" );
        }
    });

    $("#id_date").datepicker({dateFormat:'yy-mm-dd'})

    $( "#addRun" )
        .click(function() {
            $( "#dialog-form" ).dialog( "open" );
        });
});
