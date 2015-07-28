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
	var UserID = parent.personalData.uid;
	var UserName = parent.personalData.uname;
	var items = data[0];
	if(items==null){
		var say = document.getElementById('test3');
		say.innerHTML = '该用户暂无此数据';
	}else{
		attention(items,UserID,UserName);
	}	
}
}
var Attention = new Attention();
url = '/attribute/attention/?uid=1642591402' ;
Attention.call_sync_ajax_request(url, Attention.ajax_method, Attention.Draw_attention);

function attention(data,UserID,UserName){
	uids = [];
	unames = [];
	values = [];
	for(i=0;i<data.length;i++){
        uids.push(data[i][0]);
        unames.push(data[i][1][0]);
        values.push(data[i][1][1]);
    }
	var nod = {};
	nodeContent = []
	nod['category'] = 0;
	nod['name'] = UserName;
	nod['value'] = 10;
	nodeContent.push(nod);
	for (i=0;i<uids.length;i++){
			nod = {};
			nod['category'] = 1;
			nod['name'] = uids[i];
			nod['value'] = values[i];
			nodeContent.push(nod);
	}
	var linkline =[];
	for (i=0;i<unames.length;i++){
		line ={};
		line['source'] = uids[i];
		line['target'] = UserName;
		line['weight'] = 1;
		linkline.push(line);
	}
	var myChart3 = echarts.init(document.getElementById('test3'));
	var option = {
            title : {
                text: '关注',
                x:'left',
                y:'top'
            },
            legend: {
                x: 'right',
                data:['用户','朋友']
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
                            name:'朋友'
                        }
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
}

