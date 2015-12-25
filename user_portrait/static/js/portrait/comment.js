 function Comment(){
  this.ajax_method = 'GET';
}
Comment.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
Draw_picture:function(data){
  //var UserID = uid;
    var UserName = document.getElementById('nickname').innerHTML;
    var number = document.getElementById('Number');
    number.innerHTML = data['out_portrait_list'].length;
   
  var items = data;
    //console.log(data[0]);
  if(items==null){
    var say = document.getElementById('test1');
    say.innerHTML = '该用户暂无此数据';
  }else{
    comment(items,uid,UserName);   
  } 
}
}
var Comment = new Comment();
Comment.call_sync_ajax_request(url, Comment.ajax_method, Comment.Draw_picture);

function comment(data,UserID,UserName){
  out_data = data['out_portrait_list'];
  in_data = data['in_portrait_list'];
  out_uids = [];
  out_unames = [];
  out_values = [];
    in_uids = [];
    in_unames = [];
    in_values = [];
  for(i=0;i<out_data.length;i++){
        out_uids.push(out_data[i][0]);
        // if(data[i][1][0] == '未知'){
        //     data[i][1][0] = "未知("+ data[i][0] +")";
        // }
        out_unames.push(out_data[i][1]);
        out_values.push(out_data[i][2]);
    }
    for(i=0;i<in_data.length;i++){
        in_uids.push(out_data[i][0]);
        in_unames.push(in_data[i][1]);
        in_values.push(in_data[i][2]);
    }
  var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
  var nod = {};
  nodeContent = []
  nod['category'] = 0;
  nod['name'] = UserName;
  nod['value'] = 10;
  nodeContent.push(nod);
    for (i=0;i<out_uids.length;i++){
            nod = {};
            //console.log(data[i][1][2]);
            nod['category'] = 2;
            nod['name'] = out_uids[i];
            nod['value'] = out_values[i];
            nod['label'] = out_unames[i];
            nodeContent.push(nod);
    }
    for (i=0;i<in_uids.length;i++){
            nod = {};
            //console.log(data[i][1][2]);
            nod['category'] = 1;
            nod['name'] = in_uids[i];
            nod['value'] = in_values[i];
            nod['label'] = in_unames[i];
            nodeContent.push(nod);
    }    
  /*for (i=0;i<uids.length;i++){
      nod = {};
      //console.log(data[i][1][2]);
      if(data[i][1][2]==0){
        nod['category'] = 2;
      }else{
        nod['category'] = 1;
      }
      nod['name'] = uids[i];
      nod['value'] = values[i];
            nod['label'] = unames[i];
      nodeContent.push(nod);
  }*/
  var linkline =[];
  for (i=0;i<in_uids.length;i++){
    line ={};
    line['source'] = in_uids[i];
    line['target'] = UserName;
    line['weight'] = 1;
    linkline.push(line);
  }
    for (i=0;i<out_uids.length;i++){
        line ={};
        line['source'] = out_uids[i];
        line['target'] = UserName;
        line['weight'] = 1;
        linkline.push(line);
    }
  var myChart1 = echarts.init(document.getElementById('test1'));
  var option = {
            title : {
                text: '粉丝',
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
  myChart1.setOption(option); 
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
                myChart1.on(ecConfig.EVENT.CLICK, focus)

                myChart1.on(ecConfig.EVENT.FORCE_LAYOUT_END, function () {
                });
            }
    )   
  
}
