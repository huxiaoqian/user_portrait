// Date format
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
 function Search_weibo(){
  this.ajax_method = 'GET';
}

var global_pre_page = 1;
var global_choose_uids = new Array();

Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_attribute_name: function(data){
    $('#attribute_name').empty();
    html = '';
    html += '<select id="select_attribute_name" style="min-width:75px;" >';

    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        html += '<option value="' + data[s] + '">' + data[s] + '</option>';
}
    $('#attribute_name').append(html);
  },

  Draw_attribute_value: function(data){
    console.log(data);
    $('#attribute_value').empty();
    html = '';
    html += '';
    html += '<select id="select_attribute_value" style="min-width:75px;">';
    for (var i = 0; i < data.length; i++) {
        var s = i.toString();
        html += '<option value="' + data[s] + '">' + data[s] + '</option>';
} 
    $('#attribute_value').append(html);
  },
  Draw_add_group_tag: function(data){
    alert('操作成功');
    $('#myModal').modal('hide');
  },
  Draw_group_tag: function(data){
    var height = '';
    height = (data.length*50).toFixed(0) + 'px'; 
    //document.getElementById("lable").style.height=height; 
    key_container = [];
    value_container = [];
    for (i=0;i<data.length;i++){
        s=i.toString();
        key_container.push(data[s]['0']);
        value_container.push(data[s]['1']);
    }
    //var myChart = echarts.init(document.getElementById('lable'));
    // var option = {
    //     title : {
    //         text: '',
    //     },
    //     tooltip : {
    //         trigger: 'axis'
    //     },
    //     legend: {
    //         data:['标签']
    //     },
    //     toolbox: {
    //         show : true,
    //         feature : {
    //             saveAsImage : {show: true}
    //         }
    //     },
    //     calculable : true,
    //     xAxis : [
    //         {
    //             type : 'value',
    //             boundaryGap : [0, 0.01]
    //         }
    //     ],
    //     yAxis : [
    //         {
    //             type : 'category',
    //             data : key_container
    //         }
    //     ],
    //     series : [
    //         {
    //             name:'标签',
    //             type:'bar',
    //             data:value_container
    //         },
    //     ]
    // };
    // myChart.setOption(option); 
},

  Draw_overview: function(data){
    var importance_star = '';
    for(var i=0;i<data.importance_star;i++){
        importance_star += '<img src="/static/img/star-yellow.png" style="width:25px">'
    };
    var activeness_star = '';
    for(var i=0;i<data.activeness_star;i++){
        activeness_star += '<img src="/static/img/star-yellow.png" style="width:25px">'
    };
    var density_star = '';
    for(var i=0;i<data.density_star;i++){
        density_star += '<img src="/static/img/star-yellow.png" style="width:25px" >'
    };
    var influence_star = '';
    for(var i=0;i<data.influence_star;i++){
        influence_star += '<img src="/static/img/star-yellow.png" style="width:25px" >'
    };

    group_tag_vector(data.tag_vector);

    $('#overview').empty();
    html = '';
    html += '<div id="stickynote" style="height:180px;width:250px;float:left"><ul class="gs_ul" style="margin-top:-65px"><li><a>';
    html += '<p style="font-size:16px">' + data.task_name +'</p><p style="font-size:16px">' + data.submit_date +'</p><p style="font-size:16px">' + data.state +'</p><p style="font-size:16px">' + data.submit_user +'</p>';
    html += '<p><span style="font-size:16px;cursor:pointer;text-decoration:underline" onclick="show_members();">群组成员</span>&nbsp;&nbsp;';
    html += '<span style="float:right;cursor:pointer;font-size:16px;" type="button"data-toggle="modal" data-target="#group_tag2"><u>群组标签</u></span></p>';
    html += '</a></li></ul></div>';
    html += '<table style="height:150px;width:750px;float:right">';
    html += '<tr><td style="text-align:center;vertical-align:middle"><img src="/static/img/closeness.png" style="height:80px"></td>';
    html += '<td style="text-align:center;vertical-align:middle"><img src="/static/img/activeness.png" style="height:80px"></td>';
    html += '<td style="text-align:center;vertical-align:middle"><img src="/static/img/importance.png" style="height:80px"></td>';
    html += '<td style="text-align:center;vertical-align:middle"><img src="/static/img/influence.png" style="height:80px"></td></tr>';
    html += '<tr><td style="text-align:center;vertical-align:middle">' + density_star + '</td><td style="text-align:center;vertical-align:middle">' + activeness_star + '</td>';
    html += '<td style="text-align:center;vertical-align:middle">' + importance_star + '</td><td style="text-align:center;vertical-align:middle">' + influence_star + '</td></tr>';
    html += '<tr><td style="font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;紧密度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员相互转发行为的多少程度，通过聚类系数、微博转发频率及参与转发的成员比例计算得到"></i>&nbsp;&nbsp;</b></td>';
    html += '<td style="font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;活跃度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员线上线下的活跃程度，通过发布微博综述、活跃地区数、发布微博的时间走势计算得到"></i>&nbsp;&nbsp;</b></td>';
    html += '<td style="font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;重要度<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员对社会网络安全业务的重要程度，通过群体成员的所属领域和偏好话题计算得到"></i>&nbsp;&nbsp;</b></td>';
    html += '<td style="font-size:14px;text-align:center;vertical-align:middle"><b>&nbsp;&nbsp;&nbsp;&nbsp;影响力<i id="" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="衡量群体内部成员整体的影响力，通过群体成员原创微博、转发微博的评论和转发的最高值、均值、总量计算得到"></i>&nbsp;&nbsp;</b></td></tr>';
    html += '</table>';
    $('#overview').append(html);
},
Draw_basic: function(data){
    Draw_totalnumber(data);
    Draw_verify(data);
    var myChart = echarts.init(document.getElementById('sex')); 
        var dataStyle = {
        normal: {
            label: {show:false},
            labelLine: {show:false}
        }
    };
    var placeHolderStyle = {
        normal : {
            color: 'rgba(0,0,0,0)',
            label: {show:false},
            labelLine: {show:false}
        },
        emphasis : {
            color: 'rgba(0,0,0,0)'
        }
    };
    option = {
        title: {
            text: '男女？',
            subtext: '',
            sublink: '',
            x: 'center',
            y: 'center',
            itemGap: 20,
            textStyle : {
                color : 'rgba(30,144,255,0.8)',
                fontFamily : '微软雅黑',
                fontSize : 15,
                fontWeight : 'bolder'
            }
        },
        tooltip : {
            show: true,
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : document.getElementById('main').offsetWidth / 2,
            y : 45,
            itemGap:12,
            data:['男','女']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        series : [
            {
                name:'男女比例',
                type:'pie',
                clockWise:false,
                radius : [60, 80],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['1'],
                        name:'男'
                    },
                    {
                        value:data['0']['2'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            },
            {
                name:'男女比例',
                type:'pie',
                clockWise:false,
                radius : [40, 60],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['2'], 
                        name:'女'
                    },
                    {
                        value:data['0']['1'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            }
        ]
    };
                        
         myChart.setOption(option);  
    },
Draw_activity: function(data){
    Draw_top_location(data);
    Draw_top_platform(data);
    Draw_more_top_location(data);
    Draw_more_top_platform(data);
    active_geo(data);
    data_x = [];
    data_y = [];
    for (var i = 0; i < data['1'].length; i++) {
        var s = i.toString();
        value_x = new Date(parseInt(data['1'][s]['0'])*1000).format("MM-dd hh:mm");
        value_y = data['1'][s]['1'];
        data_x.push(value_x);
        data_y.push(value_y);
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
            categories: data_x,
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
            data: data_y
        }]
    });
},
Draw_social_line: function(data){
    Draw_group(data);
    draw_relation_picture(data);
    draw_relation_table(data);
    draw_more_relation_table(data);
    draw_group_out_table(data);
    draw_more_group_out_table(data);
},
Draw_keyword: function(data){
    Draw_emotion(data);
    Draw_hashtag(data);
    Draw_more_emotion(data);
    Draw_more_hashtag(data);
    Draw_more_keyword(data);
    keyword = [];
    for (i=0;i<20;i++){
      s=i.toString();
      word = {};
      word['name'] = data['1'][s]['0'];
      word['value'] = data['1'][s]['1']*60;
      word['itemStyle'] = createRandomItemStyle();
      keyword.push(word);
    }
    var myChart = echarts.init(document.getElementById('keywordcloud'));
    var option = {
    title: {
        text: '',
    },
    tooltip: {
        show: true
    },
    series: [{
        name: '关键词',
        type: 'wordCloud',
        size: ['80%', '80%'],
        textRotation : [0, 45, 90, -45],
        textPadding: 0,
        autoSize: {
            enable: true,
            minSize: 15
        },
        data:keyword
    }]
};
                    
      myChart.setOption(option);

    
},
Draw_weibo: function(data){
    Draw_influence(data);
    Draw_importance(data);
    Draw_activeness(data);
    $('#weibo').empty();
    if (data['3'].length > 9){
        $('#weibo').css("height", "615px");
    }
    else{
        var height = data['3'].length * 35 + 265;
        $('#weibo').css("height", height+"px");
    }

    html = '';
    html += '<table id="weibo_table" class="table table-striped table-bordered bootstrap-datatable datatype responsive" style="font-size:14px">'; 
    html += '<thead><tr><th style="text-align:center;vertical-align:middle">用户ID</th><th style="text-align:center;vertical-align:middle;width:180px">昵称</th><th style="text-align:center;vertical-align:middle;width:80px">活跃度</th>';
    html += '<th style="text-align:center;vertical-align:middle;">重要度</th><th style="text-align:center;vertical-align:middle;">影响力</th><th style="text-align:center;vertical-align:middle;">原创微博最大转发数</th>';
    html += '<th style="text-align:center;vertical-align:middle;">原创微博最大评论数</th><th style="text-align:center;vertical-align:middle;">转发微博最大转发数</th><th style="text-align:center;vertical-align:middle;">转发微博最大评论数</th></tr></thead>';
    html += '<tbody>';
    for ( var i = 0 ;i< data['3'].length;i++){
        s = i.toString();
        html += '<tr><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['3'][s]['0'] + '">' + data['3'][s]['0'] +'</a></th><th style="text-align:center;width:180px">' +  data['3'][s]['1'] + '</th><th style="text-align:center;width:80px">' +  data['3'][s]['2'].toFixed(2) + '</th>';
        html += '<th style="text-align:center">' +  data['3'][s]['3'].toFixed(2) + '</th><th style="text-align:center">' +  data['3'][s]['4'].toFixed(2) + '</th><th style="text-align:center"><a target="_blank" href="' + data['3'][s]['5']['2'] + '">' +  data['3'][s]['5']['0'] + '</a></th>';
        html += '<th style="text-align:center"><a target="_blank" href="' + data['3'][s]['6']['2'] + '">' + data['3'][s]['6']['0'] + '</a></th><th style="text-align:center"><a href="' + data['3'][s]['7']['2'] + '">' + data['3'][s]['7']['0'] + '</a></th><th style="text-align:center"><a href="' + data['3'][s]['8']['2'] + '">' + data['3'][s]['8']['0'] + '</a></th></tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $('#weibo').append(html);
},
Draw_personal_tag: function(data){
for (key in data){
    personal_tag =  data[key];
    document.getElementById(key).title=personal_tag;
}
},
Draw_group_weibo: function(data){
    page_num = 10;
    if (data.length < page_num) {
          page_num = data.length
          page_group_weibo( 0, page_num, data);
      }
      else {
          page_group_weibo( 0, page_num, data);
          var total_pages = 0;
          if (data.length % page_num == 0) {
              total_pages = data.length / page_num;
          }
          else {
              total_pages = Math.round(data.length / page_num) + 1;
          }
        }
    var pageCount = total_pages;

    if(pageCount>5){
        page_icon(1,5,0);
    }else{
        page_icon(1,pageCount,0);
    }
    
    $("#pageGro li").live("click",function(){
        if(pageCount > 5){
            var pageNum = parseInt($(this).html());
            pageGroup(pageNum,pageCount);
        }else{
            $(this).addClass("on");
            $(this).siblings("li").removeClass("on");
        }
      page = parseInt($("#pageGro li.on").html())  
      //console.log(page);         
      start_row = (page - 1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length)
          end_row = data.length;
        page_group_weibo(start_row,end_row,data);
    });

    $("#pageGro .pageUp").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());
            pageUp(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index > 0){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index-1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html())  
      //console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data);
    });
    

    $("#pageGro .pageDown").click(function(){
        if(pageCount > 5){
            var pageNum = parseInt($("#pageGro li.on").html());

            pageDown(pageNum,pageCount);
        }else{
            var index = $("#pageGro ul li.on").index();
            if(index+1 < pageCount){
                $("#pageGro li").removeClass("on");
                $("#pageGro ul li").eq(index+1).addClass("on");
            }
        }
      page = parseInt($("#pageGro li.on").html()) 
      //console.log(page);
      start_row = (page-1)* page_num;
      end_row = start_row + page_num;
      if (end_row > data.length){
          end_row = data.length;
      }
        page_group_weibo(start_row,end_row,data);
    });
}
}
 
var Search_weibo = new Search_weibo(); 
function Draw_group_weibo_date(){
    $('#group_weibo_date').empty();
    html = '';
    html += '<select id="select_group_weibo_date">';
    var timestamp = Date.parse(new Date());
    date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
    html += '<option value="' + date + '" selected="selected">' + date + '</option>';      
    for (var i = 0; i < 6; i++) {
        timestamp = timestamp-24*3600*1000;
        date = new Date(parseInt(timestamp)).format("yyyy-MM-dd");
        html += '<option value="' + date + '">' + date + '</option>';
}
    html += '</select>';
    $('#group_weibo_date').append(html);
  }

function page_group_weibo(start_row,end_row,data){
    weibo_num = end_row - start_row;
    $('#group_weibo').empty();
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
    $('#group_weibo').append(html);
}

function show_personal_tag(uid){
    var show_personal_tag_url = '/tag/show_user_tag/?uid_list=' + uid;
    Search_weibo.call_sync_ajax_request(show_personal_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_personal_tag);
}

function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function add_group_tag(){
    var cur_uids = []
    $('input[name="in_status"]:checked').each(function(){
        cur_uids.push($(this).attr('value'));
    });
    global_choose_uids[global_pre_page] = cur_uids;
    var select_uids = [];
    var select_uids_string = '';
    for (var key in global_choose_uids){
        var temp_list = global_choose_uids[key];
        for (var i = 0; i < temp_list.length; i++){
            select_uids.push(temp_list[i]);
        }
    }
    //console.log(select_uids);

    for (var i = 0; i < select_uids.length; i++) {
        s=i.toString();
        select_uids_string += select_uids[s] + ',';
    };
    console.log(select_uids_string);
    add_tag_attribute_name = $("#select_attribute_name").val();
    add_tag_attribute_value = $("#select_attribute_value").val();
    add_group_tag_url = '/tag/add_group_tag/?uid_list=' + select_uids_string + "&attribute_name=" + add_tag_attribute_name + "&attribute_value=" + add_tag_attribute_value;
    Search_weibo.call_sync_ajax_request(add_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_add_group_tag);
}

function Draw_more_keyword(data){
    $('#more_keyword').empty();
    html = '';
    html += '<table id ="user_group" class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">权重</th></tr>';
    for (var i = 0; i < data['1'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data['1'][s]['0'] +  '&psycho_status=&domain&topic" target="_blank">' + data['1'][s]['0'] +  '</a></th><th style="text-align:center">' + data['1'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_keyword').append(html);

 }


function Draw_group(data){
    $('#group').empty();
    html = '';
    html += '<table><tr><th style="text-align:center;width:300px">连接紧密度<i id="closeness_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内所有节点之间实际存在的边数与所有可能边数之比"></i>&nbsp;&nbsp;'+ data['1'].toFixed(2) +'(低于平均)</th>';
    html += '<th style="text-align:center;width:300px">微博转发频率<i id="weibo_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内单个节点转发群体微博的平均次数"></i>&nbsp;&nbsp;'+ data['2'].toFixed(2) +'(高于平均)</th>';
    html += '<th style="text-align:center;width:300px">参与转发比例<i id="join_tooltip" class="glyphicon glyphicon-question-sign" data-toggle="tooltip" data-placement="right" title="群体内所有参与转发群体微博的人数占群体人数的比例"></i>&nbsp;&nbsp;'+ (Math.round(data['3'] * 10000)/100).toFixed(0) + '%' +'(低于平均)</th></tr>';
    html += '</table>'; 
    $('#group').append(html);
}


function active_geo(data){
    //console.log(data);
    $('#top_active_geo').empty();
    html = '';
    html += '<div style="font-size:17px">一周轨迹</div>';
    html += '<div class="clearfix course_nr" style="margin-top:-50px"><ul class="course_nr2">';
    for (i=0; i<data['3'].length;i++){
        s = i.toString();
        html += '<li><div class="shiji"><h1>' + data['3'][s]['0'].substring(5, 10) + '</h1><p><font color="#0000E3">' + data['3'][s]['1']['0']['1'] + '</font></p><p>' + data['3'][s]['1']['0']['0'] + '</p><p><font color="#0000E3">' + data['3'][s]['1']['1']['1'] + '</font></p><p>' + data['3'][s]['1']['1']['0'] + '</p></div></li>';        
    }
    html += '</ul></div>';   
    $('#top_active_geo').append(html);
}

function draw_relation_picture(data){
    total_content = [];
    source_content = []
    for (i=0;i<data['0'].length;i++){
        s=i.toString();
        content = {};
        content['category'] = 1;
        content['name'] = data['0'][s]['1'];
        content['id'] = data['0'][s]['0'];
        content['value'] = 7;
        content['draggable'] = true;
        content['symbolSize'] = [60, 30];
        total_content.push(content);
        content = {};
        content['category'] = 1;
        content['name'] = data['0'][s]['3'];
        content['id'] = data['0'][s]['2'];
        content['value'] = 7;
        content['draggable'] = true;
        content['symbolSize'] = [60, 30];
        total_content.push(content);

        relation = {};
        relation['source'] = data['0'][s]['1'];
        relation['target'] = data['0'][s]['3'];
        relation['weight'] = data['0'][s]['4'];
        relation['name'] = data['0'][s]['4'];

        width = data['0'][s]['4'];
        normal = {'width':width};
        itemStyle= {'normal':normal};
        relation['itemStyle'] = itemStyle;

        source_content.push(relation);
    }

    var option = {
    tooltip : {
        trigger: 'item',
        formatter: '{a} : {b}'
    },
    toolbox: {
        show : true,
        feature : {
            restore : {show: true},
            magicType: {show: true, type: ['force', 'chord']},
            saveAsImage : {show: true}
        }
    },
    legend: {
        x: 'left',
        data:['']
    },
    series : [
        {
            type:'force',
            name : "",
            ribbonType: false,
            categories : [
                {
                    name:'微博用户'
                }
            ],
            itemStyle: {
                normal: {
                    label: {
                        show: true,
                        textStyle: {
                            color: '#333'
                        }
                    },
                    nodeStyle : {
                        brushType : 'both',
                        borderColor : 'rgba(255,215,0,0.4)',
                        borderWidth : 1
                    }
                },
                emphasis: {
                    label: {
                        show: false
                        // textStyle: null      // 默认使用全局文本样式，详见TEXTSTYLE
                    },
                    nodeStyle : {
                        //r: 30
                    },
                    linkStyle : {}
                }
            },
            minRadius : 15,
            maxRadius : 25,
            gravity: 1.1,
            scaling: 1.2,
            draggable: false,
            linkSymbol: 'arrow',
            steps: 10,
            coolDown: 0.9,
            //preventOverlap: true,
            nodes:total_content,
            links : source_content
        }
    ]
};
    var myChart = echarts.init(document.getElementById('relation_picture'));
    myChart.setOption(option);
    require([
            'echarts'
        ],
        function(ec){
            var ecConfig = require('echarts/config');
            function focus(param) {
                var data = param.data;
                var links = option.series[0].links;
                var nodes = option.series[0].nodes;
                if (
                    data.source != null
                    && data.target != null
                ) { //点击的是边
                    var sourceNode = nodes.filter(function (n) {return n.name == data.source})[0];
                    var targetNode = nodes.filter(function (n) {return n.name == data.target})[0];
                    // console.log("选中了边 " + sourceNode.name + ' -> ' + targetNode.name + ' (' + data.weight + ')');
                } else{
                        window.open("/index/personal/?uid=" + data.id);                 
                }
            }
                myChart.on(ecConfig.EVENT.CLICK, focus)

                myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                    //console.log(myChart.chart.force.getPosition());
                });
            }
    )
}

function draw_relation_table(data){
    $('#relation_table').empty();
    html = '';
    html = '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="margin-top:40px">';
    html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center"></td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">转发量</td></tr>';
    for (i=0;i<5;i++){
        s =i.toString();
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['0'][s]['0'] + '">' + data['0'][s]['0'] +'</a></td><td style="text-align:center">' + data['0'][s]['1'] +'</td><td style="text-align:center"><img  src= "/static/img/arrow.png" style="height:20px"></td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['0'][s]['2'] + '">' + data['0'][s]['2'] +'</a></td><td style="text-align:center">' + data['0'][s]['3'] +'</td><td style="text-align:center">' + data['0'][s]['4'] +'</td></tr>';
    };
    html += '</table>';
    html +='<div type="button" data-toggle="modal" data-target="#modal_group_in" style="font-size:16px;cursor:pointer;float:left"><u>查看更多</u></div>';
    $('#relation_table').append(html);
}

function draw_more_relation_table(data){
    $('#more_group_in').empty();
    html = '';
    html = '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center"></td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">转发量</td></tr>';
    for (i=0;i<data['0'].length;i++){
        s =i.toString();
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['0'][s]['0'] + '">' + data['0'][s]['0'] +'</a></td><td style="text-align:center">' + data['0'][s]['1'] +'</td><td style="text-align:center"><img src= "/static/img/arrow.png" style="height:20px"></td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['0'][s]['2'] + '">' + data['0'][s]['2'] +'</a></td><td style="text-align:center">' + data['0'][s]['3'] +'</td><td style="text-align:center">' + data['0'][s]['4'] +'</td></tr>';
    };
    html += '</table>';
    $('#more_group_in').append(html);
}


function draw_group_out_table(data){
    $('#relation_active_table').empty();
    html = '';
    html = '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">影响力</td><td style="text-align:center"</td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">转发量</td></tr>';
    for (i=0;i<5;i++){
        s =i.toString();
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['4'][s]['2'] + '">' + data['4'][s]['2'] +'</a></td><td style="text-align:center">' + data['4'][s]['3'] +'</td><td style="text-align:center">' + data['4'][s]['5'].toFixed(2) +'</td><td style="text-align:center"><img src= "/static/img/arrow.png" style="height:20px"></td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['4'][s]['0'] + '">' + data['4'][s]['0'] +'</a></td><td style="text-align:center">' + data['4'][s]['1'] +'</td><td style="text-align:center">' + data['4'][s]['4'] +'</td></tr>';
    };
    html += '</table>';
    $('#relation_active_table').append(html);
}

function draw_more_group_out_table(data){
    $('#more_group_out_user').empty();
    html = '';
    html = '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">影响力</td><td style="text-align:center"</td><td style="text-align:center">UID</td><td style="text-align:center">昵称</td><td style="text-align:center">转发量</td></tr>';
    for (i=0;i<data['4'].length;i++){
        s =i.toString();
    html += '<tr><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['4'][s]['2'] + '">' + data['4'][s]['2'] +'</a></td><td style="text-align:center">' + data['4'][s]['3'] +'</td><td style="text-align:center">' + data['4'][s]['5'].toFixed(2) +'</td><td style="text-align:center"><img src= "/static/img/arrow.png" style="height:20px"></td><td style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['4'][s]['0'] + '">' + data['4'][s]['0'] +'</a></td><td style="text-align:center">' + data['4'][s]['1'] +'</td><td style="text-align:center">' + data['4'][s]['4'] +'</td></tr>';
    };
    html += '</table>';
    $('#more_group_out_user').append(html);
}

function Draw_importance(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['0']['0'].length; i++) {
       var s = i.toString();
       x_value = data['0']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['0']['1'].length; i++) {
       var s = i.toString();
       y_value = data['0']['1'][s].toFixed(0);
       y_data.push(y_value);
    };
    xdata = [];
    for (i = 0; i< y_data.length-1; i++){
    xdata.push(y_data[i] + '-' + y_data[i+1])
    };
    $('#importance').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '重要度排名分布'
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
        title: {
                text: '排名'
            },
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:38//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
}

function Draw_activeness(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['1']['0'].length; i++) {
       var s = i.toString();
       x_value = data['1']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['1']['1'].length; i++) {
       var s = i.toString();
       y_value = data['1']['1'][s].toFixed(0);
       y_data.push(y_value);
    };
    xdata = [];
    for (i = 0; i< y_data.length-1; i++){
        xdata.push(y_data[i] + '-' + y_data[i+1])
    };

    $('#activeness').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '活跃度排名分布'
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
        title: {
                text: '排名'
            },
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:38//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
}


function Draw_influence(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['2']['0'].length; i++) {
       var s = i.toString();
       x_value = data['2']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['2']['1'].length; i++) {
       var s = i.toString();
       y_value = data['2']['1'][s].toFixed(0);
       y_data.push(y_value);
    };
    xdata = [];
    for (i = 0; i< y_data.length-1; i++){
        xdata.push(y_data[i] + '-' + y_data[i+1])
    };
    $('#influence').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '影响力排名分布'
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
        title: {
                text: '排名'
            },
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:38//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
}

function createRandomItemStyle(){
      
    return {
        normal: {
            color: 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
            ].join(',') + ')'
        }
    };
}
function show_members(){
	var downloadurl = window.location.host;
    var model_url =   "/group/show_group_list/?task_name=" + name;
    base_call_ajax_request(model_url, Draw_model);
    $("#myModal_group").modal();
    function Draw_model(data){
        $('#group_member_user').empty();
        html = '';
        html += '<table id="modal_table" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
        html += '<thead><tr><th class="center" style="text-align:center">用户ID</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">性别</th>';
        html += '<th class="center" style="text-align:center">注册地</th><th class="center" style="text-align:center">重要度</th><th class="center" style="text-align:center;width:72px">影响力</th>';
        html += '<th class="center" style="text-align:center">全选<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()"></th>';
        html += '</tr></thead>';
        html += '<tbody>';
        for ( i=0 ; i<data.length; i++){
            s = i.toString();
            if (data[s]['2'] == 1){
                sex = '男';
            }else{
                sex = '女';
            }
          html += '<th class="center" style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data[s]['0']+ '">' + data[s]['0']+ '</a></th><th class="center" style="text-align:center">' + data[s]['1']+ '<img data-toggle="tooltip" data-placement="right" title="" id=' + data[s]['0'] + ' src="/static/img/tag.png" class="tag" onmouseover="show_personal_tag(' + data[s]['0'] + ')"; style="height:20px"></th><th class="center" style="text-align:center">' + sex+ '</th>';
          html += '<th class="center" style="text-align:center">' + data[s]['3']+ '</th><th class="center" style="text-align:center">' + data[s]['4'].toFixed(2) + '</th><th class="center" style="text-align:center;width:72px">' + data[s]['5'].toFixed(2) + '</th>';  
          html += '<th class="center" style="text-align:center"><input name="in_status" class="in_status" type="checkbox" value="' + data[s]['0'] + '"/></th>';
          html += '</tr>';
        };
        html += '</tbody>';
        html += '</table>';
        $('#group_member_user').append(html);
        $('#modal_table').dataTable({
            "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
            "sPaginationType": "custom_bootstrap",
            // "aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}],
            "oLanguage": {
                "sLengthMenu": "_MENU_ 每页"
            }
        });
    }
}

$(document).ready(function(){
	var downloadurl = window.location.host;
    Draw_group_weibo_date();
    // Draw_think_emotion();
    // Draw_think_domain();
    // Draw_think_topic();
    // Draw_think_tendency();

    var group_overview_url = '/group/show_group_result/?module=overview&task_name=' + name;
    //var overviewdata = ['媒体','2013-09-01','关注的媒体','0.2222','0.542','6.233','10000.345','某某']
    //Search_weibo.Draw_overview(overviewdata);
    // var weibo_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=overview";
     Search_weibo.call_sync_ajax_request(group_overview_url, Search_weibo.ajax_method, Search_weibo.Draw_overview);
    var tag_url =  'http://' + downloadurl + "/tag/show_attribute_name/";
    Search_weibo.call_sync_ajax_request(tag_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_name);
    // var basic_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=basic";
    // Search_weibo.call_sync_ajax_request(basic_url, Search_weibo.ajax_method, Search_weibo.Draw_basic);
    var select_attribute_name =document.getElementById("select_attribute_name").value;
    console.log(select_attribute_name);
    var attribute_value_url = '';
    attribute_value_url = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
    //attribute_value_url = '/tag/show_attribute_value/?attribute_name=风暴';
    Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);

    //var show_group_tag_url = '/tag/show_group_tag/?task_name=' + '媒体';
    //Search_weibo.call_sync_ajax_request(show_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_group_tag);

    // var show_group_weibo_url = 'http://' + downloadurl + '/weibo/show_group_weibo/?task_name=' + name + "&date=2013-09-02";
    // Search_weibo.call_sync_ajax_request(show_group_weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_group_weibo);

    // var activity_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=activity";
    // Search_weibo.call_sync_ajax_request(activity_url, Search_weibo.ajax_method, Search_weibo.Draw_activity);
    // var social_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=social";
    // Search_weibo.call_sync_ajax_request(social_url, Search_weibo.ajax_method, Search_weibo.Draw_social_line);
    // var think_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=think";
    // var text_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=text";
    // Search_weibo.call_sync_ajax_request(text_url, Search_weibo.ajax_method, Search_weibo.Draw_keyword);
    // var influence_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=influence";
    // Search_weibo.call_sync_ajax_request(influence_url, Search_weibo.ajax_method, Search_weibo.Draw_weibo);

    $('#select_attribute_name').change(function(){
            // console.log($(this).val());
            var attribute_value_url = '/tag/show_attribute_value/?attribute_name=' ;
            attribute_value_url += $(this).val();
            Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);
        });
    
})

// $('#select_attribute_name').click(function(){
//     var select_attribute_name = $("#select_attribute_name").val();
//     console.log(select_attribute_name);
//     var attribute_value_url = '';
//     attribute_value_url = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
//     Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);
// });
/*
$('#select_attribute_name').click(function(){
    console.log('dfsd');
    var select_attribute_name = $("#select_attribute_name").val();
    var attribute_value_url = '';
    url_attribute_value = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
    Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);
});

function Valuechange(){
      console.log('asdasd');
      var select_attribute_name = document.getElementById("select_attribute_name").value;
      console.log(select_attribute_name);
      var attribute_value_url = '';
      // attribute_value_url = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
      attribute_value_url = '/tag/show_attribute_value/?attribute_name=' +select_attribute_name ;
      Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);
    }
*/
function Draw_verify(data){
    var myChart = echarts.init(document.getElementById('verify')); 
        var dataStyle = {
        normal: {
            label: {show:false},
            labelLine: {show:false}
        }
    };
    var placeHolderStyle = {
        normal : {
            color: 'rgba(0,0,0,0)',
            label: {show:false},
            labelLine: {show:false}
        },
        emphasis : {
            color: 'rgba(0,0,0,0)'
        }
    };
    option = {
        title: {
            text: '你认证了吗？',
            subtext: '',
            sublink: '',
            x: 'center',
            y: 'center',
            itemGap: 20,
            textStyle : {
                color : 'rgba(30,144,255,0.8)',
                fontFamily : '微软雅黑',
                fontSize : 15,
                fontWeight : 'bolder'
            }
        },
        tooltip : {
            show: true,
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : document.getElementById('main').offsetWidth / 2,
            y : 45,
            itemGap:12,
            data:['已认证','未认证']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        series : [
            {
                name:'认证比例',
                type:'pie',
                clockWise:false,
                radius : [60, 80],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['1'],
                        name:'已认证'
                    },
                    {
                        value:data['0']['2'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            },
            {
                name:'认证比例',
                type:'pie',
                clockWise:false,
                radius : [40, 60],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['2'], 
                        name:'未认证'
                    },
                    {
                        value:data['0']['1'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            }
        ]
    };
                        
         myChart.setOption(option);  
    }
function Draw_totalnumber(data){
    $('#totalnumber').empty();
    html = '';
    html += '<a class="well top-block" style="height:180px;width:180px;border-radius:400px;margin-top:10px">';
    html += '<div><img src="/static/img/user_group.png" style="height:40px;margin-top:40px"></div>';
    html += '<div>群组总人数</div>'
    html += '<div>' + data['1'] + '</div></a>';
    $('#totalnumber').append(html);
}

function Draw_think_emotion(){
    var myChart = echarts.init(document.getElementById('pie_emotion')); 
    var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: false},
            dataView : {show: false, readOnly: false},
            magicType : {
                show: false, 
                type: ['pie', 'funnel']
            },
            restore : {show: false},
            saveAsImage : {show: true}
        }
    },
    calculable : false,
    series : [
        {
            name:'',
            type:'pie',
            selectedMode: 'single',
            radius : [0, 35],
            
            // for funnel
            x: '20%',
            width: '40%',
            funnelAlign: 'right',
            max: 1548,
            
            itemStyle : {
                normal : {
                    label : {
                        position : 'inner'
                    },
                    labelLine : {
                        show : false
                    }
                }
            },
            data:[
                {value:5, name:'积极'},
                {value:5, name:'中性'},
                {value:12, name:'消极', selected:true}
            ]
        },
        {
            name:'',
            type:'pie',
            radius : [50, 70],
            
            // for funnel
            x: '60%',
            width: '35%',
            funnelAlign: 'left',
            max: 1048,
            
            data:[
                {value:5, name:'积极'},
                {value:5, name:'中性'},
                {value:3, name:'生气'},
                {value:4, name:'悲伤'},
                {value:5, name:'其他'}
            ]
        }
    ]
}
    myChart.setOption(option);  
                    
}

function Draw_think_topic(){
    var myChart = echarts.init(document.getElementById('radar_topic')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['话题']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
            indicator : [
                {text : '娱乐', max  : 100},
                {text : '计算机', max  : 100},
                {text : '经济', max  : 100},
                {text : '教育', max  : 100},
                {text : '自然', max  : 100},
                {text : '健康', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '话题'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}

function Draw_think_tendency(){
        var myChart = echarts.init(document.getElementById('radar_tendency')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['倾向性']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
            indicator : [
                {text : '九一八', max  : 100},
                {text : '马航', max  : 100},
                {text : '六四', max  : 100},
                {text : 'APEC', max  : 100},
                {text : '踩踏事件', max  : 100},
                {text : '东盟博览会', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '倾向性'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}

function Draw_think_domain(){
    var myChart = echarts.init(document.getElementById('radar_domain')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['领域']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                {text : '高校微博', max  : 100},
                {text : '境内机构', max  : 100},
                {text : '境外机构', max  : 100},
                {text : '媒体', max  : 100},
                {text : '律师', max  : 100},
                {text : '草根', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 56, 28, 94, 45, 86],
                        name : '领域'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}

   
function Draw_hashtag(data){
    $('#hashtag').empty();
    html = '';
    html += '<div><span style="font-size:17px;">hashtag排名</span><span style="font-size:17px;float:right;cursor:pointer" type="button"data-toggle="modal" data-target="#rank_hashtag"><u>查看更多</u></span></div>';
    html += '<table id ="user_group" class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">hashtag</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < 5; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=' + data['0'][s]['0'] +  '&adkeyword=&psycho_status=&domain&topic" target="_blank">' + data['0'][s]['0'] +  '</a></th><th style="text-align:center">' + data['0'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#hashtag').append(html);    
}

function Draw_more_hashtag(data){
    $('#more_hashtag').empty();
    html = '';
    html += '<table id ="user_group" class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">hashtag</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data['0'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=' + data['0'][s]['0'] +  '&adkeyword=&psycho_status=&domain&topic" target="_blank">' + data['0'][s]['0'] +  '</a></th><th style="text-align:center">' + data['0'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_hashtag').append(html);    
}
function text2icon(text){
    var icon = '';
    for (var i = 0;i < emoticon_list.length;i++){
        var item = emoticon_list[i];
        if (item['value'] == text){
            icon = item['icon'];
            return icon;
        }
    }
    return icon;
}

function Draw_emotion(data){
    $('#emotion').empty();
    html = '';
    html += '<div><span style="font-size:17px;">表情符号排名</span><span style="font-size:17px;float:right;cursor: pointer" type="button"data-toggle="modal" data-target="#rank_emotion"><u>查看更多</u></span></div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">表情符号</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i <  5; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['2'][s]['0'] + '<img src=' + text2icon(data['2'][s]['0']) + ' /></th><th style="text-align:center">' + data['2'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#emotion').append(html);    
}

function Draw_more_emotion(data){
    $('#more_emotion').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">表情符号</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i <  data['2'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['2'][s]['0'] + '<img src=' + text2icon(data['2'][s]['0']) + ' /></th><th style="text-align:center">' + data['2'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_emotion').append(html);    
}

function Draw_top_location(data){
    $('#top_location').empty();
    html = '';
    html += '<div><span style="font-size:17px;">发布地点排名</span><span style="font-size:17px;margin-left:230px;cursor: pointer" type="button"data-toggle="modal" data-target="#rank_geo"><u>查看更多</u></span></div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:400px;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">地点</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i <  5; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=' + data['0'][s]['0'] +  '&hashtag=&adkeyword=&psycho_status=&domain&topic" target="_blank">' + data['0'][s]['0'] +  '</a></th><th style="text-align:center">' + data['0'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_location').append(html);
}

function Draw_more_top_location(data){
    $('#top_more_location').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">地点</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i <  data['0'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=' + data['0'][s]['0'] +  '&hashtag=&adkeyword=&psycho_status=&domain&topic" target="_blank">' + data['0'][s]['0'] +  '</a></th><th style="text-align:center">' + data['0'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_more_location').append(html);
}
function Draw_top_platform(data){
    $('#top_platform').empty();
    html = '';
 html += '<div><span style="font-size:17px;">发布平台排名</span><span style="font-size:17px;margin-left:230px;cursor:pointer" type="button"data-toggle="modal" data-target="#rank_platform"><u>查看更多</u></span></div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:400px;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">平台</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data['2'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['2']['0']['0'] + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#top_platform').append(html);
}

function Draw_more_top_platform(data){
    $('#top_more_platform').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">平台</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data['2'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['2']['0']['0'] + '</th><th style="text-align:center">2819</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">237</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">158</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">74</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">30</th></tr>';
    html += '</table>'; 
    $('#top_more_platform').append(html);
}

function Draw_think_status(){
    var myChart = echarts.init(document.getElementById('radar_status')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['身份']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                {text : '进攻', max  : 100},
                {text : '防守', max  : 100},
                {text : '体能', max  : 100},
                {text : '速度', max  : 100},
                {text : '力量', max  : 100},
                {text : '技巧', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '身份'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}

function group_tag_vector(data){
    $('#group_tag_vector').empty();
    var html = '';
    html += '<table class="table table-striped">';
    html += '<tr>';
    for(var key in data){
        html += '<tr>';
        html += '<th>'+ data[key][0] + '</th>';
        if(data[key][0] == '主要消极情绪'){
            var value_emotion='';
            // console.log('情绪',data[key][0])
            switch(data[key][1])
            {
            case '2': value_emotion = "生气";break;
            case '3': value_emotion = "焦虑";break;
            case '4': value_emotion = "悲伤";break;
            case '5': value_emotion = "厌恶";break;
            case '6': value_emotion = "消极其他";break;
            } 
            html += '<th>'+ value_emotion + '</th>';
        }else{
            html += '<th>'+ data[key][1] + '</th>';
        }
        //html += data[key][1] + '</span></li>';
        html += '</tr>'
    }
    html += '</table>'
    //console.log('tagvector');
    //console.log(global_tag_vector);
    $('#group_tag_vector').html(html);
}
