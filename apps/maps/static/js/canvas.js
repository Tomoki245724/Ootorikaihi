$(function() {

    $map = $(".map-container");
    $pins = $(".pins");

    // ドラッグでスクロール
    var isDragging = false;
    var startX, startY;
    var scrollLeft, scrollTop;

    $map.mousedown(function(e) {
        isDragging = true;
        startX = e.pageX
        startY = e.pageY
        scrollLeft = $(window).scrollLeft();
        scrollTop = $(window).scrollTop();
    }).mousemove(function(e) {
        if (isDragging) {
            e.preventDefault();
            var movedX = e.pageX
            var movedY = e.pageY
            var dx = movedX - startX;
            var dy = movedY - startY;
            $(window).scrollLeft(scrollLeft - dx);
            $(window).scrollTop(scrollTop - dy);
        }
    }).mouseup(function() {
        isDragging = false;
    });

    $(document).mouseup(function() {
        isDragging = false;
    });

    // 拡大・縮小
    var scale = parseFloat($map.css("zoom"));
    $(".scale").text(scale);

    function updatePinsScale() {
        $pins.find("span").each(function() {
            $(this).css("transform", `scale(${1 / scale})`);
        });
    }

    $(".zoomin").click(function() {
        scale += 0.1;
        $(".scale").text(scale);
        $map.css("zoom", scale);
        updatePinsScale();
    });
    $(".zoomout").click(function() {
        if (scale > 0.2) {
            scale -= 0.1;
            $(".scale").text(scale);
            $map.css("zoom", scale);
            updatePinsScale();
        }
    });

    // ピン？を指す
    var x, y;
    var pinId = 0;
    $map.contextmenu(function(e) {
        x = e.offsetX / scale;
        y = e.offsetY / scale;
        $(".coordinates").show().text(x +", "+ y);
        var pinHtml = `<span class="material-symbols-outlined pin-${pinId.toString()}">location_on</span>`;
        $pins.append(pinHtml);
        var $newPin = $(`.pin-${pinId}`);
        $newPin.css({
            position: "absolute",
            top: `${y - $newPin.height()}px`,
            left: `${x - $newPin.width() / 2}px`,
            transform: `scale(${1 / scale})`
        });
        pinId += 1;
        return false; // デフォルトのメニュー非表示
    })
});
