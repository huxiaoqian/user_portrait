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
            x: -20, //-20：center
            style: {
                color: '#555555',
                fontSize: '14px'
            }
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

function Draw_top_location2(){
    var myChart = echarts.init(document.getElementById('top_active_geo_line')); 
    var option = {
        timeline:{
            data:[
                '2002-01-01','2003-01-01','2004-01-01','2005-01-01','2006-01-01',
                '2007-01-01','2008-01-01','2009-01-01'
            ],
            label : {
                formatter : function(s) {
                    return s.slice(0, 4);
                }
            },
            autoPlay : true,
            playInterval : 1000
        },
        options:[
            {
                title : {
                    'text':'整体用户地理位置分布'
                },
                tooltip : {'trigger':'axis'},
                legend : {
                    x:'right',
                    'data':['GDP','金融','房地产'],
                    'selected':{
                        'GDP':true,
                        '金融':false,
                        '房地产':true
                        
                    }
                },
                toolbox : {
                    'show':false, 
                    orient : 'vertical',
                    x: 'right', 
                    y: 'center',
                    'feature':{
                        'mark':{'show':true},
                        'dataView':{'show':true,'readOnly':false},
                        'magicType':{'show':true,'type':['line','bar','stack','tiled']},
                        'restore':{'show':true},
                        'saveAsImage':{'show':true}
                    }
                },
                calculable : true,
                grid : {'y':80,'y2':100},
                xAxis : [{
                    'type':'category',
                    'axisLabel':{'interval':0},
                    'data':[
                        '北京','\n天津','河北','\n山西','内蒙古','\n辽宁','吉林','\n黑龙江',
                        '上海','\n江苏','浙江','\n安徽','福建','\n江西','山东','\n河南',
                        '湖北','\n湖南','广东','\n广西','海南','\n重庆','四川','\n贵州',
                        '云南','\n西藏','陕西','\n甘肃','青海','\n宁夏','新疆'
                    ]
                }],
                yAxis : [
                    {
                        'type':'value',
                        'name':'GDP（亿元）',
                        'max':53500
                    },
                    {
                        'type':'value',
                        'name':'其他（亿元）'
                    }
                ],
                series : [
                    {
                        'name':'GDP',
                        'type':'bar',
                        'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]
                    },
                    {
                        'name':'金融','yAxisIndex':1,'type':'bar',
                        'data':  [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]
                    },
                    {
                        'name':'房地产','yAxisIndex':1,'type':'bar',
                        'data':  [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]
                    }
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                 series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                 series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                 series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                 series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            },
            {
                title : {'text':'整体用户地理位置分布'},
                series : [
                    {'data': [120,37,44,245,34,226,34,205,54,345,234,234,134,35,546,45]},
                    {'data': [22,33,44,245,324,116,364,25,54,345,234,234,134,35,546,45]},
                    {'data': [221,30,44,245,24,46,4,25,54,345,234,234,134,35,546,45]},
                    // {'data': dataMap.dataPI['2003']},
                    // {'data': dataMap.dataSI['2003']},
                    // {'data': dataMap.dataTI['2003']}
                ]
            }
        ]
    };
    myChart.setOption(option);
                    
}

function moving_geo(){
    var data = [['北京', '上海', 100], ['北京', '1上海', 100], ['北京', '上1海', 20],['北京', '1上海', 100],  ['北京', '上海', 30]];
    $('#move_location').empty();
    var html = '';
    html += '<table class="table table-striped" style="width:100%;font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">起始地</th>';
    html += '<th style="text-align:right"></th>';
    html += '<th style="text-align:left">目的地</th>';
    html += '<th style="text-align:center">人数</th>';
    html += '</tr>';
    for (var i = 0; i < data.length; i++) {
        html += '<tr>';
        html += '<td style="text-align:center">' + data[i][0] + '</td>';
        html += '<td style="text-align:center"><img src="/../../static/img/arrow_geo.png" style="width:30px;"></td>';
        html += '<td style="text-align:left">' + data[i][1] + '</td>';
        html += '<td style="text-align:center">' + data[i][2] + '</td>';
    html += '</tr>'; 
    };
    html += '</table>'; 
    $('#move_location').append(html);
}

function Draw_more_moving_geo(){
    var data = [['北京', '上海', 100], ['北京', '1上海', 100], ['北京', '上1海', 20],['北京', '1上海', 100],  ['北京', '上海', 30]];
    $('#move_location_more_detail').empty();
    var html = '';
    html += '<table class="table table-striped " font-size:14px">';
    html += '<tr><th style="text-align:center">起始地</th>';
    html += '<th style="text-align:right"></th>';
    html += '<th style="text-align:left">目的地</th>';
    html += '<th style="text-align:center">人数</th>';
    html += '</tr>';
    for (var i = 0; i < data.length; i++) {
        html += '<tr>';
        html += '<td style="text-align:center">' + data[i][0] + '</td>';
        html += '<td style="text-align:left"><img src="/../../static/img/arrow_geo.png" style="width:30px;"></td>';
        html += '<td style="text-align:left">' + data[i][1] + '</td>';
        html += '<td style="text-align:center">' + data[i][2] + '</td>';
    html += '</tr>'; 
    };
    html += '</table>'; 
    $('#move_location_more_detail').append(html);
}

function Draw_top_platform(){
    $('#top_platform').empty();
    var html = '';
    html += '<table class="table table-striped" style="width:260px;font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">平台</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < 1; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + 'web' + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#top_platform').append(html);
}

function Draw_more_top_platform(){
    $('#top_more_platform').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">平台</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < 1; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + 'web' + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#top_more_platform').append(html);
}

function draw_active_distribution(){
    var mychart1 = echarts.init(document.getElementById('active_distribution'));
    var option = {
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            name : '人数',
            data : ['巴西','印尼','美国','印度','中国','100-200']
        }
    ],
    series : [
        {
            name:'2011年',
            type:'bar',
            data:[18203, 23489, 29034, 104970, 131744, 230230]
        }
    ]
};
  mychart1.setOption(option);
}

function show_active_users(div_name){
    $('#' + div_name).empty();
    var html = '';
    html += '<table class="table table-striped" style="font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < 1; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + 'web' + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#'+div_name).append(html);
}
function show_more_active_users(div_name){
    $('#' + div_name).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < 1; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + 'web' + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#'+div_name).append(html);
}

function group_activity(){
   var mychart = echarts.init(document.getElementById('group_activity'));
   var option = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['邮件营销','联盟广告','视频广告']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar', 'stack', 'tiled']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            boundaryGap : false,
            data : ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'邮件营销',
            type:'line',
            stack: '总量',
            data:[120, 132, 101, 134, 90, 230, 210]
        },
        {
            name:'联盟广告',
            type:'line',
            stack: '总量',
            data:[220, 182, 191, 234, 290, 330, 310]
        },
        {
            name:'视频广告',
            type:'line',
            stack: '总量',
            data:[150, 232, 201, 154, 190, 330, 410]
        }
        
    ]
};
  mychart.setOption(option);
}

// var activity_data = []
var time_data = [23,3,4,55,22,6]
Draw_activity();
show_online_time(time_data);
Draw_top_location2();
moving_geo();
Draw_more_moving_geo();
Draw_top_platform();
Draw_more_top_platform();
draw_active_distribution();
group_activity();
show_active_users('active_users');
show_active_users('unactive_users');
show_more_active_users('show_rank_active_users');
show_more_active_users('show_rank_unactive_users');
$('#activity_conclusion').append('结论结论结论结论');
