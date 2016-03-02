function Search_weibo(){
  this.ajax_method = 'GET';
  that = this;
}

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

    Get_Callback_data:function(data){
        that.call_data = data
    },
    
    Return_data: function(){
        return that.call_data;
    },

    Draw_table: function(data){
        $('#table').empty();
        var html = '';
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive" >';
        html += '<thead ><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">重要度</th><th class="center" style="text-align:center;width:72px">活跃度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">得分</th></tr></thead>';
        html += '<tbody>';
        for(var item in data){
            html += '<tr>';
            for(var i =0; i < data[item].length; i++){                
                html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data[item][i] +'</td>';
            }
            html += '</tr>';
        }
        html += '</tbody>';
        html += '</table>';
        $('#table').append(html);
    },

    Draw_cloud_keywords:function(data, div){

        function createRandomItemStyle() {
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
        var keywords_data = data;
        var keywords = new Array();

        for(i in keywords_data){

            keywords.push({'name':keywords_data[i][0], 'value':keywords_data[i][1]*1000, 'itemStyle':createRandomItemStyle()});
            
        }

        option = {
            title: {
                text: '',
            },
            tooltip: {
                show: true
            },
            series: [{
                name: '',
                type: 'wordCloud',
                size: ['80%', '80%'],
                textRotation : [0, 45, 90, -45],
                textPadding: 0,
                autoSize: {
                    enable: true,
                    minSize: 14
                },
                data: keywords,
            }]
        };
        var myChart = echarts.init(document.getElementById(div));
        myChart.setOption(option);
    },

    Draw_line:function(x_data, value_data,div){

        option = {
            title : {
                text: '',
                subtext: ''
            },
            tooltip : {
                trigger: 'axis'
            },
            calculable : true,
            xAxis : [
                {
                    type : 'category',
                    boundaryGap : false,
                    data : x_data
                }
            ],
            yAxis : [
                {
                    type : 'value',
                    axisLabel : {
                        formatter: ''
                    }
                }
            ],
            series : [
                {
                    name:'',
                    type:'line',
                    data: value_data,
                    smooth:true,
                    markPoint : {
                        data : [
                            {type : 'max', name: '最大值'},
                            {type : 'min', name: '最小值'}
                        ]
                    },
                    markLine : {
                        data : [
                            {type : 'average', name: '平均值'}
                        ]
                    }
                },
            ]
        };
        var myChart = echarts.init(document.getElementById(div));
        myChart.setOption(option);
                    
    },

    Draw_picture: function(data){
        var Related_Node = new Array();
        var Related_Link = new Array();
        var user_name = data[0][1];
        for(var item =0; item < data.length; item++){
            Related_Node.push({'name':data[item][1], 'value':data[item][5], 'label':data[item][1]});
            Related_Link.push({'source':user_name, 'target':data[item][1], 'weight':data[item][5]});
        }
        var option = {
                title : {
                    text: '',
                    subtext: '',
                    x:'right',
                    y:'bottom'
                },
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
                    data:['家人']
                },
                series : [
                    {
                        type:'force',
                        name : "人物关系",
                        ribbonType: false,
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
                                },
                                linkStyle: {
                                    type: 'curve'
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
                        useWorker: false,
                        minRadius : 15,
                        maxRadius : 25,
                        gravity: 1.1,
                        scaling: 1.1,
                        roam: 'move',
                        nodes: Related_Node,
                        links : Related_Link,
                    }
                ]
        };  

        var myChart = echarts.init(document.getElementById('echart'));
        myChart.setOption(option);
        //回调函数，添加监听事件
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
                    } else { // 点击的是点
                    }
                }
                    myChart.on(ecConfig.EVENT.CLICK, focus)

                    myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                    });
                }
        )     
    },
}

uid_list = window.location.search;
Search_weibo = new Search_weibo();
var url_activity = '/manage/compare_user_activity/' + uid_list;
var url_profile = '/manage/compare_user_profile/'+ uid_list;
var url_portrait = '/manage/compare_user_portrait/' + uid_list;
var user_tag = '/tag/show_user_tag/'+ uid_list;
// var url_activity = '/manage/compare_user_activity/?uid_list=1642591402,2948738352';
//  = '/manage/compare_user_profile/?uid_list=1642591402,2948738352';
// var url_portrait = '/manage/compare_user_portrait/?uid_list=1642591402,2948738352';
Search_weibo.call_sync_ajax_request(url_profile, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var url_photo = Search_weibo.Return_data();
Search_weibo.call_sync_ajax_request(url_activity, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var activity = Search_weibo.Return_data();
Search_weibo.call_sync_ajax_request(url_portrait, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var portrait = Search_weibo.Return_data();
Search_weibo.call_sync_ajax_request(user_tag, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var tag_data = Search_weibo.Return_data();

function Compare(){
    var html = '';
    var num = 0;
    var j = 0;
    for(var k in url_photo){
        num += 1;
    }
    html += '<thead id="head_id">';
    html += '<tr style="background: #fafafa;"><th style="width:100px;font-size:20px;vertical-align:middle; text-align:center;"></th>';
    var i =0;
    var photos = '';
   // var person_url = "http://"+window.location.host+"/index/personal/?uid=";
    for(var k in url_photo){
        var person_url = "http://"+window.location.host+"/index/personal/?uid=";
        person_url = person_url + k;
        i += 1;
        if(url_photo[k]=='unkown'){
            photos = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
        }else{
            photos = url_photo[k];
        }
        html += '<th name="line'+ i +'" id='+k +' value='+i+'>';
        html += '<div class="panel-heading text-center">';
        html += '<div class="col-md-12">';
        html += '<a href="'+ person_url +'" target="_blank">';
        html += '<img src='+photos+' alt="" class="img-circle">';
        html += '</a>';
        html += '</div>';
        html += '<div style="float:right;margin-top:-66px">';
        html += '<a  name="line'+i+'" class="btn btn-round btn-default" style="border-radius:40px;font-size:12px;padding-top:4px;padding-bottom:0px"><i class="glyphicon glyphicon-remove"></i></a>';
        html += '</div>'
        html += '</div>';
        html += '</th>';
    }
    html += '</tr></thead><tbody>';
    html += '<tr><td colspan="'+ (num +1) +'" name="list-1" class="cate_title" style="font-size:20px"><b>基本信息</b></td></tr>';
    j = 0;
    html += '<tr class="list-1"><td class="cate_title" style="width:90px;text-align:right">昵称</td>';
    for(var k in portrait){
        if(portrait[k]['uname'] == 'unknown'){
            portrait[k]['uname'] = '未知';
        }
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['uname'] +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-1"><td class="cate_title" style="width:90px;text-align:right">注册地</td>';
    for(var k in portrait){
        if(portrait[k]['location'] = 'unknown'){
            portrait[k]['location'] = '未知';
        }
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['location'] +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-2" class="cate_title" style="font-size:20px"><b>整体评价</b></td></tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">活跃度</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['activeness'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">重要度</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['importance'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr class="list-2"><td class="cate_title" style="width:90px;text-align:right">影响力</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['influence'].toFixed(2) +'</td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-3" class="cate_title" style="font-size:20px"><b>标签属性</b></td></tr>';
    html += '<tr class="list-3"><td class="cate_title" style="width:90px;text-align:right">领域</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['domain'] +'</td>';
    }
	//html += '<td class="center" name="line1">作家</td>';
	//html += '<td class="center" name="line2">媒体</td>';
    html += '</tr>';
    j = 0;
    html += '<tr class="list-3"><td class="cate_title" style="width:90px;text-align:right">话题</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['topic'][0]+','+ portrait[k]['topic'][1]+','+portrait[k]['topic'][2]+ '</td>';
		
    }
	//html += '<td class="center" name="line1">生活</td>';
	//html += '<td class="center" name="line2">娱乐</td>';
    html += '</tr>';
    /*
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-4" class="cate_title" style="font-size:20px"><b>活跃属性</b></td></tr>';
    j = 0;
    html += '<tr class="list-4"><td class="cate_title" style="width:90px;text-align:right">活跃时间</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><a href="#activityb'+ j +'" id="control'+ j +'"><div id="activity'+ j +'" style="height:300px"></div></a></td>';
    }
    html += '</tr>';

    j = 0;
    html += '<tr class="list-4"><td class="cate_title" style="width:90px;text-align:right">活跃地区</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">';
        if(portrait[k]['activity_geo'].length == 0){
            html += '';
        }
        else{
            for(var i = 0; i < portrait[k]['activity_geo'].length; i++){
                if(i == portrait[k]['activity_geo'].length-1){
                    html += portrait[k]['activity_geo'][i];
                }else{
                    html += portrait[k]['activity_geo'][i] + ',';
                }
            }
        }
        html += '</td>';
    }
    html += '</tr>';
    */
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-5" class="cate_title" style="font-size:20px"><b>语言属性</b></td></tr>';
    html += '<tr class="list-5"><td class="cate_title" style="width:90px;text-align:right">关键词</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id="line'+ j +'" style="height:300px"></div></td>';
    }
    html += '</tr>';
    j = 0 ;
    html += '<tr class="list-5"><td class="cate_title" style="width:90px;text-align:right">hashtag</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id = "hashtag'+ j +'" style="height:200px"></div></td>';
    }
    html += '</tr>';
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-6" class="cate_title" style="font-size:20px"><b>思想属性</b></td></tr>';
    /*
    html += '<tr class="list-6"><td class="cate_title" style="width:90px;text-align:right">倾向</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id="perfer'+ j +'" style="height:300px"></div></td>';
    }
    html += '</tr>';
    */
    j = 0;
    html += '<tr class="list-6"><td class="cate_title" style="width:90px;text-align:right">心理状态</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'"><div id="emotion'+ j +'" style="height:300px"></div></td>';
    }
    html += '</tr>';
    
    j = 0;
    html += '<tr><td colspan="'+ (num+1) +'" name="list-7" class="cate_title" style="font-size:20px"><b>自定义标签</b></td></tr>';
    html += '<tr class="list-7"><td class="cate_title" style="width:90px;text-align:right">标签</td>';
    for(var k in tag_data){
        j += 1;
        html += '<td class="center" name="line'+ j +'">';
        if(tag_data[k].length == 0){
        	// html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ tag_data[k][i] +'</span>';
        	 html += '';
        }
        else{
        	for(var i = 0; i < tag_data[k].length; i++){
        		if(i == tag_data[k].length -1){
        			html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ tag_data[k][i] +'</span>';
        		}
        		else{
        			html += '<span class="input-group-addon" style="width:96px;border:1px solid white; border-radius: 8px;display:inline-block">'+ tag_data[k][i] +',</span>';
        		}
        	}
        }
    }
    html += '</tr>';
    
    html += '</tbody>';
    $('#table_compare').append(html);

    var html2 = '';
    j = 0;
    for(var k in portrait){
        j += 1;
        html2 += '<div id="activityb'+ j +'"; style="display:none;height:600px;width:1000px"></div>'
    }
    $('#picturebig').append(html2);
}
//心理状态
var SENTIMENT_DICT_NEW = {'0':'中性', '1':'积极', '2':'生气', '3':'焦虑', '4':'悲伤', '5':'厌恶', '6':'其他', '7':'消极'};
function Draw_think_emotion(psycho_status,div){
    var first_data = psycho_status['first'];
    var first = new Array();

    for(var key in first_data){
        if(key == 7){
            first.push({'name':SENTIMENT_DICT_NEW[key],'value':first_data[key].toFixed(2),selected:true});
        }else{
            first.push({'name':SENTIMENT_DICT_NEW[key],'value':first_data[key].toFixed(2)});
        } 
    }
    var second = new Array();
    var second_data = psycho_status['second'];
    second.push({'name':SENTIMENT_DICT_NEW[0],'value':first_data[0].toFixed(2)});
    second.push({'name':SENTIMENT_DICT_NEW[1],'value':first_data[1].toFixed(2)});
    for(var key in second_data){
        second.push({'name':SENTIMENT_DICT_NEW[key],'value':second_data[key].toFixed(2)});
    }
    var myChart = echarts.init(document.getElementById(div)); 
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
            data:first
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
            
            data:second
        }
    ]
}
myChart.setOption(option);  
                    
}
//话题
function Draw_think_topic(div){
    // domain_value = [];
    // domain_key = [];
    // indicate = [];
    // for ( key in data['2']){
    //      indicator = {};
    //     domain_key.push(key);
    //     indicator['text'] = key;
    //     indicator['max'] = 20;
    //     indicate.push(indicator);
    //     domain_value.push(data['2'][key]);
    // }
    var myChart = echarts.init(document.getElementById(div)); 
        
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

jQuery.fn.fancyZoom = function(options){
  
  var options   = options || {};
  // var directory = options && options.directory ? options.directory : 'images';
  var zooming   = false;

  if ($('#zoom').length == 0) {
    var html = '<div class="round_shade_box" id="zoom" style="background-color:white"> \
                    <div class="round_shade_top"> \
                        <span class="round_shade_topleft"> \</span> \
                        <span class="round_shade_topright"> \</span> \
                    </div> \
                    <div class="round_shade_centerleft"> \
                        <div class="round_shade_centerright"> \
                            <div class="round_shade_center" id="zoom_content" style = "height:600px; width:1000px"> \</div> \
                        </div> \
                    </div> \
                    <div class="round_shade_bottom"> \
                        <span class="round_shade_bottomleft"> \</span> \
                        <span class="round_shade_bottomright"> \</span> \
                    </div> \
                    <a href="#close" class="round_box_close" id="zoom_close">关闭</a> \
                </div>';
                
    $('body').append(html);
    
    $('html').click(function(e){if($(e.target).parents('#zoom:visible').length == 0) hide();});
    $(document).keyup(function(event){
        if (event.keyCode == 27 && $('#zoom:visible').length > 0) hide();
    });
    
    $('#zoom_close').click(hide);
  }
  
  var zoom          = $('#zoom');
  var zoom_close    = $('#zoom_close');
  var zoom_content  = $('#zoom_content');
  var content      ='zoom_content';
  
  this.each(function(i) {
    $($(this).attr('href')).hide();
    $(this).click(show);

  });
  $('#zoom_close').click(hide);
  return this;
  
  function show(e) {
    if (zooming) return false;
        zooming         = true;
        var content_div = $($(this).attr('href'));
        var zoom_width  = options.width;
        var zoom_height = options.height;
        
        var width       = window.innerWidth || (window.document.documentElement.clientWidth || window.document.body.clientWidth);
        var height      = window.innerHeight || (window.document.documentElement.clientHeight || window.document.body.clientHeight);
        var x           = window.pageXOffset || (window.document.documentElement.scrollLeft || window.document.body.scrollLeft);
        var y           = window.pageYOffset || (window.document.documentElement.scrollTop || window.document.body.scrollTop);
        var window_size = {'width':width, 'height':height, 'x':x, 'y':y}
    
        var width              = (zoom_width || content_div.width()) + 40;
        var height             = (zoom_height || content_div.height()) + 40;
        var d                  = window_size;
        
        // ensure that newTop is at least 0 so it doesn't hide close button
        var newTop             = Math.max((d.height/2) - (height/2) + y, 0);
        var newLeft            = (d.width/2) - (width/2);
        var curTop             = e.pageY;
        var curLeft            = e.pageX;
        
        zoom_close.attr('curTop', curTop);
        zoom_close.attr('curLeft', curLeft);
        zoom_close.attr('scaleImg', options.scaleImg ? 'true' : 'false');
        
    $('#zoom').hide().css({
            position    : 'absolute',
            top             : curTop + 'px',
            left            : curLeft + 'px',
            width     : '1px',
            height    : '1px'
        });
    
    zoom_close.hide();
    
    if (options.closeOnClick) {
      $('#zoom').click(hide);
    }
    
    if (options.scaleImg) {

        // zoom_content.html(content_div.html());
        $('#zoom_content img').css('width', '100%');
        } else {
          zoom_content.html('');
    }
    
    $('#zoom').animate({
      top     : newTop + 'px',
      left    : newLeft + 'px',
      opacity : "show",
      width   : width,
      height  : height
    }, 500, null, function() {
      if (options.scaleImg != true) {
        Search_weibo.Draw_line(options['x_data'],options['y_data'],content );
            // zoom_content.html(content_div.html());
        }
            zoom_close.show();
            zooming = false;
    })
    return false;
  }
  
  function hide() {
    if (zooming) return false;
        zooming         = true;
      $('#zoom').unbind('click');
        
        if (zoom_close.attr('scaleImg') != 'true') {
        zoom_content.html('');
        }
        zoom_close.hide();
        $('#zoom').animate({
          top     : zoom_close.attr('curTop') + 'px',
          left    : zoom_close.attr('curLeft') + 'px',
          opacity : "hide",
          width   : '1px',
          height  : '1px'
        }, 500, null, function() {
            
          if (zoom_close.attr('scaleImg') == 'true') {
                zoom_content.html('');
            }
                zooming = false;
        });
        return false;
      }
  
}

Compare();
var mark = 1;
var div ;
var m = 0;
var div2;
for(var key in portrait){
    div = 'line'+ mark;
    
    
    if(portrait[key]['keywords'].length == 0){
        $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
    }else{
        Search_weibo.Draw_cloud_keywords(portrait[key]['keywords'], div);
    }

    // div = 'topic'+ mark;
    // Draw_think_topic(div);

    div = 'emotion'+ mark;
    var psycho_status = portrait[key]['psycho_status']


    Draw_think_emotion(psycho_status,div);
    /*
    div = 'perfer'+ mark;
    Draw_think_topic(div);
    */
    div = 'hashtag'+ mark;

    if(portrait[key]['hashtag']){
        $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
    }else{
        Search_weibo.Draw_cloud_keywords(portrait[key]['hashtag'], div);
    }
    
    mark = mark + 1;
}
/*
var x_data = new Array();

for(var j =0; j < activity[2].length; j++ ){
    x_data.push(new Date(activity[2][j] * 1000).format("yyyy/MM/dd"));
}
var y_data = activity[0];

for(var key in y_data){
    m += 1;
    div = 'activity'+m;
    div2 = 'activityb'+m;
    Search_weibo.Draw_line(x_data,y_data[key],div );
    Search_weibo.Draw_line(x_data,y_data[key],div2 );
    $('#control'+m).fancyZoom({'x_data':x_data, 'y_data':y_data[key]});
   

}
 $('.btn-round').click(function(){
    
    var cell = $('#table_compare').find('th').prevAll().length;

    $('#table_compare').css('table-layout', 'fixed');
    $('[name='+ $(this).attr("name") +']').remove();
    $('#table_compare').css('table-layout', 'auto');
    $("td[name^='list-']").attr('colspan',cell);
    $('#table_compare').css('table-layout', 'fixed');
    if(cell == 1){
        $('#table_compare').css('table-layout', 'fixed');
    }
    var length = $("#head_id").find('th').length;
    for(var i = 1; i < length; i++){
        var obj = $("#head_id").find('th').eq(i);
        var uid = obj.attr('id');
        var value = obj.attr("value");
        var div = 'activity'+ value;
        var cloud_div = 'line'+value;
        var topic_div = 'topic'+ value;
        var perfer_div = 'perfer'+ value;
        var emotion_div = 'emotion' + value;
        var hashtag_div = 'hashtag'+ value ;
        Search_weibo.Draw_line(x_data, y_data[uid],div);
        if(portrait[uid]['keywords'].length == 0){
            $('#'+cloud_div).empty();
            $('#'+cloud_div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['keywords'], cloud_div);
        }
        if(portrait[uid]['hashtag'].length == 0){
            $('#'+hashtag_div).empty();
            $('#'+hashtag_div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['hashtag'], hashtag_div);
        }
        Search_weibo.Draw_think_emotion(portrait[key]['psycho_status'],emotion_div);
        // Draw_think_topic(topic_div);
        Draw_think_topic(perfer_div);
    }

 });
*/
// $("td[name^='list-']").click(function(){
//     var name = $(this).attr('name');
//     if($(this).children('a').children('i').attr('class')=='glyphicon glyphicon-chevron-up'){
//         $(this).children('a').children('i').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
//     }else{
//         $(this).children('a').children('i').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
//     }

//     $('.'+ name).each(function(){
//         if($(this).css('display') == 'table-row'){
//             $(this).css('display','none');
//         }
//         else{
//             $(this).css('display','table-row');
//         }
//     });
//  });
