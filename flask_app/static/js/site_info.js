import { makeMap } from "./map_utils.js";

function makeMapAndOneMarker() {
    var dataUrl = `/data/${site_id}`;

    $.ajaxSetup({async: false});

    $.getJSON(dataUrl, function(site) {
        var coordinates = site[0].coordinates;
        if (coordinates) {
            var [lat, lng] = coordinates.split(",").map(parseFloat);

            var map = makeMap([lat, lng]);
            
            var marker = L.marker([lat, lng]).addTo(map);

            return [lat, lng];
        }
    });

}

$(function() {
    makeMapAndOneMarker();
});
