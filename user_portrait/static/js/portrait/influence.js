function Bubble(){
  this.ajax_method = 'GET';
}
Bubble.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
	Draw_bubble:function(data){
		var item = data[0][0];
		var origin = [];
		for (i=7;i<15;i++){
			origin.push(item[i]);
		}
		var origin_retwitter = [];
		for (i=0;i<4;i++){
			var content = {};
			switch(i)
			{
				case 0:x="总数";break;
				case 1:x="平均数";break;
				case 2:x="最高数";break;
				case 3:x="爆发度";break;
			}
			content['name'] = x;
			var child =[];
			child[0] = {};
			child[0]['name'] = origin[i].toFixed(0);
			content['children'] = child;
			origin_retwitter.push(content);
		}
		//console.log(origin_retwitter);
		var origin_comment = [];
		for (i=4;i<8;i++){
			var content = {};
			switch(i)
			{
				case 4:x="总数";break;
				case 5:x="平均数";break;
				case 6:x="最高数";break;
				case 7:x="爆发度";break;
			}
			content['name'] = x;
			var child =[];
			child[0] = {};
			child[0]['name'] = origin[i].toFixed(0);
			content['children'] = child;
			origin_comment.push(content);
		}
		//console.log(origin_comment);
		var retwitter = [];
		for (i=15;i<item.length;i++){
			retwitter.push(item[i]);			
		}
		var retwitter_retwitter = [];
		for (i=0;i<4;i++){
			var content = {};
			switch(i)
			{
				case 0:x="总数";break;
				case 1:x="平均数";break;
				case 2:x="最高数";break;
				case 3:x="爆发度";break;
			}
			content['name'] = x;
			var child =[];
			child[0] = {};
			child[0]['name'] = retwitter[i].toFixed(0);
			content['children'] = child;
			retwitter_retwitter.push(content);
		}
		//console.log(retwitter_retwitter);
		var retwitter_comment = [];
		for (i=4;i<8;i++){
			var content = {};
			switch(i)
			{
				case 4:x="总数";break;
				case 5:x="平均数";break;
				case 6:x="最高数";break;
				case 7:x="爆发度";break;
			}
			content['name'] = x;
			var child =[];
			child[0] = {};
			child[0]['name'] = retwitter[i].toFixed(0);
			content['children'] = child;
			retwitter_comment.push(content);
		}
		//console.log(retwitter_comment);
	var tree = echarts.init(document.getElementById('treeB')); 
	var option = {
    title : {
        text: '微博统计指标'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{b}: {c}",
		backgroundColor:'rgba(0,0,0,0.7)'
    },
    toolbox: {
        show : true,
        feature : {
            saveAsImage : {show: true}
        }
    },
    calculable : false,

    series : [
        {
            name:'树图',
            type:'tree',
            orient: 'vertical',  // vertical horizontal
            rootLocation: {x:'center', y:30}, // 根节点位置  {x: 'center',y: 10}
            nodePadding: 10,
            
            symbolSize: 45,
			layerPadding:40,
            itemStyle: {
                normal: {
					color:'#add8e6',
                    label: {
                        show: true,
                        position: 'inside',
                        textStyle: {
                            color: '#EE6A50',
                            fontSize: 13,
                            fontWeight:  'bolder'
                        }
                    },
                    lineStyle: {
                        color: '#000',
                        width: 1,
                        type: 'dotted' // 'curve'|'broken'|'solid'|'dotted'|'dashed'
                    }
                },
                emphasis: {
                    label: {
                        show: true
                    }
                }
            },
            data: [
                {
                    name: '',//weibo
					symbol:'image://../../static/img/weibo.jpg',
                    children: [
                        {
                            name: '原创',
                            children: [
                                {
                                    name: '',//被转发
									symbol:'image://../../static/img/share.jpg',
									children:origin_retwitter
                                },
                                {
                                    name: '',//被评论
									symbol:'image://../../static/img/mss.jpg',
									children:origin_comment
                                }
                            ]
                        },
                        {
                            name: '转发',
							children:[
								{
									name: '',//被转发
									symbol:'image://../../static/img/share.jpg',
									children:retwitter_retwitter
								},
								{
                                    name: '',//被评论
									symbol:'image://../../static/img/mss.jpg',
									children:retwitter_comment
                                }
							]
                        }
                    ]
                }
            ]
        }
    ]
};
     tree.setOption(option); 
	}
}

var Bubble = new Bubble();
var date = new Date();
var yy = date.getFullYear();
var mm = date.getMonth()+1;
if(mm<10){
	mm = '0'+mm.toString();
}
if(dd<10){
	dd = '0'+dd.toString();
}
var dd = date.getDate();
var dateStr = "";
dateStr = yy.toString()+mm.toString()+dd.toString();

url = '/influence_application/hot_origin_weibo_brust/?date='+'20130907'+'&uid='+parent.personalData.uid ;
Bubble.call_sync_ajax_request(url, Bubble.ajax_method, Bubble.Draw_bubble);




