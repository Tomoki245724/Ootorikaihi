function makeMap(center=[36.105446527684215, 140.10174633069715]) {
    var map = L.map('map',
    {
        center: center,
        zoom: 15,
        zoomControl: false
    });

    // タイル選択
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    // Zoomボタン
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);

    // 移動制限
    const southWest = L.latLng(36.054055080143236, 140.0320789791267);
    const northEast = L.latLng(36.14511141462569, 140.18986633469459);
    const bounds = L.latLngBounds(southWest, northEast);
    map.setMaxBounds(bounds);

    return map;
}

function addMarker(addTo, latLng, sitename, siteid, categoryname, categoryid) {
    var customIcon = L.icon({
        iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        tooltipAnchor: [16, -28],
        shadowSize: [41, 41],
        className: `icon-${ categoryid }`,
    });
    var coordinates = latLng[0].toString() + "," + latLng[1].toString();
    var marker = L.marker(latLng, {icon: customIcon}).addTo(addTo);
    var popup = L.popup({
        closeButton: false,
        className: "custom-popup",
    }).setContent(
        `<span>${ categoryname }</span><a href="../site/${siteid}">${ sitename }</a>
        <a class="to-googlemaps" href="https://www.google.co.jp/maps/place/${coordinates}">GoogleMapsへ</a>`
    );
    marker.bindPopup(popup);
}

function makeMapAndOneMarker(siteData) {
    var coordinates = siteData[0].coordinates;
    if (coordinates) {
        var [lat, lng] = coordinates.split(",").map(parseFloat);

        var map = makeMap([lat, lng]);
        
        var customIcon = L.icon({
            iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
            shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            tooltipAnchor: [16, -28],
            shadowSize: [41, 41],
            className: `icon-${ siteData[0].categoryid }`,
        });
        var marker = L.marker([lat, lng], {icon: customIcon}).addTo(map);

        return [map, marker];
    }
}

function changeMarkerColor(genreId) {
    var color_deg = Number(genreId) * 53;
    $(`.icon-${ genreId }`).css("filter", `hue-rotate(${ color_deg }deg)`);
}

export { makeMap, addMarker, makeMapAndOneMarker, changeMarkerColor };
