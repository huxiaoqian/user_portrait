// Date format
Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}
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
  Draw_model: function(data){
    console.log(data);
    $('#group_user').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<thead><tr><th class="center" style="text-align:center">UID</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">性别</th>';
    html += '<th class="center" style="text-align:center">注册地</th><th class="center" style="text-align:center">重要度</th><th class="center" style="text-align:center;width:72px">影响力</th></tr></thead>';
    html += '<tbody>';
    for ( i=0 ; i<data.length; i++){
        s = i.toString();
        if (data[s]['2'] == 1){
            sex = '男';
        }else{
            sex = '女';
        }
      html += '<tr><th class="center" style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + data[s]['0']+ '">' + data[s]['0']+ '</a></th><th class="center" style="text-align:center">' + data[s]['1']+ '</th><th class="center" style="text-align:center">' + sex+ '</th>';
      html += '<th class="center" style="text-align:center">' + data[s]['3']+ '</th><th class="center" style="text-align:center">' + data[s]['4'].toFixed(2) + '</th><th class="center" style="text-align:center;width:72px">' + data[s]['5'].toFixed(2) + '</th></tr>';  
    };
    html += '</tbody>';
    html += '</table>';
    $('#group_user').append(html);

      },
  Draw_overview: function(data){
    $('#overview').empty();
    html = '';
    html += '<div style="height:180px;width:250px;float:left"><ul style="margin-top:-60px"><li><a href="#">';
    html += '<p style="font-size:16px">' + data[0] +'</p><p style="font-size:16px">' + data[1] +'</p><p style="font-size:16px">' + data[2] +'</p><p style="font-size:16px" data-toggle="modal" data-target="#myModal">群组成员</p>';
    html += '</a></li></ul></div>';
    html += '<table style="height:150px;width:750px;float:right">';
    html += '<tr><td style="text-align:center;vertical-align:middle"><img src="/static/img/closeness.png" style="height:80px"></td>';
    html += '<td style="text-align:center;vertical-align:middle"><img src="/static/img/activeness.png" style="height:80px"></td>';
    html += '<td style="text-align:center;vertical-align:middle"><img src="/static/img/importance.png" style="height:80px"></td>';
    html += '<td style="text-align:center;vertical-align:middle"><img src="/static/img/influence.png" style="height:80px"></td></tr>';
    html += '<tr><td style="text-align:center;vertical-align:middle">' + data[3].toFixed(2) + '</td><td style="text-align:center;vertical-align:middle">' + data[4].toFixed(2) + '</td>';
    html += '<td style="text-align:center;vertical-align:middle">' + data[5].toFixed(2) + '</td><td style="text-align:center;vertical-align:middle">' + data[6].toFixed(2) + '</td></tr>';
    html += '<tr><td style="font-size:14px;text-align:center;vertical-align:middle"><b>紧密度</b></td>';
    html += '<td style="font-size:14px;text-align:center;vertical-align:middle"><b>活跃度</b></td>';
    html += '<td style="font-size:14px;text-align:center;vertical-align:middle"><b>重要度</b></td>';
    html += '<td style="font-size:14px;text-align:center;vertical-align:middle"><b>影响度</b></td></tr>';
    html += '</table>';
    $('#overview').append(html);
},

Draw_basic: function(data){
    var myChart = echarts.init(document.getElementById('sex')); 
        var dataStyle = {
        normal: {
            label: {show:false},
            labelLine: {show:false}
        }
    };
    var placeHolderStyle = {
        normal : {
            color: 'rgba(0,0,0,0)',
            label: {show:false},
            labelLine: {show:false}
        },
        emphasis : {
            color: 'rgba(0,0,0,0)'
        }
    };
    option = {
        title: {
            text: '男女？',
            subtext: '',
            sublink: '',
            x: 'center',
            y: 'center',
            itemGap: 20,
            textStyle : {
                color : 'rgba(30,144,255,0.8)',
                fontFamily : '微软雅黑',
                fontSize : 15,
                fontWeight : 'bolder'
            }
        },
        tooltip : {
            show: true,
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : document.getElementById('main').offsetWidth / 2,
            y : 45,
            itemGap:12,
            data:['男','女']
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
        series : [
            {
                name:'',
                type:'pie',
                clockWise:false,
                radius : [60, 80],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['1'],
                        name:'男'
                    },
                    {
                        value:data['0']['2'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            },
            {
                name:'',
                type:'pie',
                clockWise:false,
                radius : [40, 60],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['2'], 
                        name:'女'
                    },
                    {
                        value:data['0']['1'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            }
        ]
    };
                        
         myChart.setOption(option);  
    },
Draw_verify: function(data){
    var myChart = echarts.init(document.getElementById('verify')); 
        var dataStyle = {
        normal: {
            label: {show:false},
            labelLine: {show:false}
        }
    };
    var placeHolderStyle = {
        normal : {
            color: 'rgba(0,0,0,0)',
            label: {show:false},
            labelLine: {show:false}
        },
        emphasis : {
            color: 'rgba(0,0,0,0)'
        }
    };
    option = {
        title: {
            text: '你认证了吗？',
            subtext: '',
            sublink: '',
            x: 'center',
            y: 'center',
            itemGap: 20,
            textStyle : {
                color : 'rgba(30,144,255,0.8)',
                fontFamily : '微软雅黑',
                fontSize : 15,
                fontWeight : 'bolder'
            }
        },
        tooltip : {
            show: true,
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient : 'vertical',
            x : document.getElementById('main').offsetWidth / 2,
            y : 45,
            itemGap:12,
            data:['已认证','未认证']
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
        series : [
            {
                name:'已认证',
                type:'pie',
                clockWise:false,
                radius : [60, 80],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['1'],
                        name:'已认证'
                    },
                    {
                        value:data['0']['2'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            },
            {
                name:'未认证',
                type:'pie',
                clockWise:false,
                radius : [40, 60],
                itemStyle : dataStyle,
                data:[
                    {
                        value:data['0']['2'], 
                        name:'未认证'
                    },
                    {
                        value:data['0']['1'],
                        name:'invisible',
                        itemStyle : placeHolderStyle
                    }
                ]
            }
        ]
    };
                        
         myChart.setOption(option);  
    },
Draw_totalnumber: function(data){
    $('#totalnumber').empty();
    html = '';
    html += '<a class="well top-block" style="height:180px;width:180;border-radius:500px">';
    html += '<i class="glyphicon glyphicon-user blue" style="margin-top:50px"></i><div>群组总人数</div>';
    html += '<div>' + data['1'] + '</div></a>';
    $('#totalnumber').append(html);
},
Draw_activity: function(data){
    data_x = [];
    data_y = [];
    for (var i = 0; i < data['1'].length; i++) {
        var s = i.toString();
        value_x = new Date(parseInt(data['1'][s]['0'])*1000).format("yyyy年MM月dd日 hh:mm:ss");
        value_y = data['1'][s]['1'];
        data_x.push(value_x);
        data_y.push(value_y);
       }
    $('#line').highcharts({
        chart: {
            type: 'spline',// line,
            animation: Highcharts.svg, // don't animate in old IE
            style: {
                fontSize: '12px',
                fontFamily: 'Microsoft YaHei'
            }},
        title: {
            text: '微博时间走势图',
            x: -20 //center
        },
        subtitle: {
            text: '',
            x: -20
        },
    lang: {
            printChart: "打印",
            downloadJPEG: "下载JPEG 图片",
            downloadPDF: "下载PDF文档",
            downloadPNG: "下载PNG 图片",
            downloadSVG: "下载SVG 矢量图",
            exportButtonTitle: "导出图片"
        },
        xAxis: {
            categories: data_x,
            labels:{
              rotation: -45,
              step: 6
            }
        },
        yAxis: {
            title: {
                text: '微博总量 (条)'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: '条',
            xDateFormat: '%Y-%m-%d %H:%M:%S'
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 0
        },
        series: [{
            name:'微博量',
            data: data_y
        }]
    });

},
Draw_top_location: function(data){
    $('#top_location').empty();
    html = '';
    html += '<div style="font-size:16px">发布地点排名</div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:400px;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">地点</th><th style="text-align:center">权重</th></tr>';
    for (var i = 0; i <  data['0'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['0'][s]['0'] + '</th><th style="text-align:center">' + data['0'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_location').append(html);
},
Draw_top_platform: function(data){
    $('#top_platform').empty();
    html = '';
    html += '<div style="font-size:16px">发布平台排名</div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="width:400px;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">平台</th><th style="text-align:center">权重</th></tr>';
    for (var i = 0; i < data['2'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['2'][s]['0'] + '</th><th style="text-align:center">' + data['2'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#top_platform').append(html);
},
Draw_social_line: function(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['0']['0'].length; i++) {
       var s = i.toString();
       x_value = data['0']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['0']['1'].length; i++) {
       var s = i.toString();
       y_value = data['0']['1'][s];
       y_data.push(y_value);
    };
    xdata = [];
    for (i = 0; i< y_data.length-1; i++){
        xdata.push(y_data[i] + '-' + y_data[i+1])
    }

    $('#social_line').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '个体节点度分布'
    },
    lang: {
            printChart: "打印",
            downloadJPEG: "下载JPEG 图片",
            downloadPDF: "下载PDF文档",
            downloadPNG: "下载PNG 图片",
            downloadSVG: "下载SVG 矢量图",
            exportButtonTitle: "导出图片"
        },
    xAxis: {
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:57//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: -90,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
},
Draw_group: function(data){
    $('#group').empty();
    html = '';
    html += '<table><tr><th style="text-align:center">群体内连接紧密度</th><th style="text-align:center">'+ data['1'].toFixed(2) +'</th></tr>';
    html += '<tr><th style="text-align:center">群体内微博转发频率</th><th style="text-align:center">'+ data['2'].toFixed(2) +'</th></tr>';
    html += '<tr><th style="text-align:center">群体内参与转发比例</th><th style="text-align:center">'+ data['3'].toFixed(2) +'</th></tr>';
    html += '</table>'; 
    $('#group').append(html);
},
Draw_think_status: function(data){
    status_value = [];
    status_key = [];
    indicate = [];
    for ( key in data['2']){
         indicator = {};
        status_key.push(key);
        indicator['text'] = key;
        indicator['max'] = 20;
        indicate.push(indicator);
        status_value.push(data['2'][key]);
    }
    var myChart = echarts.init(document.getElementById('radar_status')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['身份']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                {text : '进攻', max  : 100},
                {text : '防守', max  : 100},
                {text : '体能', max  : 100},
                {text : '速度', max  : 100},
                {text : '力量', max  : 100},
                {text : '技巧', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '身份'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
},
Draw_think_domain: function(data){
    domain_value = [];
    domain_key = [];
    indicate = [];
    for ( key in data['2']){
         indicator = {};
        domain_key.push(key);
        indicator['text'] = key;
        indicator['max'] = 20;
        indicate.push(indicator);
        domain_value.push(data['2'][key]);
    }
    var myChart = echarts.init(document.getElementById('radar_domain')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['领域']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
            indicator : [
                {text : '进攻', max  : 100},
                {text : '防守', max  : 100},
                {text : '体能', max  : 100},
                {text : '速度', max  : 100},
                {text : '力量', max  : 100},
                {text : '技巧', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '领域'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
},
Draw_think_topic: function(data){
    topic_value = [];
    topic_key = [];
    indicate = [];
    for ( key in data['2']){
         indicator = {};
        topic_key.push(key);
        indicator['text'] = key;
        indicator['max'] = 20;
        indicate.push(indicator);
        topic_value.push(data['2'][key]);
    }


    var myChart = echarts.init(document.getElementById('radar_topic')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['话题']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                {text : '进攻', max  : 100},
                {text : '防守', max  : 100},
                {text : '体能', max  : 100},
                {text : '速度', max  : 100},
                {text : '力量', max  : 100},
                {text : '技巧', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '话题'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
},
Draw_think_psycho: function(data){
    psycho_value = [];
    psycho_key = [];
    indicate = [];
    for ( key in data['2']){
        indicator = {};
        psycho_key.push(key);
        indicator['text'] = key;
        indicator['max'] = 20;
        indicate.push(indicator);
        psycho_value.push(data['2'][key]);
    }
    var myChart = echarts.init(document.getElementById('radar_psycho')); 
        
        var option = {
        title : {
            text: '',
            subtext: ''
        },
        tooltip : {
            trigger: 'axis'
        },
        legend: {
            x : 'center',
            data:['心理']
        },
        toolbox: {
            show : true,
            feature : {
                saveAsImage : {show: true}
            }
        },
        calculable : true,
        polar : [
            {
                indicator : [
                {text : '进攻', max  : 100},
                {text : '防守', max  : 100},
                {text : '体能', max  : 100},
                {text : '速度', max  : 100},
                {text : '力量', max  : 100},
                {text : '技巧', max  : 100}],
                radius : 80
            }
        ],
        series : [
            {
                name: '',
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
                        value : [97, 42, 88, 94, 90, 86],
                        name : '心理'
                    }
                ]
            }
        ]
    };                
        // 为echarts对象加载数据 
        myChart.setOption(option); 
},
Draw_hashtag: function(data){
    $('#hashtag').empty();
    html = '';
    html += '<div style="font-size:16px">Hashtag排名</div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">hashtag</th><th style="text-align:center">权重</th></tr>';
    for (var i = 0; i < data['0'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['0'][s]['0'] + '</th><th style="text-align:center">' + data['0'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#hashtag').append(html);    
},
Draw_emotion: function(data){
    $('#emotion').empty();
    html = '';
    html += '<div style="font-size:16px">表情符号排名</div>';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive;font-size:14px">';
    html += '<tr><th style="text-align:center">排名</th><th style="text-align:center">表情符号</th><th style="text-align:center">权重</th></tr>';
    for (var i = 0; i <  data['2'].length; i++) {
       var s = i.toString();
       var m = i + 1;
       html += '<tr><th style="text-align:center">' + m + '</th><th style="text-align:center">' + data['2'][s]['0'] + '</th><th style="text-align:center">' + data['2'][s]['1'] +  '</th></tr>';
    };
    html += '</table>'; 
    $('#emotion').append(html);    
},
Draw_keyword: function(data){
    keyword = [];
    for (key in data['1']){
      word = {};
      word['name'] = data['1'][key]['0'];
      word['value'] = data['1'][key]['1']*10;
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

    
},
Draw_importance: function(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['0']['0'].length; i++) {
       var s = i.toString();
       x_value = data['0']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['0']['1'].length; i++) {
       var s = i.toString();
       y_value = data['0']['1'][s].toFixed(2);
       y_data.push(y_value);
    };
    for (i = 0; i< y_data.length-1; i++){
    xdata.push(y_data[i] + '-' + y_data[i+1])
    }

    $('#importance').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '重要度分布'
    },
    lang: {
            printChart: "打印",
            downloadJPEG: "下载JPEG 图片",
            downloadPDF: "下载PDF文档",
            downloadPNG: "下载PNG 图片",
            downloadSVG: "下载SVG 矢量图",
            exportButtonTitle: "导出图片"
        },
    xAxis: {
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:64//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
},
Draw_activeness: function(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['1']['0'].length; i++) {
       var s = i.toString();
       x_value = data['1']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['1']['1'].length; i++) {
       var s = i.toString();
       y_value = data['1']['1'][s].toFixed(2);
       y_data.push(y_value);
    };
    for (i = 0; i< y_data.length-1; i++){
        xdata.push(y_data[i] + '-' + y_data[i+1])
    }

    $('#activeness').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '活跃度分布'
    },
    lang: {
        printChart: "打印",
        downloadJPEG: "下载JPEG 图片",
        downloadPDF: "下载PDF文档",
        downloadPNG: "下载PNG 图片",
        downloadSVG: "下载SVG 矢量图",
        exportButtonTitle: "导出图片"
    },
    xAxis: {
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:64//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
},
Draw_influence: function(data){
    x_data = [];
    y_data = [];
    for (var i = 0; i < data['2']['0'].length; i++) {
       var s = i.toString();
       x_value = data['2']['0'][s];
       x_data.push(x_value);
    };
    for (var i = 0; i < data['2']['1'].length; i++) {
       var s = i.toString();
       y_value = data['2']['1'][s].toFixed(2);
       y_data.push(y_value);
    };
    for (i = 0; i< y_data.length-1; i++){
        xdata.push(y_data[i] + '-' + y_data[i+1])
    }
    $('#influence').highcharts({
        chart: {
        type: 'column',
        margin: [ 50, 50, 100, 80]
    },
    title: {
        text: '影响力分布'
    },
    lang: {
            printChart: "打印",
            downloadJPEG: "下载JPEG 图片",
            downloadPDF: "下载PDF文档",
            downloadPNG: "下载PNG 图片",
            downloadSVG: "下载SVG 矢量图",
            exportButtonTitle: "导出图片"
        },
    xAxis: {
        categories: xdata,
        labels: {
            rotation: -45,
            align: 'right'
        }
    },
    yAxis: {
        min: 0,
        title: {
            text: '数量 (人)'
        }
    },
    legend: {
        enabled: false
    },
    tooltip: {
        pointFormat: '<b>{point.y:.1f} 人</b>',
    },
    plotOptions: {
           series: {
               pointPadding: 0, //数据点之间的距离值
               groupPadding: 0, //分组之间的距离值
               borderWidth: 0,
               shadow: false,
               pointWidth:64//柱子之间的距离值
           }
       },
    series: [{
        name: '',
        data: x_data ,
        dataLabels: {
            // enabled: true,
            rotation: 0,
            color: '#FFFFFF',
            align: 'right',
            x: 4,
            y: 10,
            style: {
                fontSize: '13px',
                fontFamily: '微软雅黑',
                textShadow: '0 0 3px black'
            }
        }
    }]
});
},
Draw_weibo: function(data){
    if(data['3'] == 0){
        text1 = '该微博原创微博为空';
    }else{
        text1 = '<a href="' + data['6'] + '">点击查看该微博</a>';
    };
    if(data['7'] == 0){
        text2 = '该微博原创微博为空';
    }else{
        text2 = '<a href="' + data['10'] + '">点击查看该微博</a>';
    };
    if(data['11'] == 0){
        text3 = '该微博原创微博为空';
    }else{
        text3 = '<a href="' + data['14'] + '">点击查看该微博</a>';
    };
    if(data['15'] == 0){
        text4 = '该微博原创微博为空';
    }else{
        text4 = '<a href="' + data['18'] + '">点击查看该微博</a>';
    };
    $('#weibo').empty();
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="font-size:14px">'; 
    html += '<tr><th>微博用户UID</th><th>最大条数</th><th style="text-align:center">微博查看</th></tr>';
    html += '<tr><th>' + data['5'] + '</th><th>原创微博最大转发数(' + data['3'] + ')</th><th style="text-align:center">' +  text1 + '</th></tr>';
    html += '<tr><th>' + data['9'] + '</th><th>原创微博最大评论数(' + data['7'] + ')</th><th style="text-align:center">' +  text2 +  '</th></tr>';
    html += '<tr><th>' + data['13'] + '</th><th>转发微博最大转发数(' + data['11'] + ')</th><th style="text-align:center">' +  text3 +  '</th></tr>';
    html += '<tr><th>' + data['17'] + '</th><th>转发微博最大评论数(' + data['15'] + ')</th><th style="text-align:center">' +  text4 +  '</th></tr>'
    html += '</table>';
    $('#weibo').append(html);                                
}

}
 
var Search_weibo = new Search_weibo(); 

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


$(document).ready(function(){
    //    $('.datatable').dataTable({
    //   "sDom": "<'row'<'col-md-6'l><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
    //   "sPaginationType": "bootstrap",
    //   "bSort": true, 
    //   "oLanguage": {
    //     "sLengthMenu": "_MENU_ 每页"
    //   }
    // });
	var downloadurl = window.location.host;
    weibo_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=overview";
    Search_weibo.call_sync_ajax_request(weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_overview);
    model_url =  'http://' + downloadurl + "/group/show_group_list/?task_name=" + name;
    Search_weibo.call_sync_ajax_request(model_url, Search_weibo.ajax_method, Search_weibo.Draw_model);
    basic_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=basic";
    Search_weibo.call_sync_ajax_request(basic_url, Search_weibo.ajax_method, Search_weibo.Draw_basic);
    Search_weibo.call_sync_ajax_request(basic_url, Search_weibo.ajax_method, Search_weibo.Draw_totalnumber);
    Search_weibo.call_sync_ajax_request(basic_url, Search_weibo.ajax_method, Search_weibo.Draw_verify);
    activity_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=activity";
    Search_weibo.call_sync_ajax_request(activity_url, Search_weibo.ajax_method, Search_weibo.Draw_activity);
    Search_weibo.call_sync_ajax_request(activity_url, Search_weibo.ajax_method, Search_weibo.Draw_top_location);
    Search_weibo.call_sync_ajax_request(activity_url, Search_weibo.ajax_method, Search_weibo.Draw_top_platform);
    social_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=social";
    Search_weibo.call_sync_ajax_request(social_url, Search_weibo.ajax_method, Search_weibo.Draw_social_line);
    Search_weibo.call_sync_ajax_request(social_url, Search_weibo.ajax_method, Search_weibo.Draw_group);
    think_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=think";
    Search_weibo.call_sync_ajax_request(think_url, Search_weibo.ajax_method, Search_weibo.Draw_think_status);
    Search_weibo.call_sync_ajax_request(think_url, Search_weibo.ajax_method, Search_weibo.Draw_think_domain);
    Search_weibo.call_sync_ajax_request(think_url, Search_weibo.ajax_method, Search_weibo.Draw_think_topic);
    Search_weibo.call_sync_ajax_request(think_url, Search_weibo.ajax_method, Search_weibo.Draw_think_psycho);
    text_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=text";
    Search_weibo.call_sync_ajax_request(text_url, Search_weibo.ajax_method, Search_weibo.Draw_hashtag);
    Search_weibo.call_sync_ajax_request(text_url, Search_weibo.ajax_method, Search_weibo.Draw_emotion);
    Search_weibo.call_sync_ajax_request(text_url, Search_weibo.ajax_method, Search_weibo.Draw_keyword);
    influence_url =  'http://' + downloadurl + "/group/show_group_result/?task_name=" + name + "&module=influence";
    Search_weibo.call_sync_ajax_request(influence_url, Search_weibo.ajax_method, Search_weibo.Draw_importance);
    Search_weibo.call_sync_ajax_request(influence_url, Search_weibo.ajax_method, Search_weibo.Draw_activeness);
    Search_weibo.call_sync_ajax_request(influence_url, Search_weibo.ajax_method, Search_weibo.Draw_influence);
    Search_weibo.call_sync_ajax_request(influence_url, Search_weibo.ajax_method, Search_weibo.Draw_weibo);

})

