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
	
	var item = data[0];
	console.log(item);
	console.log(data[1]);
	document.getElementById('sayinfluence').innerHTML = data[1];
	var tree = echarts.init(document.getElementById('treeB')); 
	var option = {
    title : {
        text: '微博统计指标'
    },
    tooltip : {
        show: false,
        /*
        trigger: 'item',
        formatter: "{b}: {c}",
		backgroundColor:'rgba(0,0,0,0.7)'
        */
    },
    toolbox: {
        show : true,
        feature : {
            saveAsImage : {show: true}
        }
    },
    calculable : false,
	legend:{
		show : true,
		orient : 'horizontal',    //'horizontal' | 'vertical'
		x : 'right',
		y : 'top',
		padding:30,
		data :[
			{
				name :'被评论',
				icon :'image://../../static/img/mss.jpg',

			},
			{
				name :'被转发',
				icon :'image://../../static/img/share.jpg',

			}
		]
	},
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
					color:'#add8e6',
                    label: {
                        show: true,
                        position: 'inside',
                        textStyle: {
                            color: '#EE6A50',
                            fontSize: 13,
                            fontWeight:  'bolder'
                        }
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
									children:[{name:'总数',children:[{name:parseInt(item.origin_weibo_retweeted_total_number.toFixed(0))}]},
										{name:'平均数',children:[{name:parseInt(item.origin_weibo_retweeted_average_number.toFixed(0))}]},
										{name:'最高数',children:[{name:parseInt(item.origin_weibo_retweeted_top_number.toFixed(0))}]},
										{name:'爆发度',children:[{name:parseInt(item.origin_weibo_retweeted_brust_average.toFixed(0))}]}
									]
                                },
                                {
                                    name: '',//被评论
									symbol:'image://../../static/img/mss.jpg',
									children:[{name:'总数',children:[{name:parseInt(item.origin_weibo_comment_total_number.toFixed(0))}]},
										{name:'平均数',children:[{name:parseInt(item.origin_weibo_comment_average_number.toFixed(0))}]},
										{name:'最高数',children:[{name:parseInt(item.origin_weibo_comment_top_number.toFixed(0))}]},
										{name:'爆发度',children:[{name:parseInt(item.origin_weibo_comment_brust_average.toFixed(0))}]}
									]
                                }
                            ]
                        },
                        {
                            name: '转发',
							children:[
								{
									name: '',//被转发
									symbol:'image://../../static/img/share.jpg',
									children:[{name:'总数',children:[{name:parseInt(item.retweeted_weibo_retweeted_total_number.toFixed(0))}]},
										{name:'平均数',children:[{name:parseInt(item.retweeted_weibo_retweeted_average_number.toFixed(0))}]},
										{name:'最高数',children:[{name:parseInt(item.retweeted_weibo_retweeted_top_number.toFixed(0))}]},
										{name:'爆发度',children:[{name:parseInt(item.retweeted_weibo_retweeted_brust_average.toFixed(0))}]}
									]
								},
								{
                                    name: '',//被评论
									symbol:'image://../../static/img/mss.jpg',
									children:[{name:'总数',children:[{name:parseInt(item.retweeted_weibo_comment_total_number.toFixed(0))}]},
										{name:'平均数',children:[{name:parseInt(item.retweeted_weibo_comment_average_number.toFixed(0))}]},
										{name:'最高数',children:[{name:parseInt(item.retweeted_weibo_comment_top_number.toFixed(0))}]},
										{name:'爆发度',children:[{name:parseInt(item.retweeted_weibo_comment_brust_average.toFixed(0))}]}
									]
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
var dd = date.getDate();
if(dd<10){
	dd = '0'+dd.toString();
}
var dateStr = "";
dateStr = yy.toString()+'-'+ mm.toString()+'-'+dd.toString();
//console.log(dateStr);
url = '/influence_application/specified_user_active/?date='+'2013-09-07'+'&uid='+parent.personalData.uid ;
Bubble.call_sync_ajax_request(url, Bubble.ajax_method, Bubble.Draw_bubble);




