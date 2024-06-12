import { makeMap, addMarker } from "./map_utils.js"

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
                addMarker(
                    genreLayers[site.categoryid],
                    [lat, lng],
                    site.sitename,
                    site.categoryname,
                    site.categoryid,
                );
            };
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
        var color_deg = Number(key) * 50;
        $(`.icon-${ key }`).css("filter", `hue-rotate(${ color_deg }deg)`);
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
        var genreId = this.id.replace("genre", "");
        if ($(this).parent().hasClass("show")) {
            $(this).appendTo(".hide");
            map.removeLayer(genreLayers[genreId]);
        } else {
            $(this).appendTo(".show");
            map.addLayer(genreLayers[genreId]);
            var color_deg = Number(genreId) * 53;
            $(`.icon-${ genreId }`).css("filter", `hue-rotate(${ color_deg }deg)`);
        };
    });
});
