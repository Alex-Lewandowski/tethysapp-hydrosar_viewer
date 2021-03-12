// base.html scripts has additional vars from render context
let csrftoken = Cookies.get('csrftoken');
Cookies.set('instance_id', instance_id);
function csrfSafeMethod(method){return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
$.ajaxSetup({beforeSend: function (xhr, settings) {if (!csrfSafeMethod(settings.type) && !this.crossDomain) {xhr.setRequestHeader("X-CSRFToken", csrftoken);}}});

////////////////////////////////////////////////////////////////////////  Initialize the Map
const map_obj = map();
const my_basemaps = basemaps();
map_obj.on("mousemove", function (event) {$("#mouse-position").html('Lat: ' + event.latlng.lat.toFixed(5) + ', Lon: ' + event.latlng.lng.toFixed(5));});
let wms_obj = newWMS();
legend.addTo(map_obj);
controlsObj = makeControls();
latlon.addTo(map_obj);

////////////////////////////////////////////////////////////////////////  EVENT LISTENERS
function update() {
    layerWMS = newWMS();
    controlsObj = makeControls();
    legend.addTo(map_obj);
}

function requestTimeSeries(){
    let data = {};
    $.ajax({
        url: URL_requestTimeSeries,
        data: data,
        dataType: 'json',
        contentType: "application/json",
        method: 'GET',
        success: function (result) {console.log("Success")}
    })
}

