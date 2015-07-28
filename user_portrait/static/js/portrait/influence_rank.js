function Search_weibo_total(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_total.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="total_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>排名</th><th>头像</th><th>用户ID</th><th>昵称</th><th>影响力</th><th>入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      var select_range = $('input[name="range_select"]:checked').val();
      if(select_range==1)
        user_url = '/index/personal/?uid=';
      else
        user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][2];
      var status = '';
      if(item[i][5]==0)
        status = '未入库';
      else if(item[i][5]==1)
        status = '已入库';
      else
        status = 'error!'
      html += '<tr>';
      html += '<td class="center">'+ item[i][0] +'</td>';
      html += '<td class="center"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center"><a href='+ user_url+ '  target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '<td class="center">'+ status +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  },
  Re_Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="total_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>排名</th><th>头像</th><th>用户ID</th><th>昵称</th><th>影响力</th><th>入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      var select_range = $('input[name="range_select"]:checked').val();
      if(select_range==1)
        user_url = '/index/personal/?uid=';
      else
        user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][2];
      var status = '';
      if(item[i][5]==0)
        status = '未入库';
      else if(item[i][5]==1)
        status = '已入库';
      else
        status = 'error!'
      html += '<tr>';
      html += '<td class="center">'+ item[i][0] +'</td>';
      html += '<td class="center"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center"><a href='+ user_url+ '  target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '<td class="center">'+ status +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#total_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function Search_weibo_domain(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_domain.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="domain_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>排名</th><th>头像</th><th>用户ID</th><th>昵称</th><th>影响力</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      user_url = '/index/personal/?uid=';
      user_url = user_url + item[i][2];
      html += '<tr>';
      html += '<td class="center">'+ item[i][0] +'</td>';
      html += '<td class="center"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center"><a href='+ user_url+ '  target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  },
  Re_Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="domain_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>排名</th><th>头像</th><th>用户ID</th><th>昵称</th><th>影响力</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      if(item[i][4]!='未知')
        item[i][4] = item[i][4].toFixed(2);
      user_url = '/index/personal/?uid=';
      user_url = user_url + item[i][2];
      html += '<tr>';
      html += '<td class="center">'+ item[i][0] +'</td>';
      html += '<td class="center"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center"><a href='+ user_url+ '  target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#domain_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function Search_weibo_change(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_change.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="change_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>排名</th><th>头像</th><th>用户ID</th><th>昵称</th><th>变动名次</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      var select_change = $('input[name="change_select"]:checked').val();
      if(select_change==1)
        user_url = '/index/personal/?uid=';
      else
        user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][2];
      html += '<tr>';
      html += '<td class="center">'+ item[i][0] +'</td>';
      html += '<td class="center"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center"><a href='+ user_url+ '  target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  },
  Re_Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="change_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>排名</th><th>头像</th><th>用户ID</th><th>昵称</th><th>变动名次</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][1]=="未知")
        item[i][1] = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
      var select_change = $('input[name="change_select"]:checked').val();
      if(select_change==1)
        user_url = '/index/personal/?uid=';
      else
        user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][2];
      html += '<tr>';
      html += '<td class="center">'+ item[i][0] +'</td>';
      html += '<td class="center"><img src="'+ item[i][1] +'" class="img-circle"></td>';
      html += '<td class="center"><a href='+ user_url+ '  target="_blank">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#change_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

$("#range").empty();
var range_html = '';
range_html += '<input type="radio" name="range_select" checked value="0" /> 全网';
range_html += '<input type="radio" name="range_select" value="1" style="margin-left:5px" /> 人物库';
$("#range").append(range_html);

$("#change").empty();
var change_html = '';
change_html += '<input type="radio" name="change_select" checked value="0" /> 全网';
change_html += '<input type="radio" name="change_select" value="1" style="margin-left:5px" /> 人物库';
$("#change").append(change_html);

$("#domain").empty();
var domain_html = '';
domain_html += '<select id="domain_select">';
domain_html += '<option value="0" selected="selected">文化</option>';
domain_html += '<option value="1">教育</option>';
domain_html += '<option value="2">娱乐</option>';
domain_html += '<option value="3">时尚</option>';
domain_html += '<option value="4">财经</option>';
domain_html += '<option value="5">媒体</option>';
domain_html += '<option value="6">体育</option>';
domain_html += '<option value="7">科技</option>';
domain_html += '</select>';
$("#domain").append(domain_html);

$('input[name="range_select"]').click(function(){
  var select_range = $('input[name="range_select"]:checked').val();
  var url_total_new = '';
  var select_total_date = $("#total_date_select").val()
  if(select_range==0)
    url_total_new = '/influence_application/all_active_rank/?date=' + select_total_date;
  else
    url_total_new = '/influence_application/portrait_user_in_active/?date=' + select_total_date;
  console.log(url_total_new);
  draw_table_total_new = new Search_weibo_total(url_total_new, '#total_rank');
  draw_table_total_new.call_sync_ajax_request(url_total_new, draw_table_total_new.ajax_method, draw_table_total_new.Re_Draw_table);
});

$('input[name="change_select"]').click(function(){
  var select_change = $('input[name="change_select"]:checked').val();
  var url_change_new = '';
  if(select_change==0)
    url_change_new = '/influence_application/vary_top_k/';
  else
    url_change_new = '/influence_application/portrait_user_in_vary/';
  console.log(url_change_new);
  draw_table_change_new = new Search_weibo_change(url_change_new, '#change_rank');
  draw_table_change_new.call_sync_ajax_request(url_change_new, draw_table_change_new.ajax_method, draw_table_change_new.Re_Draw_table);
});

$('#domain_button').click(function(){
  var url_domain_new = '/influence_application/domain_rank/?date=' + $("#domain_date_select").val() + '&domain=' + $("#domain_select").val();
  draw_table_domain_new = new Search_weibo_domain(url_domain_new, '#domain_rank');
  draw_table_domain_new.call_sync_ajax_request(url_domain_new, draw_table_domain_new.ajax_method, draw_table_domain_new.Re_Draw_table);
});

var tomorrow = new Date(2013,8,8);
var now_date = new Date(tomorrow-24*60*60*1000);
var now = now_date.getFullYear()+"-"+((now_date.getMonth()+1)<10?"0":"")+(now_date.getMonth()+1)+"-"+((now_date.getDate())<10?"0":"")+(now_date.getDate());

var url_total = '/influence_application/all_active_rank/?date=' + now;
draw_table_total = new Search_weibo_total(url_total, '#total_rank');
draw_table_total.call_sync_ajax_request(url_total, draw_table_total.ajax_method, draw_table_total.Draw_table);

var url_domain = '/influence_application/domain_rank/?date=' + now;
draw_table_domain = new Search_weibo_domain(url_domain, '#domain_rank');
draw_table_domain.call_sync_ajax_request(url_domain, draw_table_domain.ajax_method, draw_table_domain.Draw_table);

var url_change = '/influence_application/vary_top_k/';
draw_table_change = new Search_weibo_change(url_change, '#change_rank');
draw_table_change.call_sync_ajax_request(url_change, draw_table_change.ajax_method, draw_table_change.Draw_table);

var total_date = [];
for(var i=0;i<7;i++){
  var today = new Date(tomorrow-24*60*60*1000*(7-i));
  total_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
}
$("#total_date").empty();
var total_date_html = '';
total_date_html += '<select id="total_date_select">';
total_date_html += '<option value="' + total_date[0] + '">' + total_date[0] + '</option>';
total_date_html += '<option value="' + total_date[1] + '">' + total_date[1] + '</option>';
total_date_html += '<option value="' + total_date[2] + '">' + total_date[2] + '</option>';
total_date_html += '<option value="' + total_date[3] + '">' + total_date[3] + '</option>';
total_date_html += '<option value="' + total_date[4] + '">' + total_date[4] + '</option>';
total_date_html += '<option value="' + total_date[5] + '">' + total_date[5] + '</option>';
total_date_html += '<option value="' + total_date[6] + '" selected="selected">' + total_date[6] + '</option>';
total_date_html += '</select>';
$("#total_date").append(total_date_html);

var domain_date = [];
for(var i=0;i<7;i++){
  var today = new Date(tomorrow-24*60*60*1000*(7-i));
  domain_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
}
$("#domain_date").empty();
var domain_date_html = '';
domain_date_html += '<select id="domain_date_select">';
domain_date_html += '<option value="' + domain_date[0] + '">' + domain_date[0] + '</option>';
domain_date_html += '<option value="' + domain_date[1] + '">' + domain_date[1] + '</option>';
domain_date_html += '<option value="' + domain_date[2] + '">' + domain_date[2] + '</option>';
domain_date_html += '<option value="' + domain_date[3] + '">' + domain_date[3] + '</option>';
domain_date_html += '<option value="' + domain_date[4] + '">' + domain_date[4] + '</option>';
domain_date_html += '<option value="' + domain_date[5] + '">' + domain_date[5] + '</option>';
domain_date_html += '<option value="' + domain_date[6] + '" selected="selected">' + domain_date[6] + '</option>';
domain_date_html += '</select>';
$("#domain_date").append(domain_date_html);

$('#total_date_button').click(function(){
  //console.log($("#total_date_select").val());
  var url_total_new = '/influence_application/all_active_rank/?date=' + $("#total_date_select").val();
  draw_table_total_new = new Search_weibo_total(url_total_new, '#total_rank');
  draw_table_total_new.call_sync_ajax_request(url_total_new, draw_table_total_new.ajax_method, draw_table_total_new.Re_Draw_table);
  prepare_rank_distribution();
});

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}

function draw_rank_distribution(axis, data1, data2, div, number_all, number_in){
  var option = {
    title : {
        text: '用户影响力分布',
        subtext: '影响力<500：全网' + number_all + '人，人物库' + number_in + '人'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['全网','人物库']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [
        {
            type : 'category',
            data : axis,
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'全网',
            type:'bar',
            data:data1,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name: '平均值'}
                ]
            }
        },
        {
            name:'人物库',
            type:'bar',
            data:data2,
            markPoint : {
                data : [
                    {type : 'max', name: '最大值'},
                    {type : 'min', name: '最小值'}
                ]
            },
            markLine : {
                data : [
                    {type : 'average', name : '平均值'}
                ]
            }
        }
    ]
  };
  var draw_init = echarts.init(document.getElementById(div));
  draw_init.setOption(option);
}

function prepare_rank_distribution(){
  var influence_bar_axis = [];
  var influence_bar_all = [];
  var influence_bar_in = [];
  var low_number_all = 0;
  var low_number_in = 0;

  var url_rank_distribution_all = '/influence_application/user_index_distribution/?date=' + $("#total_date_select").val();
  $.ajax({
    url: url_rank_distribution_all,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:callback_all
  });

  function callback_all(data1){
    for(var i=3;i<(data1[0].length-1);i++)
      influence_bar_axis.push(data1[0][i]+'-'+data1[0][i+1]);
    low_number_all = data1[1][0]+data1[1][1]+data1[1][2];
    for(var j=3;j<data1[1].length;j++)
      influence_bar_all.push(data1[1][j]);
  }

  var url_rank_distribution_in = '/influence_application/portrait_user_index_distribution/?date=' + $("#total_date_select").val();
  $.ajax({
    url: url_rank_distribution_in,
    type: 'GET',
    dataType: 'json',
    async: false,
    success:callback_in
  });

  function callback_in(data2){
    low_number_in = data2[1][0]+data2[1][1]+data2[1][2];
    for(var k=3;k<data2[1].length;k++)
      influence_bar_in.push(data2[1][k]);
  }

  console.log(influence_bar_axis, influence_bar_all, influence_bar_in, low_number_all, low_number_in);
  draw_rank_distribution(influence_bar_axis, influence_bar_all, influence_bar_in, 'rank_distribution', low_number_all, low_number_in);
}

prepare_rank_distribution();