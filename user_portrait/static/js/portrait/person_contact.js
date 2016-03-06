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
    Draw_user_tag: function(data){
      //console.log(data);
      $('#user_lable').empty();
      user_lable_html = '';
      user_lable_html += '<table id="" class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
      user_lable_html += '<thead><tr><th class="center" style="text-align:center">用户ID</th>';
      //user_lable_html += '<th class="center" style="text-align:center">昵称</th>';
      user_lable_html += '<th class="center" style="text-align:center">用户标签</th>';
      user_lable_html += '<th class="center" style="text-align:center">全选<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()"></th>';
      user_lable_html += '</tr></thead>';
      user_lable_html += '<tbody>';
      for (key in data){
       user_lable_html += '<tr>';
       user_lable_html += '<th class="center" style="text-align:center"><a target="_blank" href="/index/personal/?uid=' + key + '">' + key +'</a></th>'; 
       //user_lable_html += '<th class="center" style="text-align:center">' + data[key] + '</th>';
       user_lable_html += '<th class="center" style="text-align:center">' + data[key] + '</th>';
       user_lable_html += '<th class="center" style="text-align:center"><input name="in_status" class="in_status" type="checkbox" value="' + key + '"/></th>';
       user_lable_html += '</tr>';   
      }    
      user_lable_html += '</tbody>';
      user_lable_html += '</table>';     
      $('#user_lable').append(user_lable_html);
    },

    Draw_add_group_tag: function(data){
      var downloadurl = window.location.host;
      show_group_tag_url = 'http://' + downloadurl + '/tag/show_user_tag/?uid_list=' + id_string;
      Search_weibo.call_sync_ajax_request(show_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_user_tag);
    },

    Draw_table: function(data){
        //console.log(data);
        that.data = data;
        if(data.length == 2){
            alert("暂无相关人物！");
            return false;
        }
        $('#table').empty();
        var html = '';
        var height = 39 * (data.length-1);
        html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive" style="table-layout:fixed">';
        html += '<thead><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center; ">活跃度</th><th class="center" style="text-align:center;">重要度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">得分</th><th style="width:40px"><input name="choose_all" id="choose_all" type="checkbox" value="" onclick="choose_all()" /></th></tr></thead>';
        html += '<tbody>';
        for(var item = 1; item < data.length-1; item++){
            html += '<tr style="border-bottom:1px solid #ddd">';
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
                       save_id.push(data[item][0]);
                        html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+user_url +' target="_blank">'+ data[item][i] +'</a></td>';
                    }else{
                       html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data[item][i] +'</td>'; 
                    }
                }            
            }
            html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item + '" /></td>';
            html += '</tr>';
        }
        html += '</tbody>';
        html += '</table>';
        $('#table').css('height',height);
        $('#table').append(html);
        for (var i = 0; i < save_id.length; i++) {
            var s=i.toString();
            id_string += save_id[s] + ',';
        };
        id_string=id_string.substring(0,id_string.length-1)
    },

  Draw_attribute_name: function(data){
    $('#attribute_name').empty();
    html = '';
    html += '<select id="select_attribute_name">';

    for (var i = 0; i < data.length-1; i++) {
      var s = i.toString();
      html += '<option value="' + data[s] + '">' + data[s] + '</option>';
    }
    var t = (data.length-1).toString();
    html += '<option value="' + data[t] + '" selected="selected">' + data[t] + '</option></select>';
    $('#attribute_name').append(html);
  },

  Draw_attribute_value: function(data){
    $('#attribute_value').empty();
    html = '';
    html += '';
    html += '<select id="select_attribute_value">';
    for (var i = 0; i < data.length-1; i++) {
      var s = i.toString();
      html += '<option value="' + data[s] + '">' + data[s] + '</option>';
    }
    var t = (data.length-1).toString();
    html += '<option value="' + data[t] + '" selected="selected">' + data[t] + '</option></select>';
    $('#attribute_value').append(html);
  },

    Draw_picture: function(data){
        if(data.length == 2){
            alert("暂无相关人物！");
            return false;
        }
        var Related_Node = new Array();
        var Related_Link = new Array();
        var main_name = data[0][1];
        if(main_name == 'unknown'){
            main_name = '未知';
        }
        var user_value = 100;
        Related_Node.push({'name':data[0][0],'value':user_value,'label':main_name,'category':0,'symbolSize':2*Math.sqrt(user_value),'itemStyle':{'normal':{'color':'rgba(255,215,0,0.4)'}}});
        var user_name = data[0][0];
         var personal_url = 'http://'+ window.location.host + '/index/personal/?uid=';
        for(var item =1; item < data.length-1; item++){
            if(data[item][1]=='unknown'){
                data[item][1] = '未知';
                Related_Node.push({'name':data[item][0], 'value':data[item][5], 'label':data[item][1],'category':1,'symbolSize':2*Math.sqrt(data[item][5])});
                Related_Link.push({'source':user_name, 'target':data[item][0], 'weight':data[item][5],'itemStyle':{'normal':{'width':Math.sqrt(data[item][5])}}});
            }
            else{
                Related_Node.push({'name':data[item][0], 'value':data[item][5], 'label':data[item][1],'category':1,'symbolSize':2*Math.sqrt(data[item][5])});
                Related_Link.push({'source':user_name, 'target':data[item][0], 'weight':data[item][5],'itemStyle':{'normal':{'width':Math.sqrt(data[item][5])}}});
            }
        }
        var option = {
                title : {
                    text: '',
                    subtext: '',
                    x:'right',
                    y:'bottom'
                },
                color:['#B0E0E6','#FFC0CB'],
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
                        name : "用户id",
                        ribbonType: false,
                        categories:[
                            {
                                name:'',
                                symbol:'circle',
                            },
                            {
                                name:'',
                                symbol:'circle',
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
                        linkSymbol:'arrow',
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
var save_id = [];
var id_string = '';
var Search_weibo = new Search_weibo();
//get tag
var user_tag = '/tag/show_user_attribute_name/?uid='+ uid;
Search_weibo.call_sync_ajax_request(user_tag, Search_weibo.ajax_method, Show_tag);

Search_weibo.call_sync_ajax_request(get_choose_data(uid), Search_weibo.ajax_method, Search_weibo.Draw_table);
Search_weibo.Draw_picture(Search_weibo.data);
var show_user_tag_url = '/tag/show_user_tag/?uid_list=' + id_string;
Search_weibo.call_sync_ajax_request(show_user_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_user_tag);
var tag_url = "/tag/show_attribute_name/";
Search_weibo.call_sync_ajax_request(tag_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_name);
var select_attribute_name = $("#select_attribute_name").val()
var attribute_value_url = '';
attribute_value_url = '/tag/show_attribute_value/?attribute_name=' + select_attribute_name;
Search_weibo.call_sync_ajax_request(attribute_value_url, Search_weibo.ajax_method, Search_weibo.Draw_attribute_value);

var global_data = Search_weibo.data;

function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function Show_tag(data){
    // var height = $('#box-height').height();
    // if(data.length <=4 && data.length > 0 ){
    //     console.log('aaaaa');
    //     $('#box-height').css('height',height+20);
    // }
    // else if(data.length >4 && data.length <=8){
    //     $('#box-height').css('height',height+20*2);
    // }
    // else{
    //     $('#box-height').css('height',height+20*3);
    // }
    var html = '';
    if(data.length == 0){
      return false;
    }
    else{
      for(var i = 0; i < data.length; i++){
        html += '<div class="col-lg-3" style="margin-bottom:4px">';
        html += '<input type="checkbox" class="inline-checkbox" value="option1">';
        html += '<span class="input-group-addon" style="width:96px;border:1px solid white; background-color:white;display:inline-block" id="'+ data[i] +'">'+ data[i] +' *</span>';
        html += '<input type="text" class="form-control" style="width:40%; display:inline;height:25px;margin-left:7px" disabled>';
        html += '</div>';
      }
      html +='<div style="font-size:12px;line-height:28px;margin-left:20px;">注：带*表明此属性为自定义属性</div>'
      $('#tag').append(html);
      var each_height =  Math.ceil(data.length/4)*30 + 200;
      var height = each_height.toString() + 'px';
      $('#contact_select').css('height', height);
    }
}

function add_group_tag(){
    var select_uids = [];
    var select_uids_string = '';
    $('input[name="in_status"]:checked').each(function(){
        select_uids.push($(this).attr('value'));
    })
    //console.log(select_uids);

    for (var i = 0; i < select_uids.length; i++) {
        var s=i.toString();
        select_uids_string += select_uids[s] + ',';
    };
    var add_tag_attribute_name = $("#select_attribute_name").val();
    var add_tag_attribute_value = $("#select_attribute_value").val();
    var add_group_tag_url = '/tag/add_group_tag/?uid_list=' + select_uids_string + "&attribute_name=" + add_tag_attribute_name + "&attribute_value=" + add_tag_attribute_value;
    Search_weibo.call_sync_ajax_request(add_group_tag_url, Search_weibo.ajax_method, Search_weibo.Draw_add_group_tag);
}

$('.label-success').click(function(){
    var url = get_choose_data(uid);
    //console.log(url);
    if(url == ''){
        return false;
    }
    else{
    Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, Search_weibo.Draw_table);
    Search_weibo.Draw_picture(Search_weibo.data);
    
    ////Search_weibo.call_sync_ajax_request(url, Search_weibo.ajax_method, Search_weibo.Draw_picture);
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
            field = $(this).attr('id');
        }
    });
    if(isflag == 1){
        url = url + keywords.join(',') + '&weight=' + weight.join(',') + '&field=' +field ;
    }
    else{
        url = '';
    }
    //console.log(url);
    return url;
}

// 保留原有的html代码
//var origin_html = $('#ADD').html();

function diy_button(){
 // $('#ADD').html(origin_html);
  // var cur_uids = []
  // $('input[name="search_result_option"]:checked').each(function(){
  //     cur_uids.push($(this).attr('value'));
  // });
  // if(cur_uids.length < 1){
  //   alert('请选择至少1个用户');
  // }
  // else{
  //  $('#Diymodal').modal();
  // }
  $('#Diymodal').modal();
}


function compare_button(){
  var compare_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      compare_uids.push($(this).attr('value'));
  });
  var len = compare_uids.length;
  if(len>3 || len<2){
    alert("请选择2至3个用户！");
  }
  else{
      draw_table_compare_confirm(compare_uids, "#compare_comfirm");
      $('#compare').modal();
  }
}

function group_button(){
  var group_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      group_uids.push($(this).attr('value'));
  });
  var len = group_uids.length;
  if (len < 1){
      alert("请选择至少1个用户!");
  }
  else{
      draw_table_group_confirm(group_uids, "#group_comfirm");
      $("#group").modal();
  }
}

function choose_all(){
  $('input[name="search_result_option"]').prop('checked', $("#choose_all").prop('checked'));
}

function draw_table_compare_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="compare_cofirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">活跃度</th><th class="center" style="text-align:center;width:72px">重要度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">得分</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="compare_confirm_uids">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ item[2].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[3].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] + '</td>';
      html += '<td class="center" style="width:80px;"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function draw_table_group_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="group_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th class="center" style="text-align:center">用户id</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">活跃度</th><th class="center" style="text-align:center;width:72px">重要度</th><th class="center" style="text-align:center">影响力</th><th class="center" style="text-align:center">得分</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr">';
      html += '<td class="center" name="group_confirm_uids">'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ item[2].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[3].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center" style="width:100px;">'+ item[5] + '</td>';
      html += '<td class="center" style="width:80px;"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function delRow(obj){
  var Row = obj.parentNode;
  while(Row.tagName.toLowerCase()!="tr"){
    Row = Row.parentNode;
  }
  Row.parentNode.removeChild(Row);
}

function compare_confirm_button(){
  var compare_confirm_uids = [];
  $('[name="compare_confirm_uids"]').each(function(){
      compare_confirm_uids.push($(this).text());
  })
  if (compare_confirm_uids.length <= 1){
      alert('对比的用户至少需要2名!');
      return;
  }
  var compare_url = '/index/contrast/?uid_list='+ compare_confirm_uids.join(',');
  //console.log(compare_url);
  window.open(compare_url);
}

function group_confirm_button(){
  var group_confirm_uids = [];
  $('[name="group_confirm_uids"]').each(function(){
      group_confirm_uids.push($(this).text());
  })
  //console.log(group_confirm_uids);
  var group_ajax_url = '/group/submit_task/';
  var group_url = '/index/group/';
  var group_name = $('input[name="group_name"]').val();
  var remark = $('input[name="remark"]').val();
  //console.log(group_name, remark);
  if (group_name.length == 0){
      alert('群体名称不能为空');
      return;
  }
  //console.log(group_url);
  var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
  if (!group_name.match(reg)){
    alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if ((remark.length > 0) && (!remark.match(reg))){
    alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
    return;
  }
  if(group_confirm_uids.length <=1){
    alert("请选择至少1个用户");
    return ;
  }
  var job = {"task_name":group_name, "uid_list":group_confirm_uids, "state":remark};
  $.ajax({
      type:'POST',
      url: group_ajax_url,
      contentType:"application/json",
      data: JSON.stringify(job),
      dataType: "json",
      success: callback
  });
  function callback(data){
      //console.log(data);
      if (data == '1'){
          //console.log('seceed',group_ajax_url)
          window.location.href = group_url;
      }
      else{
          alert('已存在相同名称的群体分析任务,请重试一次!');
      }
  }
}

