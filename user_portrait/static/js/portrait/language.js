var keywordsCloud = parent.personalData.keywords;
var positive = parent.personalData.emotion_words['positive'];
var negative = parent.personalData.emotion_words['negative'];
var angry = parent.personalData.emotion_words['angry'];
var anxiety = parent.personalData.emotion_words['anxiety'];
var emoticon = parent.personalData.emoticon;
var hashtag = parent.personalData.hashtag_dict;
//keywords

keywords_name = 'Language'
hashtag_name = 'hashtag_words'
keywords_title = '关键词'
hashtag_title = 'hashtag'
keywords_more = 'key_WordList'
hashtag_more = 'hashtag_WordList'
Draw_keyword(keywordsCloud, keywords_name, keywords_title, keywords_more)
Draw_keyword(hashtag, hashtag_name, hashtag_title, hashtag_more)
Draw_topic()
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
function Draw_keyword(data, div_name, div_title, more_div){
	var keyword = [];

	$('#'+ more_div).empty();
    html = '';
    html += '<table class="table table-striped table-bordered" style="width:480px;">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">关键词</th><th style="text-align:center">频率</th></tr>';
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
    title: {
        text: div_title,
    },
    tooltip: {
        show: true
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

function get_radar_data (data) {
  var topic = data;
  var topic_name = [];
  var topic_value = [];
  for(var key in topic){
    topic_value.push(topic[key])
    topic_name.push(key)
  };
  var topic_value2 = [];
  var topic_name2 = [];
  for(var i=0; i<6;i++){ //取前6个最大值
    a=topic_value.indexOf(Math.max.apply(Math, topic_value))
    topic_value2.push(topic_value[a]);
    topic_name2.push(topic_name[a]);
    topic_value[a]=0;
  }
  var topic_name3 = [];
  for(var i=0;i<6;i++){ //设置最大值的话题的阈值
    var name_dict = {};
    var index = topic_name2[i];
    name_dict["text"] = index;
    name_dict["max"] = 50
    topic_name3.push(name_dict)
  }
  var topic_result = [];
  topic_result.push(topic_name3);
  topic_result.push(topic_value2);
  return topic_result;
}
function Draw_topic(){
  var topic = {'话题1':20,'话题2':23,'话题3':45,'话题4':32,'话题5':22,'话题6':40,'话题7':19,'话题8':35}
  var topic_result = [];
  topic_result = get_radar_data(topic);
  var topic_name = topic_result[0];
  console.log('aaaaaaaaaaaaaaaa')
  console.log(topic_name);
  var topic_value = topic_result[1];
  var myChart2 = echarts.init(document.getElementById('user_topic'));
  var option = {
    title : {
      text: '用户话题分布',
      subtext: ''
    },
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

/*function text2icon(text){
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


//positive
var html1 = '';
$('#con1').empty();
html1 += '<div class="Litem-list fleft">';
html1 += '<ul class="Litem">';
html1 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
if(positive.length==0){
		 html1 += '<li> <span class="fleft range">无此数据</span></li>';
}else{
	for(i=0;i<positive.length;i++){
		html1 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+positive[i][0]+'</span></li>';
	}
}
html1 += '</ul>';
html1 += '</div> ';
$('#con1').append(html1);
//negative
var html2 = '';
$('#con2').empty();
html2 += '<div class="Litem-list fleft">';
html2 += '<ul class="Litem">';
html2 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
if(negative.length==0){
	html2 += '<li> <span class="fleft range">无此数据</span></li>';
}else{
	for(i=0;i<negative.length;i++){
		html2 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+negative[i][0]+'</span></li>';
	}
}
html2 += '</ul>';
html2 += '</div> ';
$('#con2').append(html2);
//anxiety
var html3 = '';
$('#con3').empty();
html3 += '<div class="Litem-list fleft">';
html3 += '<ul class="Litem">';
html3 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
if(anxiety.length==0){
	html3 += '<li> <span class="fleft range">无此数据</span></li>';
}else{
	for(i=0;i<anxiety.length;i++){
		html3 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+anxiety[i][0]+'</span></li>';
	}
}
html3 += '</ul>';
html3 += '</div> ';
$('#con3').append(html3);
//angry
var html4 = '';
$('#con4').empty();
html4 += '<div class="Litem-list fleft">';
html4 += '<ul class="Litem">';
html4 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
if(angry.length==0){
	html4 += '<li> <span class="fleft range">无此数据</span></li>';
}else{
	for(i=0;i<angry.length;i++){
		html4 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+angry[i][0]+'</span></li>';
	}
}
html4 += '</ul>';
html4 += '</div> ';
$('#con4').append(html4);
//emoticon
var html5 = '';
$('#con5').empty();
html5 += '<div class="Litem-list fleft">';
html5 += '<ul class="Litem">';
html5 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
if(emoticon.length==0){
	html5 += '<li> <span class="fleft range">无此数据</span></li>';
}else{
	for(i=0;i<emoticon.length;i++){
		html5 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+emoticon[i][0]+ '<img src=' + text2icon(emoticon[i][0]) + ' /></span></li>';
	}
}
html5 += '</ul>';
html5 += '</div> ';
$('#con5').append(html5);
//hashtag
var html6 = '';
$('#con6').empty();
html6 += '<div class="Litem-list fleft">';
html6 += '<ul class="Litem">';
html6 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
if(hashtag.length==0){
	html6 += '<li> <span class="fleft range">无此数据</span></li>';
}else{
	for(i=0;i<hashtag.length;i++){
		html6 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+hashtag[i][0]+'</span></li>';
	}
}
html6 += '</ul>';
html6 += '</div> ';
$('#con6').append(html6);

*/


function Hashtag(){
  this.ajax_method = 'GET';
}
Hashtag.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
Draw_hashtag:function(data){
	
	
	var link = document.getElementById('linkDes');
	if(data.link_conclusion==""){
        link.innerHTML = '';
    }else{
        link.innerHTML = data.link_conclusion;
    }
	
	var emotion = document.getElementById('emotionDes');
    if(data.emotion_conclusion==""){
        emotion.innerHTML = '';
    }else{
        emotion.innerHTML = data.emotion_conclusion;
    }
	
	
}
}
var Hashtag = new Hashtag();
url = '/attribute/portrait_attribute/?uid='+parent.personalData.uid ;
Hashtag.call_sync_ajax_request(url, Hashtag.ajax_method, Hashtag.Draw_hashtag);





