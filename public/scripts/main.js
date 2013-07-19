$(function () {
    var LOADING_TEXT = "Eating...",
        SHORT_TEXT = "Feed",
        EXPAND_TEXT = "Vomit";

    var input = $("#url-input"),
        form = $("form").first(),
        submit = $("button[type=submit]");

    input.focus();

    var resetForm = function () {
        submit.removeAttr("disabled");
        replaceButtonDependsOnURL();
        input.focus().select();
    };

    var replaceButtonDependsOnURL = function () {
        var reg = new RegExp(location.protocol + "//" + location.host + "/.*");
        reg.ignoreCase = true;
        reg.global = true;
        if (reg.test(input.val())) {
            submit.text(EXPAND_TEXT);
        } else {
            submit.text(SHORT_TEXT);
        }
        if (/.+:\/\/.+/ig.test(input.val())) {
            submit.removeAttr('disabled');
        } else {
            submit.attr('disabled', 'disabled');
        }
    };
    replaceButtonDependsOnURL();

    var errorBlink = function () {
        var originalInputBg = input.css("backgroundColor");
        input.animate({background: "#ffffcc"}, 150, "ease", function() {
            input.animate({background: originalInputBg}, 200, "ease");
        });
    };

    input.on("change", replaceButtonDependsOnURL);
    input.on("keydown", replaceButtonDependsOnURL);
    input.on("keyup", replaceButtonDependsOnURL);
    input.on("paste", replaceButtonDependsOnURL);

    input.focus(function(){
        window.setTimeout(function(){
            input.select();
        }, 100);
    });

    form.on("submit", function () {
        submit.attr("disabled", "disabled").text(LOADING_TEXT);
        $.ajax({
            type: "POST",
            data: form.serialize(),
            url: form.attr("action"),
            dataType: "json",
            timeout: 300,
            success: function (data, status, xhr) {
                input.val(data.short_url ? data.short_url : data.long_url);
                resetForm();
            },
            error: function (xhr, type) {
                if (xhr.status >= 400 && xhr.status < 500) {
                    input.val('');
                }
                resetForm();
                errorBlink();
            }
        });
        return false;
    });
});