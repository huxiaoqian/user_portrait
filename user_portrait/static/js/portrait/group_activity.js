ajax_method = 'GET';
function call_sync_ajax_request(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: true,
      success:callback
    });
}
function Draw_activity(data){
	var data_x_ = [];
	var data_y_ = [];

	for(var i=0;i<data.length;i++){
		var time_line  = new Date(parseInt(data[i][0])*1000).format("yyyy-MM-dd");
		data_x_.push(time_line);
		data_y_.push(data[i][1]);

	}

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
                        console.log('传递的是',data_x_[event.point.x]);
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
        	enabled: false,
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            borderWidth: 0
        },
        series: [{
            name:'微博量',
            data: data_y_
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

function Draw_top_location(data){
	var timeline_data = [];
	var bar_data = [];
	var bar_data_x = [];
	var bar_data_y = [];
	for(var key in data){
		var key_time = new Date(parseInt(key)*1000).format("yyyy-MM-dd");
		timeline_data.push(key_time);
		bar_data.push(data[key]);
	}
	for(var i=0;i<bar_data.length;i++){
		var bar_data_x_single = [];
		var bar_data_y_single = [];
		for(var key in bar_data[i]){
			bar_data_x_single.push(key);
			bar_data_y_single.push(bar_data[i][key]);
		}
		bar_data_x.push(bar_data_x_single);
		bar_data_y.push(bar_data_y_single);
	}
	// console.log(bar_data_y);
	
		//console.log(timeline_data);
    var myChart = echarts.init(document.getElementById('top_active_geo_line')); 
    var option = {
        timeline:{
            data:timeline_data,
            // label : {
            //     formatter : function(s) {
            //         return s.slice(0, 4);
            //     }
            // },
            autoPlay : true,
            playInterval : 1000
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
        options : (function () {
        	var option_data = [];
        	for(var i=0;i<timeline_data.length;i++){
        		var option_single_data = {};

        		option_single_data.title={'text': '整体用户地理位置分布' };
        		option_single_data.tooltip ={'trigger':'axis'};
        		option_single_data.calculable = true;
                option_single_data.grid = {'y':80,'y2':100};
                option_single_data.xAxis = [{
                    'type':'category',
                    'axisLabel':{'interval':0},
                    'data':bar_data_x[i]
                }];
                option_single_data.yAxis = [
                    {
                        'type':'value',
                        'name':'次数',
                        //'max':53500
                    }
                ];
                option_single_data.series = [
                    {
                        'name':'活跃次数',
                        'type':'bar',
                        'data': bar_data_y[i]
                    },

                ];
                option_data.push(option_single_data);
        	};
        	// console.log(option_data);
        	return option_data;
        }
        )()
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

function draw_active_distribution(data){
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
            data : data[1]
        }
    ],
    series : [
        {
            name:'2011年',
            type:'bar',
            data:data[0]
        }
    ]
};
  mychart1.setOption(option);
}

function show_active_users(data, div_name){
	// console.log(data[1])
	if(data.length<5){
		var show_count = data.length;
	} else{
		show_count = 5
	};
    $('#' + div_name).empty();
    var html = '';
    html += '<table class="table table-striped" style="font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < show_count; i++) {
        var name_list = data[i][0].split('&');
        var name = name_list[1];
        var s = i.toString();
        var m = i + 1;
        html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + name + '</th><th style="text-align:center">'+data[i][1] + '</th></tr>';
    };
    html += '</table>'; 
    $('#'+div_name).append(html);
}
function show_more_active_users(data, div_name){
    $('#' + div_name).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data.length; i++) {
    	var name_list = data[i][0].split('&');
        var name = name_list[1];
        var s = i.toString();
        var m = i + 1;
        html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + name + '</th><th style="text-align:center">'+data[i][1] + '</th></tr>';
    };
    html += '</table>'; 
    $('#'+div_name).append(html);
}

function group_activity(data){

	//活跃非活跃用户
	var main_active = data.main_max;
	var main_unactive = data.main_min;
	show_active_users(main_active, 'active_users');
	show_active_users(main_unactive, 'unactive_users');
	//show_more_active_users(main_active, 'show_rank_active_users');
	//show_more_active_users(main_unactive, 'show_rank_unactive_users');

	//折线图
	//var legend_data = []
	var xAxis_data = data.time_list;
	var yAxis_ave = data.ave_list;
	var max_list = data.max_list;
	var yAxis_max = [];
	for(var i=0; i<max_list.length;i++){
		yAxis_max.push(max_list[i][1])

	};
	var min_list = data.min_list;
	var yAxis_min = [];
	for(var i=0; i<min_list.length;i++){
		yAxis_min.push(min_list[i][1])

	};

   var mychart = echarts.init(document.getElementById('group_activity'));
   var option = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['最高值','最低值','平均值']
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
            data : xAxis_data
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'最高值',
            type:'line',
            stack: '总量',
            data:yAxis_max
        },
        {
            name:'最低值',
            type:'line',
            stack: '总量',
            data:yAxis_min
        },
        {
            name:'平均值',
            type:'line',
            stack: '总量',
            data:yAxis_ave
        }
        
    ]
};
  mychart.setOption(option);
}

function show_activity(data) {
	var time_data = [23,3,4,55,22,6]
	//微博走势，点击后显示微博
	Draw_activity(data.activity_trend);

	show_online_time(time_data);

	//活跃地区分布
	Draw_top_location(data.activity_geo_disribution);
	
	moving_geo();
	Draw_more_moving_geo();
	Draw_top_platform();
	Draw_more_top_platform();

	draw_active_distribution(data.activeness_his);

	group_activity(data.activeness_trend);

	$('#activity_conclusion').append(data.activeness_description);
	// body...
}


var group_activity_url = 'http://219.224.134.213:9040/group/show_group_result/?module=activity&task_name=媒体';
call_sync_ajax_request(group_activity_url,ajax_method, show_activity)
// var activity_data = []

