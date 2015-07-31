 function Search_weibo(){
  this.ajax_method = 'GET';
}


Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    console.log(url);
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_usernumber: function(data){
    console.log(data);
    compute = data['compute'];
    console.log(compute);
    in_count = data['in_count'];
    out_count = data['out_count'];
    user_count = data['user_count'];
    $('#user_num').empty();
    html = '';
    html += '<div class="row"><div class="col-md-3 col-sm-3 col-xs-6"><a class="well top-block"><i class="glyphicon glyphicon-user blue"></i>';
    html += '<div>已入库人数</div>';
    html += '<div>' + user_count + '</div></a></div>';
    html += '<div class="col-md-3 col-sm-3 col-xs-6"><a class="well top-block"><i class="glyphicon glyphicon-user green"></i>';
    html += '<div>推荐入库人数</div>';
    html += '<div>' + in_count + '</div></a></div>';
    html += '<div class="col-md-3 col-sm-3 col-xs-6"><a class="well top-block"><i class="glyphicon glyphicon-user yellow"></i>';
    html += '<div>推荐出库人数</div>';
    html += '<div>' + out_count + '</div></a></div>';
    html += '<div class="col-md-3 col-sm-3 col-xs-6"><a class="well top-block"><i class="glyphicon glyphicon-user red"></i>';
    html += '<div>未启动计算人数</div>';
    html += '<div>' + compute + '</div></a></div>';
    html += ' </div>';
    $('#user_num').append(html);
    draw_sex(data);
    draw_vertify(data);
    draw_keyword(data);
    draw_onlinepattern(data);
    draw_hastag(data);
    draw_domain(data);
    draw_location(data);
    draw_topic(data);
    draw_retweeted_user(data);
    draw_domian_portrait(data);
}
}
 
var Search_weibo = new Search_weibo(); 


$(document).ready(function(){
	var downloadurl = window.location.host;
    weibo_url =  'http://' + downloadurl + "/overview/show/?date=2013-09-07";
    Search_weibo.call_sync_ajax_request(weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_usernumber);
})

function draw_domian_portrait(data){
  $('#domain_portrait').empty();
  for (key in data['domain_top_user']){  
   html = '';
   html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
   html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
   html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
   html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
   for (i = 0; i<data['domain_top_user'][key].length; i++){
      var s = i.toString();
      html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['domain_top_user'][key][s]['0'] +'" title="' + data['domain_top_user'][key][s]['1'] +'">';
      html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + data['domain_top_user'][key][s]['2'] + '" alt="' + data['domain_top_user'][key][s]['1'] +'"></div></a></li>';         
   }
   html += '</ul></div></div>';
   $('#domain_portrait').append(html);
 }
}

function draw_onlinepattern(data){
    $('#online_pattern').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">上网方式</th><th style="text-align:center">比重</th></tr>';
    for (var i = 0; i < data['online_pattern_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['online_pattern_top'][s]['0'] +  '</th><th style="text-align:center">' + data['online_pattern_top'][s]['1'] +  '</th></tr>';
    };
    html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iphone</th><th style="text-align:center">128625</th></tr>';
    html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">ipad</th><th style="text-align:center">48230</th></tr>';
    html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">huawei</th><th style="text-align:center">21368</th></tr>';
    html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">SAMSUNG</th><th style="text-align:center">13629</th></tr>';
    html += '</table>'; 
    $('#online_pattern').append(html);                  
}

function draw_hastag(data){
    $('#hashtag').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">hashtag</th><th style="text-align:center">比重</th></tr>';
    for (var i = 0; i < data['hashtag_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['hashtag_top'][s]['0'] +  '</th><th style="text-align:center">' + data['hashtag_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#hashtag').append(html);                  
}

function draw_domain(data){
    $('#domain').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">活跃地</th><th style="text-align:center">比重</th></tr>';
    for (var i = 0; i < data['activity_geo_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['activity_geo_top'][s]['0'] +  '</th><th style="text-align:center">' + data['activity_geo_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#domain').append(html);                  
}
function draw_location(data){
    $('#location').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">注册地</th><th style="text-align:center">比重</th></tr>';
    for (var i = 0; i < data['location_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       if (data['location_top'][s]['0'] == 'unknown'){
          user_location = '未知';
       }else{
          user_location = data['location_top'][s]['0'];
       };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + user_location +  '</th><th style="text-align:center">' + data['location_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#location').append(html);                  
}

function draw_topic(data){
    $('#topic').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">话题</th><th style="text-align:center">比重</th></tr>';
    for (var i = 0; i < data['topic_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       if(data['topic_top'][s]['0'] == 'education'){
          user_domain = '教育';
       }
       if(data['topic_top'][s]['0'] == 'art'){
          user_domain = '艺术';
       }
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + user_domain +  '</th><th style="text-align:center">' + data['topic_top'][s]['1'] +  '</th></tr>';
    };
    html += '<tr><th style="text-align:center">3</th><th style="text-align:center">娱乐</th><th style="text-align:center">3625</th></tr>';
    html += '<tr><th style="text-align:center">4</th><th style="text-align:center">民生</th><th style="text-align:center">3280</th></tr>';
    html += '<tr><th style="text-align:center">5</th><th style="text-align:center">交通</th><th style="text-align:center">2892</th></tr>';
    html += '</table>'; 
    $('#topic').append(html);                  
}

function draw_retweeted_user(data){
    online_pattern_top = data['top_retweeted_user'];
    $('#retweeted_user').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">转发量</th></tr>';
    for (var i = 0; i < data['top_retweeted_user'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       if (data['top_retweeted_user'][s]['1'] == 'unknown'){
          top_retweeted = '未知';
       }else{
          top_retweeted = data['top_retweeted_user'][s]['1'];
       };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_retweeted_user'][s]['0'] + '">' + top_retweeted + '</a></th><th style="text-align:center">' + data['top_retweeted_user'][s]['3'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#retweeted_user').append(html);                  
}

function draw_sex(data){
  value_male = data['gender_ratio']['1'].toFixed(2);
  value_female = data['gender_ratio']['2'].toFixed(2);
  var myChart = echarts.init(document.getElementById('sex')); 
  var option = {
      tooltip : {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      legend: {
          orient : 'vertical',
          x : 'left',
          data:['男','女']
      },
      toolbox: {
          show : true,
          feature : {
              saveAsImage : {show: true}
          }
      },
      calculable : true,
      series : [
          {
              name:'',
              type:'pie',
              radius : ['50%', '70%'],
              itemStyle : {
                  normal : {
                      label : {
                          show : false
                      },
                      labelLine : {
                          show : false
                      }
                  },
                  emphasis : {
                      label : {
                          show : true,
                          position : 'center',
                          textStyle : {
                              fontSize : '30',
                              fontWeight : 'bold'
                          }
                      }
                  }
              },
              data:[
                  {value:value_male, name:'男'},
                  {value:value_female, name:'女'}
              ]
          }
      ]
  }; 
   myChart.setOption(option);  
  }
function draw_vertify(data){
  verified_yes = data['verified_ratio']['yes'].toFixed(2);
  verified_no = data['verified_ratio']['no'].toFixed(2);
  var myChart = echarts.init(document.getElementById('vertify'));
  var option = {
      tooltip : {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      legend: {
          orient : 'vertical',
          x : 'left',
          data:['已认证','未认证']
      },
      toolbox: {
          show : true,
          feature : {
              saveAsImage : {show: true}
          }
      },
      calculable : true,
      series : [
          {
              name:'',
              type:'pie',
              radius : ['50%', '70%'],
              itemStyle : {
                  normal : {
                      label : {
                          show : false
                      },
                      labelLine : {
                          show : false
                      }
                  },
                  emphasis : {
                      label : {
                          show : true,
                          position : 'center',
                          textStyle : {
                              fontSize : '30',
                              fontWeight : 'bold'
                          }
                      }
                  }
              },
              data:[
                  {value:verified_yes, name:'已认证'},
                  {value:verified_no, name:'未认证'}
              ]
          }
      ]
  };  
   myChart.setOption(option); 
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
function draw_keyword(data){
    keyword = [];
    for (key in data['keywords_top']){
      word = {};
      word['name'] = data['keywords_top'][key]['0'];
      word['value'] = data['keywords_top'][key]['1']*10;
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
                    
}                                