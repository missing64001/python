
var time_interval = 3000

window.onload=function(){
    var list = document.getElementsByClassName('asks');

    for (var i=0;i<list.length;i++) {
    list[i].scrollTop = list[i].scrollHeight; 
    }
    // console.log('test');
    setTimeout(ajax_get,time_interval)
    // setInterval
}



function ajax_get(){
    // console.log('test');
    // if (is_ajax_run){
    //     console.log('wait');
    //     return;
    // }
    // is_ajax_run = true;
    var title = $($("ul.trades")[0]).attr('id')
    var symbol = title.split("_")[1] + "_" + title.split("_")[2] 
    $.ajax({
        type: 'get',
        url: '/ajax_get/'+ symbol,
        dataType: "json",
        success: function(json){
            // console.log(json['data']);
            set_data(json);
            setTimeout(ajax_get,time_interval);
        },
        error: function(data){
            console.log("error...");
            // is_ajax_run = false;
            setTimeout(ajax_get,time_interval);
        }
    });

}

function set_data(json){
    var date = json['date']
    var data = json['data']
    for(var key in data){
        var keyl = key.split(' ')
        var exchange = keyl[0]
        var symbol = keyl[1]
        var type = keyl[2]
        
        var $ex = $('#'+exchange+'_'+symbol + '.' + type)
        $ex.html('')
        // console.log(data[key].length)
        if (type == 'asks'){
            for(var i=0;i<data[key].length;i++){
                var $li = $('<li><span class="s1">'+data[key][i][0]+'</span><span class="s1">'+data[key][i][1]+'</span></li>')
                $ex.append($li)
            }
            $ex[0].scrollTop = $ex[0].scrollHeight
            $ex.prev().html(exchange +' '+symbol +'<span class="right" date='+date+'></span>')
        }

        else if (type == 'bids'){
            for(var i=0;i<data[key].length;i++){
                var $li = $('<li><span class="s1">'+data[key][i][0]+'</span><span class="s1">'+data[key][i][1]+'</span></li>')
                $ex.append($li)
            }
        }

        else if (type == 'trades'){
            for(var i=0;i<data[key].length;i++){
                var $li = $(
                '<li style="color: '+data[key][i][3]+';">\
                    <span class="s1">'+data[key][i][0]+'</span>\
                    <span class="s1">'+data[key][i][1]+'</span>\
                    <span class="s2">'+data[key][i][2]+'</span>\
                    <span class="s3">'+data[key][i][4]+'</span>\
                </li>')
                $ex.append($li)
            }
            $ex.prev().html('trades<span class="right" date='+date+'></span>')

        }


        // var $e = $ex()
        // console.log('#'+exchange+'_'+symbol);
        // console.log($e);


        // console.log($('#xx_xx'))
        // $e.text('sdfdf')

    }

    var timestamp = Date.parse(new Date())/1000
    var $time = $('.right')
    for(var i=0;i<$time.length;i++){
        $($time[i]).text(        timestamp-$time.attr('date')   +"秒前"     )
    }
    
}