$(function() {
    var date = $( "#date" ),
        distance = $( "#distance" ),
        hours = $( "#hours" ),
        minutes = $( "#minutes" ),
        seconds = $( "#seconds" ),
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

    $( "#dialog-form" ).dialog({
        autoOpen: false,
        height: 400,
        width: 400,
        modal: true,
        buttons: {
            "Add Run": function() {
                var bValid = true;
                allFields.removeClass( "ui-state-error" );

                bValid = bValid && checkLength( date, "date", 3, 16 );
                bValid = bValid && checkLength( distance, "distance", 0, 100 );
                bValid = bValid && checkLength( hours, "hours", 0, 2 );
                bValid = bValid && checkLength( minutes, "minutes", 0, 2 );
                bValid = bValid && checkLength( seconds, "seconds", 0, 2 );

                //bValid = bValid && checkRegexp( name, /^[a-z]([0-9a-z_])+$/i, "Username may consist of a-z, 0-9, underscores, begin with a letter." );
                //bValid = bValid && checkRegexp( password, /^([0-9a-zA-Z])+$/, "Password field only allow : a-z 0-9" );

                if ( bValid ) {
                    //$( "#users tbody" ).append( "<tr>" +
                    //"<td>" + name.val() + "</td>" +
                    //"<td>" + email.val() + "</td>" +
                    //"<td>" + password.val() + "</td>" +
                    //"</tr>" );
                    $( this ).dialog( "close" );
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

    $( "#addRun" )
        .click(function() {
            $( "#dialog-form" ).dialog( "open" );
        });
});
