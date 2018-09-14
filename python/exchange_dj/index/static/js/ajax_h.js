

var is_ajax_run = false


window.onload=function(){
    var list = document.getElementsByClassName('asks');

    for (var i=0;i<list.length;i++) {
    list[i].scrollTop = list[i].scrollHeight; 
    }
    console.log('test');
    setTimeout(ajax_get,5000)
    // setInterval
}



function ajax_get(){
    // console.log('test');
    // if (is_ajax_run){
    //     console.log('wait');
    //     return;
    // }
    // is_ajax_run = true;

    $.ajax({
        type: 'get',
        url: 'ajax_get',
        dataType: "json",
        success: function(json){
            console.log('get data');
            // is_ajax_run = false;
            setTimeout(ajax_get,5000);
        },
        error: function(data){
            console.log("error...");
            // is_ajax_run = false;
            setTimeout(ajax_get,5000);
        }
    });

}

