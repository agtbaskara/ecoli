$(document).ready(function () {
    $("#btn123on").click(function () {
        $.post("/changestatus", {
            plugId: "123",
            status: "on"
        })
    });

    $("#btn123off").click(function () {
        $.post("/changestatus", {
            plugId: "123",
            status: "off"
        })
    });

    $("#btn456on").click(function () {
        $.post("/changestatus", {
            plugId: "456",
            status: "on"
        })
    });

    $("#btn456off").click(function () {
        $.post("/changestatus", {
            plugId: "456",
            status: "off"
        })
    });
});