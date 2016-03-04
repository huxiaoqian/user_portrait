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
          success:callback,
        });
    },
    Get_Callback_data:function(data){
        that.call_data = data
    },
    Return_data: function(){
        return that.call_data;
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
            if(keywords.length == 20){
                break;
            }
        }
        var option = {
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
                    minSize: 14,
                },
                data: keywords,
            }]
        };
        var myChart = echarts.init(document.getElementById(div));
        myChart.setOption(option);
    },
}


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
    html += '</tr>';
    j = 0;
    html += '<tr class="list-3"><td class="cate_title" style="width:90px;text-align:right">话题</td>';
    for(var k in portrait){
        j += 1;
        html += '<td class="center" name="line'+ j +'">'+ portrait[k]['topic'][0]+','+ portrait[k]['topic'][1]+','+portrait[k]['topic'][2]+ '</td>';
		
    }
    html += '</tr>';
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
function compare_extra(){
    var mark = 1;
    var div ;
    for(var key in portrait){
        div = 'line'+ mark;
        if(portrait[key]['keywords'].length == 0){
            $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['keywords'], div);
        }
        div = 'emotion'+ mark;
        var psycho_status = portrait[key]['psycho_status']
        Draw_think_emotion(psycho_status,div);
        div = 'hashtag'+ mark;

        if(portrait[key]['hashtag']){
            $('#'+div).append('<span style="display:block; padding-top:83px">该数据为空</span>');
        }else{
            Search_weibo.Draw_cloud_keywords(portrait[key]['hashtag'], div);
        }
        mark = mark + 1;
    }
}
var uid_list = window.location.search;
Search_weibo = new Search_weibo();
//心理状态
var SENTIMENT_DICT_NEW = {'0':'中性', '1':'积极', '2':'生气', '3':'焦虑', '4':'悲伤', '5':'厌恶', '6':'其他', '7':'消极'};
$('#compare_loading').showLoading();
var url_profile = '/manage/compare_user_profile/'+ uid_list;
Search_weibo.call_sync_ajax_request(url_profile, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var url_photo = Search_weibo.Return_data();

var url_portrait = '/manage/compare_user_portrait/' + uid_list;
Search_weibo.call_sync_ajax_request(url_portrait, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var portrait = Search_weibo.Return_data();

var user_tag = '/tag/show_user_tag/'+ uid_list;
Search_weibo.call_sync_ajax_request(user_tag, Search_weibo.ajax_method, Search_weibo.Get_Callback_data);
var tag_data = Search_weibo.Return_data();
Compare();
compare_extra();
$('#compare_loading').hideLoading();
