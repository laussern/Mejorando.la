define([
    'jquery',
    'vendor/jquery.scountdown'], function ($) {
        var _hora, 
            hora = $("#hora"),
            proximo = $("#proximo"),
            timestamp = parseInt(proximo.attr('data-timestamp'), 10);

        function formatNumber(rep) {
            rep = rep + ''; // coerce to string
            if (rep < 1000) {
                return rep; // return the same number
            }
            else if (rep < 5000) { // place a comma between
                return rep.charAt(0) + ',' + rep.substring(1);
            }
            else { // divide and format
                return (rep / 1000).toFixed(rep % 1000 !== 0) + 'k';
            }
        }

        return {
            boot: function () {
                _hora = new Date(timestamp);
                hora.text(_hora.toString("h:mmtt"));

                proximo.scountdown({
                    timestamp: timestamp,
                    callback: function (d, h, m, s) {
                        $(".dias", proximo).text(d);
                        $(".horas", proximo).text(h);
                        $(".minutos", proximo).text(m);
                        $(".segundos", proximo).text(s);
                }});
            }
        };
});