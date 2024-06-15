import { makeMapAndOneMarker, changeMarkerColor } from "./map_utils.js";

$(function() {
    var dataUrl = `/data/${site_id}`;

    $.ajaxSetup({async: false});

    $.getJSON(dataUrl, function(site) {
        var siteData = site;
        var [map, marker] = makeMapAndOneMarker(site);
        var genId = site[0].categoryid;
        changeMarkerColor(genId);
    });
});
