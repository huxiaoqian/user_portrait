
function g_basic(){
  this.ajax_method = 'GET';
}
g_basic.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  }
}
function draw_basic(data){
	draw_sex(data);
	draw_verify(data);
	Draw_totalnumber(data);
	draw_tag(data);
	//draw_tag({'user_tag':{'好':13,'中':21,'坏':9}});
}
g_basic = new g_basic();
function draw_sex(data){
	var mychart1 =  echarts.init(document.getElementById('group_sex')); 
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
	        show : false,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            magicType : {
	                show: true, 
	                type: ['pie', 'funnel'],
	                option: {
	                    funnel: {
	                        x: '25%',
	                        width: '50%',
	                        funnelAlign: 'center',
	                        max: 1548
	                    }
	                }
	            },
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    calculable : true,
	    series : [
	        {
	            name:'性别',
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
	                {value:data['gender']['1'], name:'男'},
	                {value:data['gender']['2'], name:'女'}
	            ]
	        }
	    ]
	};
	                  
  mychart1.setOption(option);
}
function draw_verify(data){
	var veri = data['verified'];
	var yes = 0;
	var no = 0;
	for (var k in veri){
		if (k == ''){
			no = veri[k];
		}else{
			yes = veri[k];
		}
	}
	var mychart1 =  echarts.init(document.getElementById('group_verify')); 
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
	        show : false,
	        feature : {
	            mark : {show: true},
	            dataView : {show: true, readOnly: false},
	            magicType : {
	                show: true, 
	                type: ['pie', 'funnel'],
	                option: {
	                    funnel: {
	                        x: '25%',
	                        width: '50%',
	                        funnelAlign: 'center',
	                        max: 1548
	                    }
	                }
	            },
	            restore : {show: true},
	            saveAsImage : {show: true}
	        }
	    },
	    calculable : true,
	    series : [
	        {
	            name:'认证情况',
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
	                            fontSize : '20',
	                            fontWeight : 'bold'
	                        }
	                    }
	                }
	            },
	            data:[
	                {value:yes, name:'已认证'},
	                {value:no, name:'未认证'}
	            ]
	        }
	    ]
	};
  mychart1.setOption(option);
}
function Draw_totalnumber(data){
    $('#totalnumber').empty();
    html = '';
    html += '<a class="well top-block" style="height: 200px;width: 200px;border-radius: 450px;margin-top: 40px;margin-left: 50px;">';
    html += '<div><img src="/static/img/user_group.png" style="height:40px;margin-top:40px"></div>';
    html += '<div>群组总人数</div>'
    html += '<div>' + data['count'] + '</div></a>';
    $('#totalnumber').append(html);
}
function toarray(a,b){
	this.names=a;
	this.num=b;
}
function draw_tag(data){
	var mychart1 = echarts.init(document.getElementById('group_tag'));
	var item = data['user_tag'];
	var items = [];
	var tagname= [];
	var tagvalue = [];
	for (var k in item){
		items.push(new toarray(k,item[k]));
	}
	items.sort(function(a,b){return a.num-b.num});
	//console.log(items);
	for (var i=0;i< items.length;i++){
		tagname.push(items[i].names);
		tagvalue.push(items[i].num);
	}
	var option = {
    tooltip : {
        trigger: 'axis',
        formatter:"{b} : {c}",
    },
    toolbox: {
        show : false,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'value',
            boundaryGap : [0, 0.01]
        }
    ],
    yAxis : [
        {
            type : 'category',
            data :tagname
        }
    ],
    series : [
        {
            // name:'2011年',
            type:'bar',
            data:tagvalue
        }
    ]
};
  mychart1.setOption(option);
}
//var basic_name=document.getElementById('').text();
//var basic_name=$("#stickynote").text();
var basic_url='/group/show_group_result/?task_name='+name;
g_basic.call_sync_ajax_request(basic_url,g_basic.ajax_method,draw_basic);
