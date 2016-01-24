ajax_method = 'GET';
function call_sync_ajax_request(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  }


$(function() {
    $( '#dl-menu' ).dlmenu();
  });
$(".closeList").off("click").click(function(){
    $("#float-wrap").addClass("hidden");
    $("#more_topic").addClass("hidden");
    $("#more_keyWords").addClass("hidden");
    $("#more_hashtagWords").addClass("hidden");
    return false;
  });
$("#showmore_keyWords").off("click").click(function(){
    $("#float-wrap").removeClass("hidden");
    $("#more_keyWords").removeClass("hidden");
    return false;
  });

$("#showmore_hashtagWords").off("click").click(function(){
        $("#float-wrap").removeClass("hidden");
        $("#more_hashtagWords").removeClass("hidden");
        return false;
    });
$("#showmore_topic").off("click").click(function(){
        $("#float-wrap").removeClass("hidden");
        $("#more_topic").removeClass("hidden");
        return false;
    });
function show_conclusion(data){
  var html = '';
  html += '<span class="fleft" style="margin-right:10px;width:32px;height:32px;background-image:url(/static/img/warning.png);margin-top:5px;display:black;"></span>';
  html += '<h4>'+data[0]+'<span style="color:red;">'+data[1]+'</span>，'+data[2]+'<span style="color:red;">'+data[3]+'</span>。</h4>';
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
function Draw_keyword(data, div_name, more_div, more){
	var keyword = [];
  var html = '';
	$('#'+ more_div).empty();
  if(data.length == 0){
     //console.log(div_name);
      html = '<h4 style="text-align:center;margin-top:50%;">暂无数据</h4>';
      //$('#'+ more_div).append(html);
      $('#'+ div_name).append(html);
      $('#'+ more).empty();
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
          show: true
      },
      series: [{
          type: 'wordCloud',
          size: ['130%', '130%'],
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
  var topic_value2 = [];
  var topic_name2 = [];
  for(var i=0; i<8;i++){ //取前8个最大值
    a=topic_value.indexOf(Math.max.apply(Math, topic_value));
    topic_value2.push(topic_value[a].toFixed(3));
    topic_name2.push(topic_name[a]);
    topic_value[a]=0;
  }
  var topic_name3 = [];
  for(var i=0;i<8;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name2[i];
    name_dict["text"] = index;
    name_dict["max"] = Math.max.apply(Math, topic_value2).toFixed(3)+0.2;
    topic_name3.push(name_dict);
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value2);
  return topic_result;
}
function Draw_topic(data){
  var topic = [];
  var html = '';
  $('#topic_WordList').empty();
  if(data.length == 0){
     //console.log(div_name);
      html = '<h3 style="font-size:20px;text-align:center;margin-top:50%;">暂无数据</h3>';
      //$('#'+ more_div).append(html);
      $('#more_topic').append(html);
      $('#showmore_topic').empty();
  }else{
      html = '';
      html += '<table class="table table-striped table-bordered" style="width:450px;">';
      html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">频率</th></tr>';
      for (var i = 0; i < data.length; i++) {
         var s = i.toString();
         var m = i + 1;
         html += '<tr style=""><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=&adkeyword=' + data[i][0] +  '&psycho_status=&domain&topic" target="_blank">' + data[i][0] +  '</a></th><th style="text-align:center">' + data[i][1].toFixed(3) + '</th></tr>';
      };
      html += '</table>'; 
      $('#topic_WordList').append(html);
    };
  var topic_result = [];
  topic_result = get_radar_data(data);
  var topic_name = topic_result[0];
  var topic_value = topic_result[1];
  var myChart2 = echarts.init(document.getElementById('user_topic'));
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

function show_domain(data){

  // var html = '';
  //html += '<h3>用户领域分析</h3>';
  data1 = '根据注册信息分类：'+data[0][0];
  data2 = '根据转发结构分类：'+data[0][1];
  data3 = '根据发帖内容分类：'+data[0][2];
  data4 = data[1];
var myChart1 = echarts.init(document.getElementById('preference_domain')); 
var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{b}"
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
    calculable : false,

    series : [
        {
            name:'树图',
            type:'tree',
            orient: 'horizontal',  // vertical horizontal
            rootLocation: {x: 30, y: 'center'}, // 根节点位置  {x: 'center',y: 10}
            nodePadding: 50,
            symbol: 'circle',
            symbolSize: 60,
            itemStyle: {
                normal: {
                    label: {
                        show: false,
                        position: 'inside',
                        textStyle: {
                            color: '#000',
                            fontSize: 14,
                            font_family: "Microsoft YaHei UI"
                        }
                    },
                    lineStyle: {
                        color: '#000',
                        width: 1,
                        type: 'curve' // 'curve'|'broken'|'solid'|'dotted'|'dashed'
                    }
                },
                emphasis: {
                    label: {
                        show: false,
                        fontSize: 14,
                    }
                }
            },
            data: [
                {
                    name: data4,
                    //value: 2,
                    // symbolSize: [90, 70],
                    // symbol: 'image://http://www.iconpng.com/png/ecommerce-business/iphone.png',
                    itemStyle: {
                        normal: {
                           color: '#95C6E2',
                            label: {
                                show: true
                            }
                        }
                    },
                    children: [
                          {
                          name: data1,
                          symbol: 'circle',
                          symbolSize: 20,
                          value: 4,
                          itemStyle: {
                              normal: {
                                  color: '#77B1E2',
                                  label: {
                                      show: true,
                                      position: 'right'
                                  },
                                  
                              },
                              emphasis: {
                                  label: {
                                      show: false
                                  },
                                  borderWidth: 0
                              }
                          }
                        },
                          {
                          name: data2,
                          symbol: 'circle',
                          symbolSize: 20,
                          value: 4,
                          itemStyle: {
                              normal: {
                                  color: '#367FBD',
                                  label: {
                                      show: true,
                                      position: 'right'
                                  },
                                  
                              },
                              emphasis: {
                                  label: {
                                      show: false
                                  },
                                  borderWidth: 0
                              }
                          }
                        },
                          {
                          name: data3,
                          symbol: 'circle',
                          symbolSize: 20,
                          value: 4,
                          itemStyle: {
                              normal: {
                                  color: '#31708F',
                                  label: {
                                      show: true,
                                      position: 'right'
                                  },
                                  
                              },
                              emphasis: {
                                  label: {
                                      show: false
                                  },
                                  borderWidth: 0
                              }
                          }
                        }    
                    ]
                }
            ]
        }
    ]
};
   myChart1.setOption(option);               
}

function show_results(data){
  //console.log(data.results.keywords);
  var keywordsCloud = data.results.keywords;
  //console.log(keywordsCloud);
  var hashtag = data.results.hashtag;
  var topic = data.results.topic;
  var conclusion = data.description;
  var domain = data.results.domain;
  var keywords_name = 'Language';
  var hashtag_name = 'hashtag_words';
  var keywords_more = 'key_WordList';
  var hashtag_more = 'hashtag_WordList';
  var key_more = 'key_more';
  var hash_more = 'hash_more';
  Draw_keyword(keywordsCloud, keywords_name, keywords_more, key_more);
  Draw_keyword(hashtag, hashtag_name, hashtag_more, hash_more);
  Draw_topic(topic);
  show_conclusion(conclusion);
  show_domain(domain);

  var tag_vector = data.tag_vector;
  //console.log(tag_vector);
  for(var i=0; i<tag_vector.length;i++){
    if(tag_vector[i][1] == ''){
      tag_vector[i][1] = '暂无数据'
    }
    global_tag_vector.push(tag_vector[i]);
  }
  }

//var url = http://219.224.135.93:9040/index/personal/?uid=2074370833
var prefrence_url = '/attribute/preference/?uid=' + parent.personalData.uid;
call_sync_ajax_request(prefrence_url, ajax_method, show_results);

