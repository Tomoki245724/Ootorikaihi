import { makeMap } from "./map_utils.js";

$(function() {
    var map = makeMap();

    var marker = L.marker();
    map.on("click", function(e) {
        var lat = e.latlng.lat;
        var lng = e.latlng.lng;
        $("#latitude").val(lat);
        $("#longitude").val(lng);
        if (marker) {
            marker.remove(map);
        }
        marker = L.marker(e.latlng).addTo(map);
    });
});
