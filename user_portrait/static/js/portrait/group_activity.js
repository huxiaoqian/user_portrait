function Draw_activity(){
    var data_x_=['周一','周二','周三','周四','周五','周六','周日'];
    // Draw_top_location(data);
    // Draw_top_platform(data);
    // Draw_more_top_location(data);
    // Draw_more_top_platform(data);
    // active_geo(data);
    // data_x = [];
    // data_y = [];
    // for (var i = 0; i < data['1'].length; i++) {
    //     var s = i.toString();
    //     value_x = new Date(parseInt(data['1'][s]['0'])*1000).format("MM-dd hh:mm");
    //     value_y = data['1'][s]['1'];
    //     data_x.push(value_x);
    //     data_y.push(value_y);
    //    }
    $('#line').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '微博时间走势图',
            x: -20 //center
        },
        subtitle: {
            text: '',
            x: -20
        },
    lang: {
            printChart: "打印",
            downloadJPEG: "下载JPEG 图片",
            downloadPDF: "下载PDF文档",
            downloadPNG: "下载PNG 图片",
            downloadSVG: "下载SVG 矢量图",
            exportButtonTitle: "导出图片"
        },
        xAxis: {
            //categories: data_x,
            categories: data_x_,
            labels:{
              rotation: 0,
              step: 6,
              y:25
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: '微博总量 (条)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        plotOptions:{
            series:{            
                cursor:'pointer',
                events:{
                    click:function(event){
                        console.log(event.point.x)
                        draw_content(data_x_[event.point.x]);
                    }
                }
            }
        },
        tooltip: {
            valueSuffix: '条',
            xDateFormat: '%Y-%m-%d %H:%M:%S'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name:'微博量',
            data: [11, 11, 15, 13, 12, 13, 10]
        }]
    });
}

function draw_content(data){
    //console.log(data);
    var html = '';
    $('#line_content').empty();
    if(data==''){
        html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
    }else{
        for(i=0;i<data.length;i++){
            html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i]+"</span></div>";
        }

    }
    $('#line_content').append(html);
}
function show_online_time(data){
    $('#online_time_table').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:100%;font-size:14px">';
    html += '<tr><th style="text-align:center">00:00 - 04:00</th>';
    html += '<th style="text-align:center">04:00 - 08:00</th>';
    html += '<th style="text-align:center">08:00 - 12:00</th>';
    html += '<th style="text-align:center">12:00 - 16:00</th>';
    html += '<th style="text-align:center">16:00 - 20:00</th>';
    html += '<th style="text-align:center">20:00 - 24:00</th></tr>';
    html += '<tr>'
    for (var i = 0; i < data.length; i++) {
       html += '<th style="text-align:center">' + data[i] + '</th>';
    };
    html += '</tr></table>'; 
    $('#online_time_table').append(html);

}

// var activity_data = []
var time_data = [23,3,4,55,22,6]
Draw_activity();
show_online_time(time_data);