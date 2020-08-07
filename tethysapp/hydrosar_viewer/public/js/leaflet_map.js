////////////////////////////////////////////////////////////////////////  MAP FUNCTIONS
function map() {
    // create the map
    return L.map('map', {
        zoom: 7,
        minZoom: 2,
        zoomSnap: .5,
        boxZoom: true,
        maxBounds: L.latLngBounds(L.latLng(-100.0, -270.0), L.latLng(100.0, 270.0)),
        center: [23.933177, 90.067217],
        timeDimension: true,
        timeDimensionControl: true,
        timeDimensionControlOptions: {
            position: "bottomleft",
            autoPlay: true,
            loopButton: true,
            backwardButton: true,
            forwardButton: true,
            timeSliderDragUpdate: true,
            minSpeed: 2,
            maxSpeed: 6,
            speedStep: 1,
        },
    });
}

function basemaps() {
    // create the basemap layers
    let esri_imagery = L.esri.basemapLayer('Imagery');
    let esri_terrain = L.esri.basemapLayer('Terrain');
    let esri_labels = L.esri.basemapLayer('ImageryLabels');
    let esri_topo = L.esri.basemapLayer('Topographic');
    let esri_ng = L.esri.basemapLayer('NationalGeographic');
    let esri_oceans = L.esri.basemapLayer('Oceans');
    let esri_streets = L.esri.basemapLayer('Streets');
    let esri_gray = L.esri.basemapLayer('Gray');
    let esri_darkgray = L.esri.basemapLayer('DarkGray');
    let esri_imageryclarity = L.esri.basemapLayer('ImageryClarity');
    let esri_imageryfirefly = L.esri.basemapLayer('ImageryFirefly');
    let esri_shadedrelief = L.esri.basemapLayer('ShadedRelief');
    let esri_usatopo = L.esri.basemapLayer('USATopo');
    let esri_physical = L.esri.basemapLayer('Physical');
    return {
        "ESRI Imagery (No Label)": L.layerGroup([esri_imagery]).addTo(map_obj),
        "ESRI Imagery (Labeled)": L.layerGroup([esri_imagery, esri_labels]),
        "ESRI Terrain": L.layerGroup([esri_terrain]),
        "ESRI Topographic": L.layerGroup([esri_topo]),
        "ESRI NationalGeographic": L.layerGroup([esri_ng]),
        "ESRI Oceans": L.layerGroup([esri_oceans]),
        "ESRI Streets": L.layerGroup([esri_streets]),
        "ESRI Gray": L.layerGroup([esri_gray]),
        "ESRI DarkGray": L.layerGroup([esri_darkgray]),
        "ESRI ImageryClarity": L.layerGroup([esri_imageryclarity]),
        "ESRI ImageryFirefly": L.layerGroup([esri_imageryfirefly]),
        "ESRI ShadedRelief": L.layerGroup([esri_shadedrelief]),
        "ESRI USATopo": L.layerGroup([esri_usatopo]),
        "ESRI Physical": L.layerGroup([esri_physical]),
    }
}

function newWMS() {
    // let layer = $("#variables").val();
    let layer = "S1_SWE";
    let wmsurl = threddsbase + '2020_watermask/merged_2.nc4';
    let cs_rng = "0,1";
    if ($("#use_csrange").is(":checked")) {
        cs_rng = String($("#cs_min").val()) + ',' + String($("#cs_max").val())
    }

    let wmsLayer = L.tileLayer.wms(wmsurl, {
        layers: layer,
        dimension: 'time',
        useCache: true,
        crossOrigin: false,
        format: 'image/png',
        transparent: true,
        opacity: $("#opacity_raster").val(),
        BGCOLOR: '0x000000',
        styles: 'boxfill/water_mask',
        // styles: 'boxfill/' + $('#colorscheme').val(),
        colorscalerange: cs_rng,
    });

    return L.timeDimension.layer.wms(wmsLayer, {
        name: 'time',
        requestTimefromCapabilities: true,
        updateTimeDimension: true,
        updateTimeDimensionMode: 'replace',
        cache: 20,
    }).addTo(map_obj);
}

////////////////////////////////////////////////////////////////////////  LEGEND AND LATLON CONTROLS
let legend = L.control({position: 'bottomright'});
legend.onAdd = function () {
    let layer = "S1_SWE";
    let wmsurl = threddsbase + "2020_watermask/merged_2.nc4";
    let style = "water_mask";
    let cs_rng = "0,1";

    let div = L.DomUtil.create('div', 'legend');
    let url = wmsurl + "?REQUEST=GetLegendGraphic&LAYER=" + layer + "&PALETTE=" + style + "&COLORSCALERANGE=" + cs_rng;
    div.innerHTML = '<img src="' + url + '" alt="legend" style="width:100%; float:right;">';
    return div
};

///////////////////////////////////////////////////////////////////////// LAT/LONG DISPLAY
let latlon = L.control({position: 'bottomleft'});
latlon.onAdd = function () {
    let div = L.DomUtil.create('div', 'well well-sm');
    div.innerHTML = '<div id="mouse-position" style="text-align: center"></div>';
    return div;
};

////////////////////////////////////////////////////////////////////////  MAP CONTROLS AND CLEARING
// the layers box on the top right of the map
function makeControls() {
    return L.control.layers(my_basemaps, {
        'HydroSAR Layer': wms_obj,
        // 'Drawing on Map': drawnItems,
        // 'Region Boundaries': layerRegion,
    }).addTo(map_obj);
}
// you need to remove layers when you make changes so duplicates dont persist and accumulate
function clearMap() {
    controlsObj.removeLayer(layerWMS);
    map_obj.removeLayer(layerWMS);
    // controlsObj.removeLayer(layerRegion);
    map_obj.removeControl(controlsObj);
}