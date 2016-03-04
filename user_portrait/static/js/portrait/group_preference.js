
function Show_pref(url,div){
    that = this;
    this.ajax_method = 'GET';
    this.div = div;
}
Show_pref.prototype = {
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
    //console.log(data);
    var keywords_data = data['keywords'];
    var keywords_name = 'Language';
    var keywords_more = 'key_WordList';
    var hashtag_data = data['hashtag'];
    var hashtag_name = 'hashtag_words';
    var hashtag_more = 'hashtag_WordList';
    var topic_data = data['topic'];
    var domain_data = data['domain'];
    Draw_keyword(keywords_data, keywords_name, keywords_more, showmore_keyWords);
    Draw_keyword(hashtag_data, hashtag_name, hashtag_more, showmore_hashtagWords);
    Draw_topic(topic_data,'preference_topic', 'topic_WordList');
    Draw_topic(domain_data,'preference_domain', 'domain_WordList');
  }
}

function show_conclusion(data){
  var html = '';
  html += '<span class="fleft" style="margin-right:10px;width:32px;height:32px;background-image:url(/static/img/warning.png);margin-top:5px;display:black;"></span>';
  //html += '<h4>'+data[0]+'<span style="color:red;">'+data[1]+'</span>，'+data[2]+'<span style="color:red;">'+data[3]+'</span>。</h4>';
  html += data;
  $("#preference_conclusion").append(html);
}

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
function Draw_keyword(data, div_name, more_div, hide_more){
  var keyword = [];
  var html = '';
  $('#'+ more_div).empty();
  if(data.length == 0){
     //console.log(div_name);
      html = '<h4 style="text-align:center;margin-top:50%;">暂无数据</h4>';
      //$('#'+ more_div).append(html);
      $('#'+ div_name).append(html);
      $('#'+ hide_more).empty();
  }else{
   
      html = '';
      html += '<table class="table table-striped table-bordered" style="width:450px;">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">频数</th></tr>';
      for (var i = 0; i < data.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data[i][0] +  '&psycho_status=&domain&topic" target="_blank">' + data[i][0] +  '</a></th><th style="text-align:center">' + data[i][1] + '</th></tr>';
      };
      html += '</table>'; 
      $('#'+ more_div).append(html);

      var word_num = Math.min(20, data.length);

    for (i=0;i<word_num;i++){
      var word = {};
      word['name'] = data[i][0];
      word['value'] =data[i][1]*100;
      word['itemStyle'] = createRandomItemStyle();
      keyword.push(word);
    }

    var myChart = echarts.init(document.getElementById(div_name)); 
    var option = {
      tooltip: {
          show: true,
          formatter:  function (params,ticket,callback){
            var res  = '';
            var value_after = params.value/100;
            res += params.name+' : '+value_after;
            return res;
          }
      },
      series: [{
          type: 'wordCloud',
          size: ['100%', '100%'],
          textRotation : [0, 45, 90, -45],
          textPadding: 0,
          autoSize: {
              enable: true,
              minSize: 14
          },
          data: keyword
      }]
    };
        myChart.setOption(option);  
  }
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
  var max_topic = 8
  if(topic.length<8){
    max_topic = topic.length;
  }
  for(var i=0;i<max_topic;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name[i];
    name_dict["text"] = index;
    name_dict["max"] = Math.max.apply(Math, topic_value).toFixed(3)+10;
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value);
  return topic_result;
}
function Draw_topic(data, radar_div, motal_div){
  var topic = [];
  var html = '';
  $('#'+ motal_div).empty();
  if(data.length == 0){
      $('#'+ motal_div).empty();
      html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      //$('#'+ more_div).append(html);
      $('#'+ radar_div).append(html);
      $('#'+ motal_div).append(html);
      //$('#'+ show_more).empty();
  }else{
      html = '';
      html += '<table class="table table-striped table-bordered" style="width:450px;">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">频率</th></tr>';
      for (var i = 0; i < data.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data[i][0] +  '&psycho_status=&domain&topic" target="_blank">' + data[i][0] +  '</a></th><th style="text-align:center">' + data[i][1].toFixed(2) + '</th></tr>';
      };
      html += '</table>'; 
      $('#'+ motal_div).append(html);
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

function show_results(data){
  show_conclusion(conclusion);
}

var Show_pref = new Show_pref();
var prefrence_url = '/group/show_group_result/?task_name='+ name +'&module=preference';
Show_pref.call_sync_ajax_request(prefrence_url, Show_pref.ajax_method, Show_pref.Draw_table);

