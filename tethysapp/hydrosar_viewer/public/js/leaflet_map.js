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