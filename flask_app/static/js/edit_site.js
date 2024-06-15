import { makeMap } from "./map_utils.js";

function makeMapAndOneMarker() {
    var dataUrl = `/data/${site_id}`;
    var [map, marker] = [0, 0]

    $.ajaxSetup({async: false});

    $.getJSON(dataUrl, function(site) {
        var coordinates = site[0].coordinates;
        if (coordinates) {
            var [lat, lng] = coordinates.split(",").map(parseFloat);

            map = makeMap([lat, lng]);
            
            marker = L.marker([lat, lng]).addTo(map);
        }
    });

    return [map, marker, site.categoryid];
}

$(function() {
    var [map, marker, categoryid] = makeMapAndOneMarker();

    map.on("click", function(e) {
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;
        $("#latitude").val(lat);
        $("#longitude").val(lng);
        if (marker) {
            marker.remove(map);
        }
    });
});
