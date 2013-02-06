/*!
 * Simple jQuery Countdown (compressed)
 * https://github.com/jonasanx/jQuery-simple-countdown
 * @author Jonathan J. Flores
 */
(function(a){a.scountdown=function(b,c){var d=this;var e={days:24*60*60,hours:60*60,minutes:60};d.init=function(){var b=a.extend({},{timestamp:0,callback:function(){}},c);(function d(){var a=Math.floor((b.timestamp-new Date)/1e3);var c={};if(a<0)a=0;for(key in e){var g=e[key];var h=c[key]=f(Math.floor(a/g));a-=h*g}b.callback(c.days,c.hours,c.minutes,f(a));setTimeout(d,1e3)})()};var f=function(a){return a.toString().length<2?"0"+a:a};d.init()};a.fn.scountdown=function(b){return this.each(function(){var c=new a.scountdown(this,b)})}})(jQuery)