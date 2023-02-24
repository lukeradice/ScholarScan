document.onreadystatechange = function () {
    var state = document.readyState
    if (state == 'complete') {
        setTimeout(function(){
           console.log('showing contents!')
           document.getElementById('load').style.visibility="hidden";
           document.getElementById('contents').style.visibility="visible";
        },1000);
    }
}

function showLoadingIndicator() {
    console.log('STATE CHANGE!')
    document.getElementById('load').style.visibility="visible";
    document.getElementById('contents').style.visibility="hidden";
}