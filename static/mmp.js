Date.prototype.stdTimezoneOffset = function() {
    var jan = new Date(this.getFullYear(), 0, 1);
    var jul = new Date(this.getFullYear(), 6, 1);
    return Math.max(jan.getTimezoneOffset(), jul.getTimezoneOffset());
}

Date.prototype.dst = function() {
    return this.getTimezoneOffset() < this.stdTimezoneOffset();
}

tday = new Array("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday");
tmonth = new Array("January","February","March","April","May","June","July","August","September","October","November","December");

function updateClocks() {

    // local
    GetClock(null, '', 'main');
    setTimeout(GetClock, 1000);

    if (typeof extraClocks != 'object') {
        return;
    }

    if (jQuery.isEmptyObject(extraClocks['1'])) {
        return;
    }

    // Set Custom
    $.each(extraClocks, function( index, value ) {
        GetClock(value.timezone, value.label, 'datetime_' + (index));
    });
}

function getDateFromTS(timestamp) {
    return new Date(timestamp*1000);
}

function GetClock(offset, label, div) {

    var d = new Date();
    if (offset == null) {
        offset = d.getTimezoneOffset() / 60;
    }
    else {
        utc = d.getTime() + (d.getTimezoneOffset() * 60000);
        if (d.dst()) {
            offset++;
        }
        d = new Date(utc + (3600000*offset));
    }

    var nday = d.getDay();
    var nmonth = d.getMonth();
    var ndate = d.getDate();
    var nyear = d.getFullYear();

    var nhour = d.getHours()
    var nmin = d.getMinutes();
    var nsec = d.getSeconds();
    var ampm;

    if (nhour ==0 ) {
        ampm = " AM";
        nhour = 12;
    }
    else if (nhour < 12) {
        ampm = " AM";
    }
    else if (nhour == 12) {
        ampm=" PM";
    }
    else if (nhour > 12) {
        ampm=" PM";
        nhour -= 12;
    }

    if(nmin <= 9) {
        nmin = "0" + nmin;
    }
    if(nsec <= 9) {
        nsec = "0" + nsec;
    }

    if (label != "") {
        $('#' + div + ' em').html(label);
        $('#' + div + ' .daydate').html(
            tday[nday] + " " + ndate + ", " + nyear
        );

    }
    else {
        $('#' + div + ' .day').html(tday[nday]);
        $('#' + div + ' .date').html(tmonth[nmonth] + " " + ndate + ", " + nyear);
    }
    $('#' + div + ' .time').html(nhour + ":" + nmin + ":" + nsec + ampm);
}

/*******************************************************************************
 Weather
*******************************************************************************/
function updateWeather(city) {

    // Current Weather
    $.getJSON( "/weather/" + city, function( data ) {
        // console.log(data);
        $('#cityId').val(data.id)


        $('#temp h1').html(data.name);

        $('#riseset #sunrise').html(data.sys.sunrise)
        $('#riseset #sunset').html(data.sys.sunset)

        $('#icon #direction').html(data.wind.deg)
        $('#icon #speed').html(data.wind.speed)
        $('#icon #humidity').html(data.main.humidity)
        $('#icon h6').html(data.weather[0].description)
        $('#icon div.weather-icon').attr("class", "weather-icon " + data.weather[0].icon)

        $('#temp h2 em').html(data.main.temp)
        $('#temp h3 em:first').html(data.main.temp_min)
        $('#temp h3 em:last').html(data.main.temp_max)

        // Forecast
        $.getJSON( "/forecast/" + data.id, function( data ) {
            var i = 1;

            jQuery.each(data, function(i, val) {
                $('#forecast #forecast_' + (i) + ' em.day').html(val['day'])
                $('#forecast #forecast_' + (i) + ' div.weather-icon').attr("class", "weather-icon " + val['icon'])
                $('#forecast #forecast_' + (i) + ' em.low').html(val['temp_min'])
                $('#forecast #forecast_' + (i) + ' em.high').html(val['temp_max'])
            });
        });

    });
}

/*******************************************************************************
 News
*******************************************************************************/
function updateNews() {
    $.getJSON( "/news/", function( data ) {
        $('ul').empty();
        $.each( data, function( key, val ) {
            $("ul").append('<li>' + val + ' </li>');
        });
    });
}