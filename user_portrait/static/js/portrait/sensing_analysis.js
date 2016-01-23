var data=[['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称1','法律机构及人士','民生类_社会保障','234',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称3','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称4','','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称5','话题2','法律机构及人士','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称2','话题2','领域domain','24',23,56],
			['http://tp2.sinaimg.cn/2127129797/50/40016674706/0','昵称3','话题3','领域domain','34',23,56]]
var keywords=[['关键词1', 7],['关键词2', 6],['关键词2', 6],['关键词2', 6],['关键词2', 6],['关键词', 8],['关键词', 34],['关键词', 76],['关键词', 32],['关键词', 23],
				['关键词1', 7],['关键词2', 6],['关键词2', 6],['关键词2', 6],['关键词2', 6],['关键词', 8],['关键词', 34],['关键词', 76],['关键词', 32],['关键词', 23],
				['关键词1', 7],['关键词2', 6],['关键词2', 6],['关键词2', 6],['关键词2', 6],['关键词', 8],['关键词', 34],['关键词', 76],['关键词', 32],['关键词', 23]]
var sensor_head=['序号','头像','昵称','领域','话题','影响力','重要度','活跃度']
var sensor2_head=['头像','昵称','领域','话题','热度','影响力','重要度','活跃度']
var keywords_head=['序号','关键词','频数']


function sensing_sensors_table (head, data, div_name) {
    $('#'+div_name).empty();
	if(data.length>7){
		$('#'+div_name).css("overflow-y", "auto");
	}
	var html = '';
	html += '<table id="" class="table table-bordered table-striped table-condensed datatable">';
	html += '<thead><tr>';
	for(var i=0; i<head.length; i++){
	html += '<th style="text-align:center">'+head[i]+'</th>';

	}
	html += '</tr></thead>';
	html += '<tbody>';

	for(var i=0; i<data.length; i++){
		var s= i+1;
		html += '<tr>';
		html += '<td style="text-align:center;vertical-align:middle;">' + s + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + '<img src="'+data[i][0] +'" class="small-photo shadow-5" title="' + data[i][1] +'">' + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][1] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][2] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][3] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][4] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 10 + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 16 + '</td>';
		html += '</tr>';
	}
	html += '</tbody></table>';
	$('#'+div_name).append(html);
}

function sensing_participate_table (head, data, div_name) {
    $('#'+div_name).empty();
	// if(data.length>7){
	// 	$('#'+div_name).css("overflow-y", "auto");
	// }
	var html = '';
	html += '<table id="participate_table" class="table table-bordered table-striped table-condensed datatable">';
	html += '<thead><tr>';
	for(var i=0; i<head.length; i++){
	html += '<th style="text-align:center">'+head[i]+'</th>';
	}
	html += '<th style="text-align:center"> <input name="participate_select_all" id="participate_select_all" type="checkbox" value="" onclick="participate_select_all()" /></th>';
	html += '</tr></thead>';
	html += '<tbody>';

	for(var i=0; i<data.length; i++){
		var s= i+1;
		html += '<tr>';
		// html += '<td style="text-align:center;vertical-align:middle;">' + s + '234567890</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + '<img src="'+data[i][0] +'" class="small-photo shadow-5" title="' + data[i][1] +'">' + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][1] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][2] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][3] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][4] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][5] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 10 + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + 16 + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + '<input name="participate_select" type="checkbox" id="participate_select" value ="'+data[i][1]+'">' + '</td>';
		html += '</tr>';
	}
	html += '</tbody></table>';
	$('#'+div_name).append(html);
	$('#participate_table').dataTable({
        	"sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",

        	"sPaginationType": "custom_bootstrap",
        	"aoColumnDefs":[ {"bSortable": false, "aTargets":[8]}, {"bAutoWidth": true, "aTargets":["_all"]}],
        	// "bAutoWidth": true,
        	"oLanguage": {

            	"sLengthMenu": "_MENU_ 每页"

        }

    });
}

function sensing_keywords_table (head, data, div_name) {
    $('#'+div_name).empty();
	if(data.length>10){
		$('#'+div_name).css("overflow-y", "auto");
	}
	var html = '';
	html += '<table id="keywords_table" class="table table-bordered table-striped table-condensed datatable">';
	html += '<thead><tr>';
	for(var i=0; i<head.length; i++){
	html += '<th style="text-align:center">'+head[i]+'</th>';
	}
	//html += '<th style="text-align:center"> <input name="participate_select_all" id="participate_select_all" type="checkbox" value="" onclick="participate_select_all()" /></th>';
	html += '</tr></thead>';
	html += '<tbody>';

	for(var i=0; i<data.length; i++){
		var s= i+1;
		html += '<tr>';
		html += '<td style="text-align:center;vertical-align:middle;">' + s + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][0] + '</td>';
		html += '<td style="text-align:center;vertical-align:middle;">' + data[i][1] + '</td>';
	}
	html += '</tbody></table>';
	$('#'+div_name).append(html);
	// $('#keywords_table').dataTable({
 //        	"sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",

 //        	"sPaginationType": "bootstrap",
 //        	"aoColumnDefs":[ {"bSortable": false, "aTargets":[8]}, {"bAutoWidth": true, "aTargets":["_all"]}],
 //        	// "bAutoWidth": true,
 //        	"oLanguage": {

 //            	"sLengthMenu": "_MENU_ 每页"

 //        }

 //    });
}

function draw_line_charts(div_name){
	var myChart = echarts.init(document.getElementById(div_name)); 
	option = {  
	    tooltip : {
	        trigger: 'item',
	        formatter : function (params) {
	            var date = new Date(params.value[0]);
	            data = date.getFullYear() + '-'
	                   + (date.getMonth() + 1) + '-'
	                   + date.getDate() + ' '
	                   + date.getHours() + ':'
	                   + date.getMinutes();
	            return data + '<br/>'
	                   + params.value[1] + ', ' 
	                   + params.value[2];
	        }
	    },
	    toolbox: {
	        show : false,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    dataZoom: {
	        show: true,
	        start : 90
	    },
	    legend : {
	        data : ['series1', 'series2', 'series3', 'series4'],
	        x:'right'
	    },
	    grid: {
	        y2: 80
	    },
	    xAxis : [
	        {
	            type : 'time',
	            splitNumber:10
	        }
	    ],
	    yAxis : [
	        {
	            type : 'value'
	        }
	    ],
	    series : [
	        {
	            name: 'series1',
	            type: 'line',
	            showAllSymbol: true,
	            symbolSize: function (value){
	                return Math.round(value[2]/200) + 2;
	            },
	            clickable: true,
	          
	            data: (function () {
	                var d = [];
	                var len = 0;
	                var now = new Date();
	                var value;
	                while (len++ < 200) {
	                    d.push([
	                        new Date(2014, 9, 1, 0, len * 10000),
	                        (Math.random()*30).toFixed(2) - 0,
	                        (Math.random()*100).toFixed(2) - 0
	                    ]);
	                }
	                return d;
	            })()
	        },
	        {
	            name: 'series2',
	            type: 'line',
	            showAllSymbol: false,
	            
	          
	            data: (function () {
	                var d = [];
	                var len = 0;
	                var now = new Date();
	                var value;
	                while (len++ < 200) {
	                    d.push([
	                        new Date(2014, 9, 1, 0, len * 10000),
	                        (Math.random()*30).toFixed(2) - 0,
	                        (Math.random()*100).toFixed(2) - 0
	                    ]);
	                }
	                return d;
	            })()
	        },
	        {
	            name: 'series3',
	            type: 'line',
	            showAllSymbol: false,
	            
	          
	            data: (function () {
	                var d = [];
	                var len = 0;
	                var now = new Date();
	                var value;
	                while (len++ < 200) {
	                    d.push([
	                        new Date(2014, 9, 1, 0, len * 10000),
	                        (Math.random()*30).toFixed(2) - 0,
	                        (Math.random()*100).toFixed(2) - 0
	                    ]);
	                }
	                return d;
	            })()
	        },
	        {
	            name: 'series4',
	            type: 'line',
	            showAllSymbol: false,
	            
	          
	            data: (function () {
	                var d = [];
	                var len = 0;
	                var now = new Date();
	                var value;
	                while (len++ < 200) {
	                    d.push([
	                        new Date(2014, 9, 1, 0, len * 10000),
	                        (Math.random()*30).toFixed(2) - 0,
	                        (Math.random()*100).toFixed(2) - 0
	                    ]);
	                }
	                return d;
	            })()
	        }
	    ]
	};
	 require([
            'echarts'
        ],
        function(ec){
			var ecConfig = require('echarts/config');
			function eConsole(param) {
				alert('aaa');
			    var mes = '【' + param.type + '】';
			    // if (typeof param.seriesIndex != 'undefined') {
			    //     mes += '  seriesIndex : ' + param.seriesIndex;
			    //     mes += '  dataIndex : ' + param.dataIndex;
			    // }
			    var click_time = param.value[0].format('yyyy-MM-dd hh:mm');
			    var data=[['0',1,2,'3neirong',4,click_time,6,7,8,9,0],['0',1,2,'3neirong',4,click_time,6,7,8,9,0],['0',1,2,'3neirong',4,5,6,7,8,9,0],['0',1,2,'3neirong',4,5,6,7,8,9,0]]
			    Draw_get_weibo(data, 'related_weibo_text');
			    //testit();
			    // if (param.type == 'hover') {
			    //     document.getElementById('hover-console').innerHTML = 'Event Console : ' + mes;
			    // }
			    // else {
			    //     document.getElementById('console').innerHTML = mes;
			    // }
			    console.log('mes', mes)
			    console.log(0);
			}
		
		myChart.on(ecConfig.EVENT.CLICK, eConsole);
	});

	// 为echarts对象加载数据 
    myChart.setOption(option);                  
}

function Draw_get_weibo(data,div_name){
  var html = '';
  $('#'+div_name).empty();
    if(data[0][3]==''){
        html += "<div style='width:100%;height:100px;'>用户在昨天未发布任何微博</div>";
    }else{
      html += '<div id="weibo_list" class="weibo_list weibo_list_height scrolls tang-scrollpanel" style="margin:0;">';
      html += '<div id="content_control_height" class="tang-scrollpanel-wrapper" style="margin:0;">';
      html += '<div class="tang-scrollpanel-content" style="margin:0;">';
      html += '<ul>';
      for(var i=0;i<data.length;i++){
        s = (i+1).toString();
        var weibo = data[i]
        var mid = weibo[0];
        var uid = weibo[9];
        var name = weibo[10];
        var date = weibo[5];
        var text = weibo[3];
        var geo = weibo[4];
        var reposts_count = weibo[1];
        var comments_count = weibo[2];
        var weibo_link = weibo[7];
        var user_link = weibo[8];
        var profile_image_url = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        var repost_tree_link = 'http://219.224.135.60:8080/show_graph/' + mid;
        if (geo==''){
           geo = '未知';
        }
        var user_link = 'http://weibo.com/u/' + uid;
        html += '<li class="item">';
        html += '<div class="weibo_detail" style="width:1000px">';
        html += '<p style="text-align:left;margin-bottom:0;">' +s + '、昵称:<a class="undlin" target="_blank" href="' + user_link  + '">' + name + '</a>(' + geo + ')&nbsp;&nbsp;发布内容：&nbsp;&nbsp;' + text + '</p>';
        html += '<div class="weibo_info"style="width:100%">';
        html += '<div class="weibo_pz">';
        html += '<div id="topweibo_mid" class="hidden">'+mid+'</div>';
        html += '<a class="retweet_count" href="javascript:;" target="_blank">转发数(' + reposts_count + ')</a>&nbsp;&nbsp;|&nbsp;&nbsp;';
        html += '<a class="comment_count" href="javascript:;" target="_blank">评论数(' + comments_count + ')</a></div>';
        html += '<div class="m">';
        html += '<u>' + date + '</u>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + weibo_link + '">微博</a>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + user_link + '">用户</a>&nbsp;-&nbsp;';
        html += '<a target="_blank" href="' + repost_tree_link + '">转发树</a>';
        html += '</div>';
        html += '</div>';
        html += '</div>';
        html += '</li>';
            }
                                    
    html += '<div id="TANGRAM_54__slider" class="tang-ui tang-slider tang-slider-vtl" style="height: 100%;">';
    html += '<div id="TANGRAM_56__view" class="tang-view" style="width: 6px;">';
    html += '<div class="tang-content"><div id="TANGRAM_56__inner" class="tang-inner"><div id="TANGRAM_56__process" class="tang-process tang-process-undefined" style="height: 0px;"></div></div></div>';
    html += '<a id="TANGRAM_56__knob" href="javascript:;" class="tang-knob" style="top: 0%; left: 0px;"></a></div>';
    html += '<div class="tang-corner tang-start" id="TANGRAM_54__arrowTop"></div><div class="tang-corner tang-last" id="TANGRAM_54__arrowBottom"></div></div>';

    html += '</ul>';
    html += '</div>';
    html += '</div>';
    html += '</div>';   
    }
      $('#'+div_name).append(html);
}

Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}

sensing_sensors_table(sensor_head,data,"modal_sensor_table");
sensing_participate_table(sensor2_head,data,"sensing_participate_table");
sensing_keywords_table(keywords_head, keywords.slice(0, 10),"sensing_keywords_table");
sensing_keywords_table(keywords_head,keywords,"modal_keywords_table");
draw_line_charts('num_line_charts');
draw_line_charts('mood_line_charts');


function participate_select_all(){
	  $('input[name="participate_select"]:not(:disabled)').prop('checked', $("#participate_select_all").prop('checked'));
}