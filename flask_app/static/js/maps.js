import { makeMap } from "./map_utils.js"

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

