//draw function
function Search_weibo(){
  this.ajax_method = 'GET';
  that = this ;
}

Search_weibo.prototype = {
    call_sync_ajax_request:function(url, method, callback){
        $.ajax({
          url: url,
          type: method,
          dataType: 'json',
          async: false,
          success:callback
        });
    },

    
    Return_data: function(data){
        return data;
    },
    Draw_table: function(data){
        that.data = data;
        if(data==0){
            alert("没有相关人物推荐");
            return false;
        }
        $('#table').empty();
        var html = '';
        var height = 39 * (data.length+1);
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
        html += '<thead><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">重要度</th><th class="center" style="text-align:center;width:72px">活跃度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">得分</th></tr></thead>';
        html += '<tbody>';
        for(var item in data){
            html += '<tr>';
            var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
            for(var i =0; i < data[item].length; i++){  
                if(data[item][i] == 'unknown'){
                    data[item][i] = '未知'
                }
                if(i >= 2) {
                    html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data[item][i].toFixed(2) +'</td>';
                }
                else{
                if(i == 0){
                   var user_url = personal_url + data[item][0];
                    html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+user_url +' target="_blank">'+ data[item][i] +'</a></td>';
                }else{
                   html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data[item][i] +'</td>'; 
                }
                }            
            }
            html += '</tr>';
        }
        html += '</tbody>';
        html += '</table>';
        $('#table').css('height',height);
        $('#table').append(html);
    },

Draw_picture: function(data){
        if(data==0){
            alert("");
            return false;
        }
        var Related_Node = new Array();
        var Related_Link = new Array();
        var user_name = data[0][0];
         var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
        for(var item =0; item < data.length; item++){
            if(data[item][1]=='unknown'){
                data[item][1] = '未知';
                Related_Node.push({'name':data[item][0], 'value':data[item][5], 'label':data[item][1]});
                Related_Link.push({'source':user_name, 'target':data[item][0], 'weight':data[item][5]});
            }
            else{
                Related_Node.push({'name':data[item][0], 'value':data[item][5], 'label':data[item][1]});
                Related_Link.push({'source':user_name, 'target':data[item][0], 'weight':data[item][5]});
            }
        }
        var option = {
                title : {
                    text: '',
                    subtext: '',
                    x:'right',
                    y:'bottom'
                },
                tooltip : {
                    trigger: 'item',
                    formatter: '{a} : {b}'
                },
                toolbox: {
                    show : true,
                    feature : {
                        restore : {show: true},
                        magicType: {show: true, type: ['force', 'chord']},
                        saveAsImage : {show: true}
                    }
                },
                series : [
                    {
                        type:'force',
                        name : "用户id：",
                        ribbonType: false,
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
                        nodes: Related_Node,
                        links : Related_Link,
                    }
                ]
        };  

        var myChart = echarts.init(document.getElementById('echart'));
        myChart.setOption(option);
        //回调函数，添加监听事件
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
                        var node_url = personal_url + data.name;
                        window.open(node_url);
                    }
                }
                    myChart.on(ecConfig.EVENT.CLICK, focus)

                    myChart.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                    });
                }
        )     
    }
}

var Search_weibo = new Search_weibo();
$('.label-success').click(function(){
    var url = get_choose_data(uid);
    if(url == ''){
        return false;
    }
    else{
    Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, Search_weibo.Draw_table);
    Search_weibo.Draw_picture(Search_weibo.data);
    //Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, Search_weibo.Draw_picture);
    }
});

$('.inline-checkbox').click(function(){
    if($(this).is(':checked')){
        $(this).next().next().val('1');
        $(this).next().next().attr('disabled',false);
    }
    else{
        $(this).next().next().val('');
        $(this).next().next().attr('disabled',true);
    }
});

//获取选择的条件，把参数传出获取返回值
function get_choose_data(uid){
    var url = '/manage/imagine/?uid=' + uid + '&keywords=';
    var keywords = new Array();
    var weight = new Array();
    var field ;
    var isflag = 1;
    $('.inline-checkbox').each(function(){
        if($(this).is(':checked')){
            keywords.push($(this).next().attr('id'));
            if($(this).next().next().val() > 10 || $(this).next().next().val < 1 ){
                alert("请输入1到10之间的权重");
                isflag = 0;
            }else{
                weight.push($(this).next().next().val());
            }
        }
    });
    $('[type="radio"]').each(function(){
        if($(this).is(':checked')){
            filed = $(this).attr('id');
        }
    });
    if(isflag == 1){
    url = url + keywords.join(',') + '&weight=' + weight.join(',') + '&field=' +filed ;
    }
    else{
        url = '';
    }
    return url;
}
