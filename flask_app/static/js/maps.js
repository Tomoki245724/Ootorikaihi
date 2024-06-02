function makeMap() {
    var map = L.map('map',
    {
        center: [36.105446527684215, 140.10174633069715], // 学生会館
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

function renderData(map) {
    var dataUrl = "/data"; // jsonデータのあるエンドポイント
    var genresDataUrl = "/genres_data"

    // const layerControl = L.control.layers().addTo(map);
    var genreLayers = {};

    $.ajaxSetup({async: false});

    $.getJSON(genresDataUrl, function(genres) {
        genres.forEach(genre => {
            genreLayers[genre.genid] = L.layerGroup();
            // layerControl.addOverlay(genreLayers[genre.genid], genre.genname);
        });
    });

    $.getJSON(dataUrl, function(data) {
        data.forEach(site => {
            var coordinates = site.coordinates;
            if (coordinates) {
                var [lat, lng] = coordinates.split(",").map(parseFloat);
                var marker = L.marker([lat, lng]).addTo(genreLayers[site.categoryid]);
                var popup = L.popup({
                    closeButton: false,
                    className: "custom-popup",
                }).setContent(
                    `${ site.sitename }<span>${ site.categoryname }</span>`
                );
                marker.bindPopup(popup);
            }
        });
    });

    return genreLayers;
}

$(function() {
    var map = makeMap();
    var genreLayers = renderData(map);

    // レイヤーを全て表示させる
    Object.keys(genreLayers).forEach(key => {
        map.addLayer(genreLayers[key]);
    });

    // サイドバーの開閉
    $(".open-btn").click(function() {
        $(".sidebar").css("display", "block")
        $(".open-btn").css("display", "none")
    });
    $(".close-btn").click(function() {
        $(".sidebar").css("display", "none")
        $(".open-btn").css("display", "block")
    });

    // レイヤーの表示非表示
    $(".genre").click(function() {
        console.log(`${this.id}`);
        var genreId = this.id.replace("genre", "");
        if ($(this).parent().hasClass("show")) {
            $(this).appendTo(".hide");
            map.removeLayer(genreLayers[genreId]);
        } else {
            $(this).appendTo(".show");
            map.addLayer(genreLayers[genreId]);
        };
    });
});
