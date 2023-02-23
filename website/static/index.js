// document.onreadystatechange = function () {
//     var state = document.readyState
//     console.log('state change!', state)
//     if (state == 'interactive') {
//         showLoadingIndicator();
//     } else if (state == 'complete') {
//         setTimeout(function(){
//         //    document.getElementById('interactive');
//            console.log('showing contents!')
//            document.getElementById('load').style.visibility="hidden";
//            document.getElementById('contents').style.visibility="visible";
//         },1000);
//     }
// }

document.onreadystatechange = function () {
    var state = document.readyState
    if (state == 'complete') {
        setTimeout(function(){
        //    document.getElementById('interactive');
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