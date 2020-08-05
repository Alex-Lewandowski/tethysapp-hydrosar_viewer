// base.html scripts has additional vars from render context
let csrftoken = Cookies.get('csrftoken');
Cookies.set('instance_id', instance_id);
function csrfSafeMethod(method){return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
$.ajaxSetup({beforeSend: function (xhr, settings) {if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

const map_obj = map();

const my_basemaps = basemaps();