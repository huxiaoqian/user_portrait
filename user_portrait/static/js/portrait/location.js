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
function getDate(tm){
    var tt = new Date(parseInt(tm)*1000).format("MM-dd hh:mm");
    return tt;
}
function getDate_zh(tm){
    var tt = new Date(parseInt(tm)*1000).format("MM-dd");
    return tt;
}
function activity_call_ajax_request(url, callback){
$.ajax({
  url: url,
  type: 'GET',
  dataType: 'json',
  async: false,
  success:callback
});
}
function geo_track(data){
	var geo_data = data[0]
	//console.log(geo_data);
	document.getElementById('saysay').innerHTML = data[1];
	var date = [];
	var citys = [];
	for(var key in geo_data){
		date.push(geo_data[key][0]);
		citys.push(geo_data[key][1][0])
	}
	//console.log(citys);
	//console.log(date);
	for(i=0;i<date.length;i++){
		document.getElementById('d'+(i+1)).innerHTML = date[i];
    }
    for(i=0;i<citys.length;i++){
        //console.log(citys[i]);
		if(citys[i]){
			document.getElementById('city'+(i+1)).innerHTML = citys[i][0];
		}else{
			$('#city'+(i+1)).addClass('gray');
			document.getElementById('city'+(i+1)).innerHTML = '未发布微博';
		}
		
	}
}

var url = '/attribute/geo_track/?uid='+ uid;
activity_call_ajax_request(url, geo_track);

function  active_chart(data){
	//console.log(data);
	var item = data.activity_time;
    for (i=0;i<item.length;i++){
       var date = item[i][0]/(15*60*16);
       switch(date)
       {
            case 0: x = "00:00-04:00";break;
            case 1: x = "04:00-08:00";break;
            case 2: x = "08:00-12:00";break;
            case 3: x = "12:00-16:00";break;
            case 4: x = "16:00-20:00";break;
            case 5: x = "20:00-24:00";break;
       }
       var str ="time"+(i+1);
       time = document.getElementById(str);
       time.innerHTML = x;
    }
    var trend = data.activity_trend;
	var data_count=[];
	var data_time = [];
	var date_zhang = [];
    for(i=0;i<trend.length;i++){
        var time = getDate(trend[i][0]);
        var count = trend[i][1];
		var date_zh =getDate_zh(trend[i][0])
		data_time.push(time);
		data_count.push(count);
		date_zhang.push(date_zh);
    }
	$('#date_zh').html(date_zhang[0]);
	//$('#date_zh').setAttribute(value,date_zhang[0]);
    /*
	var date_html ='';
	$('#select_date').empty();
	console.log(date_zhang[i]);
	date_html =date_html + '<option value="'+date_zhang[i]+'">'+date_zhang[i]+'</option>';
    $('#select_date').append(date_html);
    */
	//Draw_trend:
	 $('#Activezh').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '微博时间走势图',
			align:'left',
			fontSize:'20',
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
            categories: data_time,
            labels:{
              rotation: 0,
              step: 6,
              x:0,
              y:30,
            }
        },
        yAxis: {
			min:0,
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
                        point2weibo(event.point.x, trend[event.point.x]);
                    }
                }
            }
        },
        tooltip: {
            valueSuffix: '条',
            xDateFormat: '%H:%M:%S'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name:'微博量',
            data: data_count
        }]
    });
	 $('#activeness').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '活跃度走势图',
			align:'left',
			fontSize:'20',
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
            categories: data_time,
            labels:{
                rotation: 0,
                step: 6,
                x:0,
                y:30,
            }
        },
        yAxis: {
			min:0,
            title: {
                text: '微博总量 (条)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '条',
            xDateFormat: '%H:%M:%S'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name:'活跃度',
            data: data_count
        }]
    });
}
//微博文本默认数据
function point2weibo(xnum, ts){
	var url ="/weibo/show_user_weibo_ts/?uid="+uid+"&ts="+ts[0];
    var delta;
    //console.log(url);
	activity_call_ajax_request(url, draw_content);
    $('#date_zh').html(getDate_zh(ts));
    switch(xnum % 6)
    {
        case 0: delta = "00:00-04:00";break;
        case 1: delta = "04:00-08:00";break;
        case 2: delta = "08:00-12:00";break;
        case 3: delta = "12:00-16:00";break;
        case 4: delta = "16:00-20:00";break;
        case 5: delta = "20:00-24:00";break;
    }
    $('#time_zh').html(delta);
	function draw_content(data){
        var html = '';
        $('#weibo_text').empty();
        if(data==''){
            html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
        }else{
            for(i=0;i<data.length;i++){
                //console.log(data[i].text);
                html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i].text+"</span></div>";
            }

        }
        $('#weibo_text').append(html);
    }
}

var url = '/attribute/activity/?uid=' + uid;
activity_call_ajax_request(url, active_chart);

function draw_daily_ip_table(div_name){
    var location_geo = parent.personalData.activity_geo;
    console.log(location_geo);
    $('#'+div_name).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">IP</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < location_geo.length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m;
       html += '</th><th style="text-align:center">' + location_geo[i][0];
       html += '</th><th style="text-align:center">' + location_geo[i][1];
       html +='</th></tr>';
    };
    html += '</table>'; 
    $('#'+div_name).append(html);                  
}
var div_name = 'daily_ip';
draw_daily_ip_table(div_name);
var div_name = 'weekly_ip';
draw_daily_ip_table(div_name);
var div_name = 'monthly_location';
draw_daily_ip_table(div_name);

function location_desc(data){
	var description1 = document.getElementById('location_description1');
	var description3 = document.getElementById('location_description3');
	//description.innerHTML = data['description'];
	var length =  data['description'].length;
	if(length==2){
		description1.style.color="red";
		description1.innerHTML = data['description'][0];
		document.getElementById('location_description2').innerHTML = data['description'][1];
	}else{
		description1.style.color="red";
		description1.innerHTML = data['description'][0];
		document.getElementById('location_description2').innerHTML = data['description'][1];
		description3.style.color="red";
		description3.innerHTML = data['description'][2];
		document.getElementById('location_description4').innerHTML = data['description'][3];
	}
}
var url ="/attribute/location/?uid="+uid;
activity_call_ajax_request(url, location_desc);

function Weibo(){
  this.ajax_method = 'GET';
}
Weibo.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_content:function(data){
	var html = '';
	$('#weibo_text').empty();
    if(data==''){
        html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
    }else{
        for(i=0;i<data.length;i++){
            //console.log(data[i].text);
            html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i].text+"</span></div>";
        }

    }
	$('#weibo_text').append(html);
  }
}

var date = '';
var time = '';
var dateStr = '';
var ts = '';
date = $('#date_zh').html();
time = '00:00:00';
dateStr = '2013-'+date+' '+time;
ts = get_unix_time(dateStr);
var Weibo = new Weibo();
var url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);

/*
$('#select_date').change(function(){
	date = $('#select_date').val();
	dateStr = '2015-'+date+' '+time+':00';
	ts = get_unix_time(dateStr);
	url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
	Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);
})
$('#select_time').change(function(){
	 time = $('#select_time').val();
	 dateStr = '2015-'+date+' '+time+':00';
	 ts = get_unix_time(dateStr);
	 url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
	 Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);
})
*/
//dateStr = '2015-'+date+' '+time+':00';
//console.log(dateStr);
//dateStr = '2014-05-08 00:22:11 ';
//
/*
$('#choose_date').click(function(){
	date = $('#select_date').val();
	time = $('#select_time').val();
	dateStr = '2013-'+date+' '+time;
	ts = get_unix_time(dateStr);
	url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
    console.log(url);
	Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);
})
*/
function get_unix_time(dateStr){
    var newstr = dateStr.replace(/-/g,'/'); 
    var date =  new Date(newstr); 
    var time_str = date.getTime().toString();
    return time_str.substr(0, 10);
}

