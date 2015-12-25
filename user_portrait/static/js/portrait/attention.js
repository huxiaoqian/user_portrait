 function Attention(){
  this.ajax_method = 'GET';
}
Attention.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
Draw_attention:function(data){
	var UserID = uid;
    var UserName = document.getElementById('nickname').innerHTML;
    var select_graph = $('input[name="graph-type"]:checked').val();
    var texts = '';
    if (select_graph == 1){texts = '转发情况';}
    else if(select_graph == 2){texts = '被转发情况';}
    else if(select_graph == 3){texts = '提及情况';}
    else if(select_graph == 4){texts = '评论情况';}
    else if(select_graph == 5){texts = '被评论情况';}
    else if(select_graph == 6){texts = '互动情况';}

	var items = data;
	if(items==null){
		var say = document.getElementById('test1');
		say.innerHTML = '该用户暂无此数据';
	}else{
		attention(items,UserID,UserName,texts);
        draw_topic(items['in_portrait_result']);
        draw_field(items['in_portrait_result']);
	}	
}
}
var Attention = new Attention();
url = '/attribute/attention/?uid='+uid+'&top_count='+select_num ;
Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);

function attention(data,UserID,UserName,texts){
    out_data = data['out_portrait_list'];
    in_data = data['in_portrait_list'];
    var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
    var nod = {};
    nodeContent = []
    nod['category'] = 0;
    nod['name'] = UserName;
    nod['value'] = 10;
    nodeContent.push(nod);
    for (i=0;i<out_data.length;i++){
            nod = {};
            //console.log(data[i][1][2]);
            nod['category'] = 2;
            nod['name'] = out_data[i][0];
            nod['label'] = out_data[i][1];
            nod['value'] = out_data[i][2];
            nodeContent.push(nod);
    }
    for (i=0;i<in_data.length;i++){
            nod = {};
            //console.log(data[i][1][2]);
            nod['category'] = 1;
            nod['name'] = in_data[i][0]
            nod['label'] = in_data[i][1];
            nod['value'] = in_data[i][2];
            nodeContent.push(nod);
    }    
    var linkline =[];
    for (i=0;i<in_data.length;i++){
        line ={};
        line['source'] = in_data[i][0];
        line['target'] = UserName;
        line['weight'] = 1;
        linkline.push(line);
    }
    for (i=0;i<out_data.length;i++){
        line ={};
        line['source'] = out_data[i][0];
        line['target'] = UserName;
        line['weight'] = 1;
        linkline.push(line);
    }
	var myChart3 = echarts.init(document.getElementById('test1'));
	var option = {
            title : {
                text: texts,
                x:'left',
                y:'top'
            },
            legend: {
                x: 'right',
                data:['用户','未入库','已入库']
            },
            series : [
                {
                    type:'force',
                    name : "人物关系",
                    ribbonType: false,
                    categories : [
                        {
                            name: '用户'
                        },
                       {
                            name:'已入库'
                        },
						{
                            name:'未入库'
                        },
                    ],
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
                    nodes:nodeContent,
                    links : linkline
                }
            ]
    };  
	myChart3.setOption(option);	
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
                    } else {
                    var node_url;
                    var weibo_url ;
                    var ajax_url ;
                    if(data.category == 0){
                        ajax_url = '/attribute/identify_uid/?uid='+UserID;
                        weibo_url = 'http://weibo.com/u/'+ UserID;
                        node_url = personal_url + UserID;
                    }else{
                        ajax_url = '/attribute/identify_uid/?uid='+data.name; 
                        weibo_url = 'http://weibo.com/u/'+ data.name;
                        node_url = personal_url + data.name;
                    }                 
                    $.ajax({
                      url: ajax_url,
                      type: 'GET',
                      dataType: 'json',
                      async: false,
                      success:function(data){
                        if(data == 1){
                            window.open(node_url);
                        }
                        else{
                            window.open(weibo_url);
                        }
                      }
                    });
                    
                }
            }
                myChart3.on(ecConfig.EVENT.CLICK, focus)

                myChart3.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                });
            }
    )   
}

function draw_topic(data){
    var myChart = echarts.init(document.getElementById('topic')); 
    var datas = data['topic'];
    var nod = {};
    var nodcontent = [];
    for(var key in datas){
        var nod = {};
        nod['name'] = key;
        nod['value'] = datas[key];
        nodcontent.push(nod);
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
            center: ['50%', '60%'],
            data:nodcontent
        }
    ]
};                    
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}

function draw_field(data){
    console.log('asdfa');
    var myChart = echarts.init(document.getElementById('field')); 
    var datas = data['domain'];
    var nod = {};
    var nodcontent = [];
    for(var key in datas){
        var nod = {};
        nod['name'] = key;
        nod['value'] = datas[key];
        nodcontent.push(nod);
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
            data:nodcontent
        }
    ]
};
        // 为echarts对象加载数据 
        myChart.setOption(option); 
}