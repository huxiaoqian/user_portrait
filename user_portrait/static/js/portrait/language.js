var keywordsCloud = parent.personalData.keywords;
var positive = parent.personalData.emotion_words['positive'];
var negative = parent.personalData.emotion_words['negative'];
var angry = parent.personalData.emotion_words['angry'];
var anxiety = parent.personalData.emotion_words['anxiety'];
var emoticon = parent.personalData.emoticon;
var hashtag = parent.personalData.hashtag_dict;
//keywords


Draw_keyword(keywordsCloud)
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
function Draw_keyword(data){
	keyword = [];
	
	for (i=0;i<data.length;i++){
		var word = {};
		word['name'] = data[i][0];
		word['value'] =data[i][1]*100;
		word['itemStyle'] = createRandomItemStyle();
		keyword.push(word);
	}
	var myChart = echarts.init(document.getElementById('Language')); 
	var option = {
    title: {
        text: '关键字',
    },
    tooltip: {
        show: true
    },
    series: [{
        name: 'Google Trends',
        type: 'wordCloud',
        size: ['80%', '80%'],
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
 


//positive
var html1 = '';
$('#con1').empty();
html1 += '<div class="Litem-list fleft">';
html1 += '<ul class="Litem">';
html1 += '<li> <span class="fleft range">排名</span><span class="items fleft Lkeywords">关键词</span></li>';
for(i=0;i<positive.length;i++){
   html1 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+positive[i][0]+'</span></li>';
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
for(i=0;i<negative.length;i++){
   html2 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+negative[i][0]+'</span></li>';
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
for(i=0;i<anxiety.length;i++){
   html3 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+anxiety[i][0]+'</span></li>';
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
for(i=0;i<angry.length;i++){
   html4 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+angry[i][0]+'</span></li>';
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
for (i=0;i<emoticon.length;i++){
   html5 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+emoticon[i][0]+'</span></li>';
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
for (i=0;i<hashtag.length;i++){
   html6 += '<li> <span class="fleft range">'+(i+1)+'</span><span class="items fleft Lkeywords">'+hashtag[i][0]+'</span></li>';
}
html6 += '</ul>';
html6 += '</div> ';
$('#con6').append(html6);