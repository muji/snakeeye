
var baseURL = 'http://192.168.100.11:10000/';

function onClick(action,event){
    switch (action) {
        case "PLAY":
            onPlay();
        break;

        case "SNAP":
            onSnap();
        break;

        case "RECORD":

            if($("#btnRecording").hasClass("recording")) {

                $("#btnRecording").removeClass("blink_me");
                $("#btnRecording").removeClass("recording");
                onRecordStop();

            } else {

                var recordingName = Math.random() + ".mp4";
                var description = "Lorem Ipsam";

                $("#btnRecording").addClass("blink_me");
                $("#btnRecording").addClass("recording");
                onRecordStart();

             }
        break;

        default:
            break;
    }
}

function onPlay() {
 
    window.alert("onPlay called");
    var endpoint = baseURL + "play";
    apiCall(endpoint);
}

function onSnap() {
    

    const Http = new XMLHttpRequest();
    const url='http://0.0.0.0:10000/snap';
    Http.open("POST", url);
    Http.send();

Http.onreadystatechange = (e) => {
  console.log(Http.responseText)
}
    //var endpoint = baseURL + "snap";
  //  apiCall(endpoint);
    
}

function getFileName() {
    var nowMilli = Date.now();
    return "utzo" + nowMilli + "." +"mp4" ;
}


function onRecordStart() {
    
    let fName=getFileName()
    //window.alert("onRecordStart called"+fName);
    let file = prompt("Please enter file name", "");
    let descp = prompt("Please enter descp", "");
    if (file.trim().length > 0 && descp.trim().length > 0) {
                    const Http = new XMLHttpRequest();
                    const url='http://0.0.0.0:10000/start_record/{det}?fname='+fName+'&fdes=sample';
                    Http.open("POST", url);
                    Http.send();
                    Http.onreadystatechange = (e) => {
                        console.log(Http.responseText)
                    }
    }
    else
    window.alert("Nothig  called");
}

function onRecordStop() {
    var endpoint = baseURL + "stop_recording";
    apiCall(endpoint, "RECORD");
}

function apiCall(endpoint, action) {

    $("#loader").addClass("loading");
    $.post( endpoint , function() {
        $("#loader").removeClass("loading");
    })
    .fail(function() {
        $("#loader").removeClass("loading");
        if(action == "RECORD") {
            $("#btnRecording").removeClass("blink_me");
            $("#btnRecording").removeClass("recording");
        }
    })
}