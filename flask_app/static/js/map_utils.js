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

export { makeMap };