function draw_influ_distribution(data){
    var mychart1 = echarts.init(document.getElementById('influ_distribution'));
    var y_axi = data[0];
    var x_axi = data[1];
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
            data : y_axi
        }
    ],
    series : [
        {
            name:'2011年',
            type:'bar',
            data:x_axi
        }
    ]
};
  mychart1.setOption(option);
}

function Show_influ(url,div){
    that = this;
    this.ajax_method = 'GET';
    this.div = div;
}

Show_influ.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_table:function(data){
    influ_his = data['influence_his'];
    influ_in_user = data['influence_in_user'];
    influ_out_user = data['influence_out_user'];
    influ_trend = data['influence_trend'];
    draw_influ_distribution(influ_his);
    show_influ_users('influ_active_users',influ_trend['main_max']);
    show_influ_users('influ_unactive_users',influ_trend['main_min']);
    //console.log(influ_trend['main_max']);
    //console.log(influ_out_user);
    group_influ(influ_trend);
  }
}

var Show_influ = new Show_influ();
var group_influ_url = '/group/show_group_result/?task_name=媒体&module=influence';
Show_influ.call_sync_ajax_request(group_influ_url, Show_influ.ajax_method, Show_influ.Draw_table);
function show_influ_users(div_name,data){
    $('#' + div_name).empty();
    console.log(data);
    var html = '';
    html += '<table class="table table-striped" style="font-size:14px;margin-bottom:0px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">频数</th></tr>';
    for (var i = 0; i < data.length; i++) {
       var s = i.toString();
       var m = i + 1;
       var uname = data[i][0].split('&')[1]
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + uname + '</th><th style="text-align:center">' + data[i][1] + '</th></tr>';
    };
    /*
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    */
    html += '</table>'; 
    $('#'+div_name).append(html);
}
function show_more_influ_active_users(div_name){
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

function group_influ(data){
   var mychart = echarts.init(document.getElementById('group_influ'));
   ave_data = data['ave_list'];
   max_data = data['max_list'];
   min_data = data['min_list'];
   time_data = data['time_list'];
   var option = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['最高','平均','最小']
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
            data : time_data
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'最高',
            type:'line',
            stack: '总量',
            data:max_data
        },
        {
            name:'平均',
            type:'line',
            stack: '总量',
            data:ave_data
        },
        {
            name:'最小',
            type:'line',
            stack: '总量',
            data:min_data
        }
        
    ]
};
  mychart.setOption(option);
}


function Draw_group_influ_weibo(data, div_name, sub_div_name){
    page_num = 5;
    console.log(div_name);
    if (data.length < page_num) {
        console.log('data_length', data.length);
        $('#'+ div_name + ' #pageGro .pageUp').css('display', 'none');
        $('#'+ div_name + ' #pageGro .pageList').css('display', 'none'); 
        $('#'+ div_name + ' #pageGro .pageDown').css('display', 'none'); 
        if (data.length == 0) {
            $('#' + sub_div_name).empty();
            $('#' + sub_div_name).append('此条件下没有与此事件相关的微博！');
        }else{
            page_num = data.length
            page_group_influ_weibo( 0, page_num, data, sub_div_name);
        }
      }
      else {
          page_group_influ_weibo( 0, page_num, data, sub_div_name);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>10){
        page_icon(1,10,0, div_name);
    }else{
        page_icon(1,pageCount,0, div_name);
    }
    
    $("#"+div_name+" #pageGro li").bind("click", function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      console.log('page', page);         
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        console.log('start', start_row);
        console.log('end', end_row);
        console.log('data',data);
        page_group_influ_weibo(start_row,end_row,data, sub_div_name);
    });

    $("#"+div_name+" #pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());
            pageUp(pageNum,pageCount);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index > 0){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html())  
      console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_influ_weibo(start_row,end_row,data, sub_div_name);
    });
    

    $("#" + div_name + " #pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#"+div_name+" #pageGro li.on").html());

            pageDown(pageNum,pageCount);
        }else{
            var index = $("#"+div_name+" #pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#"+div_name+" #pageGro li").removeClass("on");
                $("#"+div_name+" #pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#"+div_name+" #pageGro li.on").html()) 
      console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_influ_weibo(start_row,end_row,data, sub_div_name);
    });
}

function page_group_influ_weibo(start_row,end_row,data, sub_div_name){
    weibo_num = end_row - start_row;
    $('#'+ sub_div_name).empty();
    var html = "";
    html += '<div class="group_weibo_font">';
    for (var i = start_row; i < end_row; i += 1){
        s=i.toString();
        uid = data[s]['uid'];
        text = data[s]['text'];
        uname = data[s]['uname'];
        timestamp = data[s]['timestamp'];
        date = new Date(parseInt(timestamp)*1000).format("yyyy-MM-dd hh:mm:ss");
        if (i%2 ==0){
            html += '<div style="background:whitesmoke;font-size:14px">';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>'
    }
        else{
            html += '<div>';
            html += '<p><a target="_blank" href="/index/personal/?uid=' + uid + '">' + uname + '</a>&nbsp;&nbsp;发布:<font color=black>' + text + '</font></p>';    
            html += '<p style="margin-top:-5px"><font color:#e0e0e0>' + date + '</font></p>';
            html += '</div>';
        }
    }
    html += '</div>'; 
    $('#'+sub_div_name).append(html);
}

//日期选择
var date = new Date();
date.setHours(0,0,0,0);
var max_date = date.format('yyyyMMdd');
var current_date = date.format('yyyy/MM/dd');
var from_date_time = Math.floor(date.getTime()/1000) - 60*60*24*30;
var min_date_ms = new Date()
min_date_ms.setTime(from_date_time*1000);
var from_date = min_date_ms.format('yyyy/MM/dd');

$('#group_influ_weibo #weibo_from').datetimepicker({value:from_date,step:60,minDate:'-1970/01/30',maxDate:'+1970/01/01'});
$('#group_influ_weibo #weibo_to').datetimepicker({value:current_date,step:60,minDate:'-1970/01/30',maxDate:'+1970/01/01'});

function Draw_group_weibo_user(){
    $('#group_influ_weibo_user').empty();
    html = '';
    html += '<select id="select_group_weibo_user" style="max-width:150px;">';
    // var timestamp = Date.parse(new Date());
    // date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
    var all= '全部用户'
    html += '<option value="' + all + '" selected="selected">' + all + '</option>';      
    for (var i = 0; i < 6; i++) {
        // timestamp = timestamp-24*3600*1000;
        // date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
        html += '<option value="' + i + '">' + i + '</option>';
    }
    html += '</select>';
    $('#group_influ_weibo_user').append(html);
}

function submit_date_user(){
    alert('aaa');
}

function get_radar_data (data) {
  var topic = data;
  var topic_name = [];
  var topic_value = [];
  for(var i=0; i<topic.length;i++){
    topic_value.push(topic[i][1])
    topic_name.push(topic[i][0])
  };
  // var topic_value2 = [];
  // var topic_name2 = [];
  // for(var i=0; i<8;i++){ //取前8个最大值
  //   a=topic_value.indexOf(Math.max.apply(Math, topic_value));
  //   topic_value2.push(topic_value[a].toFixed(3));
  //   topic_name2.push(topic_name[a]);
  //   topic_value[a]=0;
  // }
  var topic_name3 = [];
  for(var i=0;i<8;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name[i];
    name_dict["text"] = index;
    name_dict["max"] = Math.max.apply(Math, topic_value).toFixed(3)+0.2;
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value);
  return topic_result;
}

function Draw_topic(data, radar_div){
  var topic = [];
  var html = '';
  if(data.length == 0){
      var html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      //$('#'+ more_div).append(html);
      $('#'+ radar_div).append(html);
      //$('#'+ show_more).empty();
  }else{
    };
  var topic_result = [];
  topic_result = get_radar_data(data);
  var topic_name = topic_result[0];
  var topic_value = topic_result[1];
  var myChart2 = echarts.init(document.getElementById(radar_div));
  var option = {
    // title : {
    //   text: '用户话题分布',
    //   subtext: ''
    // },
      tooltip : {
        trigger: 'axis'
      },
      toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            restore : {show: true},
            saveAsImage : {show: true}
        }
      },
      calculable : true,
      polar : [
       {
        indicator :topic_name,
        radius : 90
       }
      ],
      series : [
       {
        name: '话题分布情况',
        type: 'radar',
        itemStyle: {
         normal: {
          areaStyle: {
            type: 'default'
          }
         }
        },
       data : [
        {
         value : topic_value,
         name : '用户话题分布'}
       ]
      }]
  };
  myChart2.setOption(option);
}
// function Draw_topic(data, radar_div, motal_div, show_more){
//   var topic = [];
//   var html = '';
//   $('#'+ motal_div).empty();
//   if(data.length == 0){
//       $('#'+ motal_div).empty();
//       html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
//       //$('#'+ more_div).append(html);
//       $('#'+ radar_div).append(html);
//       $('#'+ motal_div).append(html);
//       $('#'+ show_more).empty();
//   }else{
//       html = '';
//       html += '<table class="table table-striped table-bordered" style="width:450px;">';
//       html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">频率</th></tr>';
//       for (var i = 0; i < data.length; i++) {
//          var s = i.toString();
//          var m = i + 1;
//          html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data[i][0] +  '&psycho_status=&domain&topic" target="_blank">' + data[i][0] +  '</a></th><th style="text-align:center">' + data[i][1].toFixed(3) + '</th></tr>';
//       };
//       html += '</table>'; 
//       $('#'+ motal_div).append(html);
//     };
//   var topic_result = [];
//   topic_result = get_radar_data(data);
//   var topic_name = topic_result[0];
//   var topic_value = topic_result[1];
//   var myChart2 = echarts.init(document.getElementById(radar_div));
//   var option = {
//     // title : {
//     //   text: '用户话题分布',
//     //   subtext: ''
//     // },
//       tooltip : {
//         trigger: 'axis'
//       },
//       toolbox: {
//         show : true,
//         feature : {
//             mark : {show: true},
//             dataView : {show: true, readOnly: false},
//             restore : {show: true},
//             saveAsImage : {show: true}
//         }
//       },
//       calculable : true,
//       polar : [
//        {
//         indicator :topic_name,
//         radius : 90
//        }
//       ],
//       series : [
//        {
//         name: '话题分布情况',
//         type: 'radar',
//         itemStyle: {
//          normal: {
//           areaStyle: {
//             type: 'default'
//           }
//          }
//         },
//        data : [
//         {
//          value : topic_value,
//          name : '用户话题分布'}
//        ]
//       }]
//   };
//   myChart2.setOption(option);
// }

var data0=[['人民日报1111',1,2,'1111这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','param.name'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','param.name'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','param.name'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','2013-09-07 20:00'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','2013-09-07 20:00'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','2013-09-07 20:00'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','2013-09-07 20:00'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','2013-09-07 20:00'],['人民日报',1,2,'这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论这里是一条结论','中国 北京 北京','2013-09-07 20:00'],['0',1,2,'3neirong',4,44,6,7,8,9,0],['0',1,2,'3neirong',4,5,6,7,8,9,0],['0',1,2,'333333333neirong',4,5,6,7,8,9,0]]

//影响力走势
//draw_influ_distribution();
//group_influ();
//show_influ_users('influ_active_users');
//show_influ_users('influ_unactive_users');
show_more_influ_active_users('show_rank_influ_users');
show_more_influ_active_users('show_rank_uninflu_users');
$('#group_influence_conclusion').append('结论结论结论结论');

//影响力内容：用户微博
    //选择用户
Draw_group_weibo_user();  
    //选择时间
var url_all = [];
var time_from = Date.parse($('#group_influ_weibo #weibo_from').val())/1000;
var time_to = Date.parse($('#group_influ_weibo #weibo_to').val())/1000;
var timestamp_from_url = '';
timestamp_from_url = 'timestamp_from=' + time_from;
url_all.push(timestamp_from_url);
var timestamp_to_url = '';
timestamp_to_url = 'timestamp_to=' + time_to;
url_all.push(timestamp_to_url);
console.log(url_all);

//提交条件
//submit_date_user();
//显示内容
Draw_group_influ_weibo(data0,'group_influ_weibo', 'group_influ_weibo_result');

var topic = [['sdgsd',21],['dsf',23],['sfv',12],['rhtb',13],['6ef',28],['sgsd',51],['d2sf',17],['tfv',22],['htb',1]];
Draw_topic(topic,'influence_topic');
Draw_topic(topic,'influence_domain');

//波及用户
$(' input[name="user_select"]').click(function(){
    if($('input[name="user_select"]:checked').val()=='1'){       
        $('#influence_in_user').css('display', 'none');
        $('#influence_out_user').css('display', 'block');
    }else{
        $('#influence_in_user').css('display', 'block');
        $('#influence_out_user').css('display', 'none');
    }
});