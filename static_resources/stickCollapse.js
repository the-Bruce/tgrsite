$(document).ready(function () {
    console.log("Setting up");
    let threads = $('#body-thread');
    let replies = $('#body-replies');
    threads.on("hidden.bs.collapse", function (event) {
        saveState('bodyThread', '#body-thread')
    });
    replies.on("hidden.bs.collapse", function (event) {
        saveState('bodyReplies', '#body-replies')
    });
    threads.on("shown.bs.collapse", function (event) {
        saveState('bodyThread', '#body-thread')
    });
    replies.on("shown.bs.collapse", function (event) {
        saveState('bodyReplies', '#body-replies')
    });
});

function saveState(key, id) {
    console.log($(id).attr("aria-expanded"));
    setCookie(key, $(id).attr("aria-expanded"), 365)
}

//Retreived from https://www.w3schools.com/js/js_cookies.asp 2018-10-11 by Thomas Bruce
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}