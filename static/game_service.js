// reference: https://version.aalto.fi/gitlab/oseppala/wsd2019/blob/master/examples/example_game.html#L17
// reference: https://github.com/mishinma/wsdproject/blob/6ee8d3904a09bdfd9984e93e96720cb521deed59/community/static/community/game-service.js#L39
$(document).ready(function () {
    "use strict";
    window.addEventListener("message", function (evt) {
        switch (evt.data.messageType){
            case "SCORE":
                $.ajax({
                    method: "POST",
                    data: evt.data,
                    dataType: 'json',
                    success: update_score,
                    error: error_alert
                });
                break;
            case "SAVE":
                var data = {
                    messageType: evt.data.messageType,
                    gameState: JSON.stringify(evt.data.gameState)
                };
                $.ajax({
                    method: "POST",
                    data: data,
                    error: error_alert
                });
                break;
            case "LOAD_REQUEST":
                $.ajax({
                    method: "POST",
                    data: evt.data,
                    dataType: 'json',
                    success: load_game,
                    error: error_alert
                });
                break;
            case "SETTING":
                var options = evt.data.options;
                options.visibility = 'visible';
                $("#gameIframe").css(options);
                break;

            default:
                console.log('Message type not supported');
        }
    });
});

function error_alert(jqXHR, exception)  {
    'use strict';
    var msg = {
        "messageType": "ERROR",
        "info": jqXHR.responseText
    };
    var gameIframe = $("#gameIframe")[0];
    gameIframe.contentWindow.postMessage(msg, gameIframe.src);
}

function update_score(data) {
    'use strict';
    $("#myBestScore").text(data.myBestScore);
    $("#globalBestScore").text(data.globalBestScore);
}

function load_game(data) {
    'use strict';
     var msg = {
         "messageType": "LOAD",
         "gameState": data
     };
     var gameIframe = $("#gameIframe")[0];
     gameIframe.contentWindow.postMessage(msg, gameIframe.src);
}