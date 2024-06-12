import { makeMap } from "./map_utils.js";

function addMarker() {
    var dataUrl = `/data/${site_id}`;
    var [map, marker] = [0, 0]

    $.ajaxSetup({async: false});

    $.getJSON(dataUrl, function(site) {
        var coordinates = site[0].coordinates;
        if (coordinates) {
            var [lat, lng] = coordinates.split(",").map(parseFloat);

            map = makeMap([lat, lng]);
            
            marker = L.marker([lat, lng]).addTo(map);
            var popup = L.popup({
                closeButton: false,
                className: "custom-popup",
            }).setContent(
                `${ site.sitename }<span>${ site.categoryname }</span>`
            );
            marker.bindPopup(popup);
        }
    });

    return [map, marker];
}

$(function() {
    var [map, marker] = addMarker();

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
