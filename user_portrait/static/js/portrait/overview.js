 function Search_weibo(){
  this.ajax_method = 'GET';
}


Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    //console.log(url);
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_usernumber: function(data){
    //console.log(data);
    var in_count = data['in_count'];
    var out_count = data['out_count'];
    $('#user_num').empty();
    var html = '';
    html += '<div class="row"><div class="col-md-3 col-sm-3 col-xs-6" style="margin-left:190px"><a href="/index/recommend_in" target="_blank"class="well top-block"><i class="glyphicon glyphicon-user green"></i>';
    html += '<div>当日推荐入库人数</div>';
    html += '<div>' + in_count + '</div></a></div>';
    html += '<div class="col-md-3 col-sm-3 col-xs-6" style="margin-left:120px"><a href="/index/recommend_out" target="_blank"class="well top-block"><i class="glyphicon glyphicon-user green"></i>';
    html += '<div>当日推荐出库人数</div>';
    html += '<div>' + out_count + '</div></a></div>';
    $('#user_num').append(html);
    draw_statistics_infor(data);
    draw_sex(data);
    draw_vertify(data);
    draw_keyword(data);
    //Draw_think_emotion();
    Draw_think_domain(data);
    Draw_think_topic(data);
    draw_domain_portrait(data);
    draw_topic_portrait(data);
    draw_more_domain_portrait(data);
    draw_more_topic_portrait(data);
    draw_onlinepattern(data);
    draw_hastag(data);
    draw_top_geo(data);
    draw_retweeted_user(data);
    draw_top_comment_user(data);
    draw_importance(data);
    draw_top_influence(data);
    draw_top_activeness(data);
    draw_more_onlinepattern(data);
    draw_more_hastag(data);
    draw_more_top_geo(data);
    draw_more_retweeted_user(data);
    draw_more_top_comment_user(data);
    draw_more_importance(data);
    draw_more_top_influence(data);
    draw_more_top_activeness(data);
    //draw_top_influence_vary(data);
}
}
 
var Search_weibo = new Search_weibo(); 


$(document).ready(function(){
    var weibo_url =  "/overview/show/";
    Search_weibo.call_sync_ajax_request(weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_usernumber);
})

  function draw_statistics_infor(data){
    $('#statistics_infor').empty();
    html = '';
    html += '<div class="row"><div class="col-md-3 col-sm-3 col-xs-6"><a class="well top-block"><i class="glyphicon glyphicon-user yellow"></i>';
    html += '<div>总入库人数</div>';
    html += '<div>' + data['user_count'] + '</div></a></div>';
    html += '<div class="col-md-3 col-sm-3 col-xs-6" style="margin-left:120px"><a class="well top-block"><i class="glyphicon glyphicon-user yellow"></i>';
    html += '<div>活跃用户比重</div>';
    html += '<div>' + (Math.round(data['activity_count'] * 10000)/100).toFixed(0) + '%' + '</div></a></div>';
    html += '<div class="col-md-3 col-sm-3 col-xs-6" style="margin-left:120px"><a class="well top-block"><i class="glyphicon glyphicon-user yellow"></i>';
    html += '<div>高影响力用户比重</div>';
    html += '<div>' + (Math.round(parseFloat(data['top_influence_ratio']) * 10000)/100).toFixed(0) + '%' + '</div></a></div>';
    $('#statistics_infor').append(html);
}

function Draw_think_emotion(){
    var myChart = echarts.init(document.getElementById('user_emotion')); 
    var option = {
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    toolbox: {
        show : true,
        feature : {
            saveAsImage : {show: true}
        }
    },
    calculable : false,
    //     grid:{
    //     y:40
    // },
    series : [
        {
            name:'',
            type:'pie',
            selectedMode: 'single',
            radius : [0, 40],
            center: ['50%', '60%'],
            
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
            name:'心理状态',
            type:'pie',
            radius : [60, 80],
            center: ['50%', '60%'],
            
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

function Draw_think_topic(data){
    var myChart = echarts.init(document.getElementById('user_topic')); 
    var topics = data['topic_top'];
	var datas = [];
    for(var i = 0;i<topics.length;i++){
        datas.push({'value':topics[i][1],'name':topics[i][0]});
	}
    var option = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
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
            name:'话题',
            type:'pie',
            radius : '55%',
            center: ['60%', '60%'],
            data:datas
        }
    ]
};                    
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}
function Draw_think_domain(data){
    var myChart = echarts.init(document.getElementById('user_domain')); 
    var domains = data['domain_top'];
    var datas = [];
    for(var i = 0;i<domains.length;i++){
        datas.push({'value':domains[i][1],'name':domains[i][0]});
    }       
    var option = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
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
            name:'领域',
            type:'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:datas
        }
    ]
};
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}


function draw_domain_portrait(data){

  $('#domain_portrait').empty();
  var num = 0 
  for (key in data['domain_top_user']){ 
     num ++;
     if (num < 7){
       var html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
       html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
       html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
       html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
       for (i = 0; i<data['domain_top_user'][key].length; i++){
          var s = i.toString();
          var domain_top_username;
          var domain_top_user_portrait;
           if (data['domain_top_user'][key][s]['1'] == 'unknown'){
              domain_top_username = '未知('+data['domain_top_user'][key][s]['0']+')';
           }else{
              domain_top_username = data['domain_top_user'][key][s]['1'];
           };
           if (data['domain_top_user'][key][s]['2'] == 'unknown'){
              domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
           }else{
              domain_top_user_portrait = data['domain_top_user'][key][s]['2'];
                  };
          html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['domain_top_user'][key][s]['0'] +'" title="' + domain_top_username +'">';
          html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + domain_top_username +'"></div></a></li>';         
       }
       html += '</ul></div></div>';
       $('#domain_portrait').append(html);
   }
}
}


function draw_more_domain_portrait(data){

  $('#domain_more_portrait').empty(); 
  for (key in data['domain_top_user']){ 
       var html = '';
       html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
       html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
       html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
       html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
       for (i = 0; i<data['domain_top_user'][key].length; i++){
          var s = i.toString();
          var domain_top_username;
          var domain_top_user_portrait;
           if (data['domain_top_user'][key][s]['1'] == 'unknown'){
              domain_top_username = '未知('+data['domain_top_user'][key][s]['0']+')';
           }else{
              domain_top_username = data['domain_top_user'][key][s]['1'];
           };
           if (data['domain_top_user'][key][s]['2'] == 'unknown'){
              domain_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
           }else{
              domain_top_user_portrait = data['domain_top_user'][key][s]['2'];
           };
          html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['domain_top_user'][key][s]['0'] +'" title="' + domain_top_username +'">';
          html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + domain_top_user_portrait + '" alt="' + domain_top_username +'"></div></a></li>';         
       }
       html += '</ul></div></div>';
       $('#domain_more_portrait').append(html);
 }
}


function draw_topic_portrait(data){
  $('#topic_portrait').empty();
  var num = 0;
  for (key in data['topic_top_user']){ 
   num ++;
   if (num < 7){ 
   var html = '';
   html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
   html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
   html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
   html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
   for (i = 0; i<data['topic_top_user'][key].length; i++){
      var s = i.toString();
      var topic_top_username;
      var topic_top_user_portrait;
       if (data['topic_top_user'][key][s]['1'] == 'unknown'){
          topic_top_username = '未知('+data['topic_top_user'][key][s]['0']+')';
       }else{
          topic_top_username = data['topic_top_user'][key][s]['1'];
        };
       if (data['topic_top_user'][key][s]['2'] == 'unknown'){
          topic_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
       }else{
          topic_top_user_portrait = data['topic_top_user'][key][s]['2'];
        };
      html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['topic_top_user'][key][s]['0'] +'" title="' + topic_top_username +'">';
      html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + topic_top_user_portrait + '" alt="' + topic_top_username +'"></div></a></li>';         
   }
   html += '</ul></div></div>';
   $('#topic_portrait').append(html);
 }
}
}

function draw_more_topic_portrait(data){
  $('#topic_more_portrait').empty();
  for (key in data['topic_top_user']){ 
   var html = '';
   html += '<div ng-repeat="t in hotTopics" class="col-md-4 ng-scope"><div style="padding:5px; padding-left:15px; padding-right:15px; margin-bottom:15px" class="section-block">';
   html += '<h1 class="no-margin"><small><a style="color:#777;font-size:18px" class="ng-binding">' + key + '</a></small></h1>';
   html += '<hr style="margin-top: 5px; margin-bottom: 15px">';
   html += '<ul style="margin-top:0px;margin-bottom:0;padding-left: 7px;height:50px; overflow-y:hidden" class="list-inline">';
   for (i = 0; i<data['topic_top_user'][key].length; i++){
      var s = i.toString();
      var topic_top_username;
      var topic_top_user_portrait;
       if (data['topic_top_user'][key][s]['1'] == 'unknown'){
          topic_top_username = '未知('+data['topic_top_user'][key][s]['0']+')';
       }else{
          topic_top_username = data['topic_top_user'][key][s]['1'];
              };
       if (data['topic_top_user'][key][s]['2'] == 'unknown'){
          topic_top_user_portrait = "http://tp2.sinaimg.cn/1878376757/50/0/1";
       }else{
          topic_top_user_portrait = data['topic_top_user'][key][s]['2'];
              };
      html += '<li ng-repeat="result in t.result" target="_blank" style="margin-bottom: 10px" class="index-small-photo-wrap no-padding ng-scope"><a target="_blank" href="/index/personal/?uid=' + data['topic_top_user'][key][s]['0'] +'" title="' + topic_top_username +'">';
      html += '<div class="small-photo shadow-5"><span class="helper"></span><img src="' + topic_top_user_portrait + '" alt="' + topic_top_username +'"></div></a></li>';         
   }
   html += '</ul></div></div>';
   $('#topic_more_portrait').append(html);
 }
}


function draw_onlinepattern(data){
    $('#online_pattern').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">上网方式</th><th style="text-align:center">微博数</th></tr>';
    var row = Math.min(5,data['online_pattern_top'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['online_pattern_top'][s]['0'] +  '</th><th style="text-align:center">' + data['online_pattern_top'][s]['1'] +  '</th></tr>';
    };
    // html += '<tr><th style="text-align:center">' + 2 + '</th><th style="text-align:center">iPhone 6 Plus</th><th style="text-align:center">128625</th></tr>';
    // html += '<tr><th style="text-align:center">' + 3 + '</th><th style="text-align:center">iPhone 6</th><th style="text-align:center">48230</th></tr>';
    // html += '<tr><th style="text-align:center">' + 4 + '</th><th style="text-align:center">iPhone客户端</th><th style="text-align:center">21368</th></tr>';
    // html += '<tr><th style="text-align:center">' + 5 + '</th><th style="text-align:center">360安全浏览器</th><th style="text-align:center">13629</th></tr>';
    html += '</table>'; 
    $('#online_pattern').append(html);                  
}


function draw_more_onlinepattern(data){
    $('#more_online_pattern').empty();
    var html = '';
    html += '<table id="modal_online_pattern" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">上网方式</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data['online_pattern_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['online_pattern_top'][s]['0'] +  '</th><th style="text-align:center">' + data['online_pattern_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_online_pattern').append(html);                  
}


function draw_top_comment_user(data){
    $('#top_comment_user').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">评论量</th></tr>';
    var row = Math.min(5,data['top_comment_user'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       var top_comment_user;
       if (data['top_comment_user'][s]['1'] == 'unknown'){
          top_comment_user = '未知('+data['top_comment_user'][s]['0']+')';
       }else{
          top_comment_user = data['top_comment_user'][s]['1'];
              };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_comment_user'][s]['0'] + '">' + top_comment_user + '</a></th><th style="text-align:center">' + data['top_comment_user'][s]['3'] +  '</th></tr>';

}
    html += '</table>'; 
    $('#top_comment_user').append(html);                  
}

function draw_more_top_comment_user(data){
    $('#more_top_comment_user').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">评论量</th></tr>';
    for (var i = 0; i < data['top_comment_user'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       var more_top_comment_user;
       if (data['top_comment_user'][s]['1'] == 'unknown'){
          more_top_comment_user = '未知('+data['top_comment_user'][s]['0']+')';
       }else{
          more_top_comment_user = data['top_comment_user'][s]['1'];
              };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_comment_user'][s]['0'] + '">' + more_top_comment_user + '</a></th><th style="text-align:center">' + data['top_comment_user'][s]['3'] +  '</th></tr>';
  }
    html += '</table>'; 
    $('#more_top_comment_user').append(html);                  
}


function draw_top_influence(data){
    $('#top_influence').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">影响力</th></tr>';
    var row = Math.min(5,data['top_influence'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       var top_influence;
       if (data['top_influence'][s]['1'] == 'unknown'){
          top_influence = '未知('+data['top_influence'][s]['0']+')';
       }else{
          top_influence = data['top_influence'][s]['1'];
      };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_influence'][s]['0'] + '">' + top_influence + '</a></th><th style="text-align:center">' + data['top_influence'][s]['2'].toFixed(2) +  '</th></tr>';
  }
    html += '</table>'; 
    $('#top_influence').append(html);                  
}


function draw_top_activeness(data){
    $('#top_activeness').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th></tr>';
    var row = Math.min(5,data['top_activeness'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       var top_activeness;
       if (data['top_activeness'][s]['1'] == 'unknown'){
          top_activeness = '未知('+data['top_activeness'][s]['0']+')';
       }else{
          top_activeness = data['top_activeness'][s]['1'];
      };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_activeness'][s]['0'] + '">' + top_activeness + '</a></th><th style="text-align:center">' + data['top_activeness'][s]['2'].toFixed(2) +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_activeness').append(html);                  
}
function draw_more_top_activeness(data){
    $('#more_top_activeness').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th></tr>';
    for (var i = 0; i < data['top_activeness'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       var top_activeness;
       if (data['top_activeness'][s]['1'] == 'unknown'){
          top_activeness = '未知('+data['top_activeness'][s]['0']+')';
       }else{
          top_activeness = data['top_activeness'][s]['1'];
      };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_activeness'][s]['0'] + '">' + top_activeness + '</a></th><th style="text-align:center">' + data['top_activeness'][s]['2'].toFixed(2) +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_top_activeness').append(html);                  
}

function draw_top_influence_vary(data){
    $('#top_influence_vary').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">变动影响力</th></tr>';
    for (var i = 0; i < 5; i++) {
       var s = i.toString();
       var m = i + 1;
       if (data['top_influence_vary'][s]['1'] == 'unknown'){
          top_influence_vary = '未知('+data['top_influence_vary'][s]['0']+')';
       }else{
          top_influence_vary = data['top_influence_vary'][s]['1'];
      };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_influence_vary'][s]['0'] + '">' + top_influence_vary + '</a></th><th style="text-align:center">' + data['top_influence_vary'][s]['2'].toFixed(2) +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_influence_vary').append(html);                  
}

function draw_hastag(data){
    $('#hashtag').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">hashtag</th><th style="text-align:center">微博数</th></tr>';
    var row = Math.min(5,data['hashtag_top'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=' + data['hashtag_top'][s]['0'] +  '&adkeyword=&psycho_status=&domain=&topic=" target="_blank">' + data['hashtag_top'][s]['0'] +  '</a></th><th style="text-align:center">' + data['hashtag_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#hashtag').append(html);                  
}

function draw_more_hastag(data){
    $('#more_hashtag').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">hashtag</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data['hashtag_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=&hashtag=' + data['hashtag_top'][s]['0'] +  '&adkeyword=&psycho_status=&domain=&topic=" target="_blank">' + data['hashtag_top'][s]['0'] +  '</a></th><th style="text-align:center">' + data['hashtag_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_hashtag').append(html);                  
}

function draw_top_geo(data){
    $('#top_geo').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">活跃地</th><th style="text-align:center">人次</th></tr>';
    var row = Math.min(5,data['activity_geo_top'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=' + data['activity_geo_top'][s]['0'] +  '&hashtag=&adkeyword=&psycho_status=&domain=&topic=" target="_blank">' + data['activity_geo_top'][s]['0'] +  '</a></th><th style="text-align:center">' + data['activity_geo_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_geo').append(html);                  
}

function draw_more_top_geo(data){
    $('#more_top_geo').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">活跃地</th><th style="text-align:center">微博数</th></tr>';
    for (var i = 0; i < data['activity_geo_top'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/search_result/?stype=2&uid=&uname=&location=' + data['activity_geo_top'][s]['0'] +  '&hashtag=&adkeyword=&psycho_status=&domain=&topic=" target="_blank">' + data['activity_geo_top'][s]['0'] +  '</a></th><th style="text-align:center">' + data['activity_geo_top'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_top_geo').append(html);                  
}

function draw_more_top_influence(data){
    $('#more_top_influence').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">影响力</th></tr>';
    for (var i = 0; i < data['top_influence'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       if(data['top_influence'][s]['1']=='unknown'){
            data['top_influence'][s]['1'] = '未知('+data['top_influence'][s]['0']+')';
       }
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a href="/index/personal/?uid=' + data['top_influence'][s]['0'] +  '" target="_blank">' + data['top_influence'][s]['1'] +  '</a></th><th style="text-align:center">' + data['top_influence'][s]['2'].toFixed(2) +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_top_influence').append(html);                  
}


function draw_importance(data){
    $('#importance').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">重要度</th></tr>';
    var row = Math.min(5,data['top_importance'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       var importance;
       if (data['top_importance'][s]['1'] == 'unknown'){
          importance = '未知('+data['top_influence'][s]['0']+')';
       }else{
          importance = data['top_importance'][s]['1'];
              };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_importance'][s]['0'] + '">' + importance + '</a></th><th style="text-align:center">' + data['top_importance'][s]['2'].toFixed(2) +  '</th></tr>';
  }
    html += '</table>'; 
    $('#importance').append(html);                  
}

function draw_more_importance(data){
    $('#more_importance').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">重要度</th></tr>';
    for (var i = 0; i < data['top_importance'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       var more_importance;
       if (data['top_importance'][s]['1'] == 'unknown'){
          more_importance = '未知('+data['top_importance'][s]['0']+')';
       }else{
          more_importance = data['top_importance'][s]['1'];
       }
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_importance'][s]['0'] + '">' + more_importance + '</a></th><th style="text-align:center">' + data['top_importance'][s]['2'].toFixed(2) +  '</th></tr>';
    }
  
    html += '</table>'; 
    $('#more_importance').append(html);                  
}


function draw_retweeted_user(data){
    $('#retweeted_user').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">转发量</th></tr>';
    var row = Math.min(5,data['top_retweeted_user'].length);
    for (var i = 0; i < row; i++) {
       var s = i.toString();
       var m = i + 1;
       var top_retweeted;
       if (data['top_retweeted_user'][s]['1'] == 'unknown'){
          top_retweeted = '未知('+data['top_retweeted_user'][s]['0']+')';
       }else{
          top_retweeted = data['top_retweeted_user'][s]['1'];
       };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_retweeted_user'][s]['0'] + '">' + top_retweeted + '</a></th><th style="text-align:center">' + data['top_retweeted_user'][s]['3'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#retweeted_user').append(html);                  
}

function draw_more_retweeted_user(data){
    $('#more_retweeted_user').empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">昵称</th><th style="text-align:center">转发量</th></tr>';
    for (var i = 0; i < data['top_retweeted_user'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       var top_retweeted;
       if (data['top_retweeted_user'][s]['1'] == 'unknown'){
          top_retweeted = '未知('+data['top_retweeted_user'][s]['0']+')';
       }else{
          top_retweeted = data['top_retweeted_user'][s]['1'];
       };
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data['top_retweeted_user'][s]['0'] + '">' + top_retweeted + '</a></th><th style="text-align:center">' + data['top_retweeted_user'][s]['3'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#more_retweeted_user').append(html);                  
}

function draw_sex(data){
  var value_male = data['gender_ratio']['1'].toFixed(2);
  var value_female = data['gender_ratio']['2'].toFixed(2);
  var value_unknown = 1 - value_female - value_male;
  value_unknown = value_unknown.toFixed(2);
  var myChart = echarts.init(document.getElementById('sex')); 
  var option = {
      tooltip : {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
      },
      legend: {
          orient : 'vertical',
          x : 'left',
          data:['男(已知)','女(已知)','未知']
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
                  {value:value_male, name:'男(已知)'},
                  {value:value_female, name:'女(已知)'},
                  {value:value_unknown, name:'未知'}
              ]
          }
      ]
  }; 
   myChart.setOption(option);  
  }
function draw_vertify(data){
  var verified_yes = data['verified_ratio']['yes'].toFixed(2);
  var verified_no = data['verified_ratio']['no'].toFixed(2);
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
  //console.log(data.hashtag_top);
    var keyword = [];
    // for (key in data['hashtag_top']){
    //   var word = {};
    //   word['name'] = data['hashtag_top'][key][0];
    //   console.log(word['name']);
    //   word['value'] = data['hashtag_top'][key][1]*10;
    //   console.log(word['value']);
    //   word['itemStyle'] = createRandomItemStyle();
    //   keyword.push(word);
    // }
    //最大是20
    var key_value = [];
    var key_name = [];
    for(var i=0;i<data['hashtag_top'].length;i++){
      key_value.push(data['hashtag_top'][i][1]+Math.random());
      key_name.push(data['hashtag_top'][i][0]);
    };

    var word_num = Math.min(50, data['hashtag_top'].length);
    var key_value2 = [];
    var key_name2 = [];
    for(var i=0; i<word_num; i++){ //取前30个最大值
      a=key_value.indexOf(Math.max.apply(Math, key_value));
      key_value2.push(key_value[a]);
      key_name2.push(key_name[a]);
      key_value[a]=0;
    }
    //var word_num = Math.min(20, data.hashtag_top.length);
    //console.log(data['hashtag_top'].length);
    for (var i=0;i<word_num;i++){
      var word = {};
      word['name'] = key_name2[i];
      word['value'] =key_value2[i]*10;
      console.log(word['value']);
      word['itemStyle'] = createRandomItemStyle();
      keyword.push(word);
    }
    // console.log(keyword);
    var myChart = echarts.init(document.getElementById('keywordcloud'));
    var option = {
        tooltip: {
            show: true,
            formatter:  function (params){
              var res  = '';
              var value_after = parseInt(params.value/10);
              res += params.name+' : '+value_after;
              return res;
            }
        },
        series: [{
            //name: '关键词',
            type: 'wordCloud',
            size: ['100%', '100%'],
            textRotation : [0, 45, 90, -45],
            textPadding: 0,
            autoSize: {
                enable: true,
                minSize: 14
            },
            data:keyword
        }]
    };
                    
      myChart.setOption(option); 
                    
}                                
