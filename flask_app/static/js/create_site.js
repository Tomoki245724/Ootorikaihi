import { makeMap, changeMarkerColor } from "./map_utils.js";

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
        var customIcon = L.icon({
            iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
            shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            tooltipAnchor: [16, -28],
            shadowSize: [41, 41],
            className: `icon-${ genId }`,
        });
        marker = L.marker(e.latlng, {icon: customIcon}).addTo(map)
        changeMarkerColor(genId);
    });

    $("#upload-image").on("change", function(e) {
        var file = e.target.files[0];
        console.log(file);
        var reader = new FileReader();
        reader.onload = function(f) {
            var img = new Image();
            img.src = f.target.result;
            console.log(img.src);
            img.onload = function() {
                $("#preview").attr("src", img.src);
            };
        };
        reader.readAsDataURL(file);
    })
});
