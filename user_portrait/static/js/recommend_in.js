function Search_weibo_recommend(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_recommend.prototype = {
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
    var div = that.div
    //console.log(div);
    $(div).empty();
    var user_url ;
    //console.log(user_url);
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>uid</th><th>昵称</th><th>性别</th><th>注册地</th><th>关注数</th><th>粉丝数</th><th>影响力</th><th>' + '<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      user_url = window.location.href;
      user_url = user_url + i;
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ '>'+ i +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center"><input name="in_status" class="in_status" type="checkbox" value="' + i + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  }
}

function Search_weibo_compute(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_compute.prototype = {
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
    var div = that.div
    //console.log(div);
    $(div).empty();
    var user_url ;
    //console.log(user_url);
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>uid</th><th>昵称</th><th>性别</th><th>注册地</th><th>关注数</th><th>粉丝数</th><th>影响力</th><th>入库时间</th><th>计算状态</th><th>' + '<input name="compute_all" id="compute_all" type="checkbox" value="" onclick="compute_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      user_url = window.location.href;
      user_url = user_url + i;
      var compute_date = item[i][0];
      var compute_status;
      if(item[i][1]==2)
        compute_status = "正在计算";
      else if(item[i][1]==1)
        compute_status = "确定计算";
      else if(item[i][1]==0)
        compute_status = "未计算";
      else
        compute_status = "Error!";
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ '>'+ i +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center" id="'+ i +'">'+ compute_status +'</td>';
      if(item[i][1]==0)
        html += '<td class="center">'+ '<input name="compute_status" class="compute_status" type="checkbox" value="' + i + '" />' +'</td>';
      else if(item[i][1]==1||item[i][1]==2)
        html += '<td class="center">'+ '<input name="compute_status" class="compute_status" type="checkbox" value="' + i + '" disabled="true" checked="true" />' +'</td>';
      else
        html += '<td class="center">'+ 'Error!' +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  }
}

function Search_weibo_history(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_history.prototype = {
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
    console.log(data);
    var div = that.div
    //console.log(div);
    $(div).empty();
    var user_url ;
    //console.log(user_url);
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>uid</th><th>昵称</th><th>性别</th><th>注册地</th><th>关注数</th><th>粉丝数</th><th>影响力</th><th>入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      user_url = window.location.href;
      user_url = user_url + i;
      var in_status;
      if(item[i]==1)
        in_status = "已入库";
      else if(item[i]==0)
        in_status = "未入库";
      else
        in_status = "Error!";
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ '>'+ i +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center" id="'+ i +'">'+ in_status +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  }
}

var url_recommend = '/recommentation/show_in/?date=2013-09-07';
draw_table_recommend = new Search_weibo_recommend(url_recommend, '#recommend');
draw_table_recommend.call_sync_ajax_request(url_recommend, draw_table_recommend.ajax_method, draw_table_recommend.Draw_table);

var url_compute = '/recommentation/show_compute/?date=2013-09-07';
draw_table_compute = new Search_weibo_compute(url_compute, '#compute');
draw_table_compute.call_sync_ajax_request(url_compute, draw_table_compute.ajax_method, draw_table_compute.Draw_table);

var url_history = '/recommentation/show_in_history/?date=2013-09-07';
draw_table_history = new Search_weibo_history(url_history, '#history');
draw_table_history.call_sync_ajax_request(url_history, draw_table_history.ajax_method, draw_table_history.Draw_table);

function recommend_button(){
  var recommend_uids = [];
  var recommend_result = [];
  var recommend_date = $("#recommend_date_select").val()
  $('input[name="in_status"]:checked').each(function(){
      $(this).attr('disabled',true);
      recommend_uids.push($(this).attr('value'));
  })
  for(var i in recommend_uids)
    $("#"+recommend_uids[i]).html("已入库");
  recommend_result[recommend_date] = recommend_uids;
  console.log(recommend_result);
}

function compute_button(){
  var compute_uids = [];
  $('input[name="compute_status"]:checked').each(function(){
      $(this).attr('disabled',true);
      compute_uids.push($(this).attr('value'));
  })
  for(var i in compute_uids)
    $("#"+compute_uids[i]).html("确定计算");
  console.log(compute_uids);
}

var today = new Date();
var recommend_date = [];
for(var i=0;i<7;i++)
  recommend_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate()-7+i)<10?"0":"")+(today.getDate()-7+i);
$("#recommend_date").empty();
var recommend_date_html = '';
recommend_date_html += '<select id="recommend_date_select">';
recommend_date_html += '<option value="' + recommend_date[0] + '">' + recommend_date[0] + '</option>';
recommend_date_html += '<option value="' + recommend_date[1] + '">' + recommend_date[1] + '</option>';
recommend_date_html += '<option value="' + recommend_date[2] + '">' + recommend_date[2] + '</option>';
recommend_date_html += '<option value="' + recommend_date[3] + '">' + recommend_date[3] + '</option>';
recommend_date_html += '<option value="' + recommend_date[4] + '">' + recommend_date[4] + '</option>';
recommend_date_html += '<option value="' + recommend_date[5] + '">' + recommend_date[5] + '</option>';
recommend_date_html += '<option value="' + recommend_date[6] + '" selected="selected">' + recommend_date[6] + '</option>';
recommend_date_html += '</select>';
$("#recommend_date").append(recommend_date_html);

var history_date = [];
for(var i=0;i<7;i++)
  history_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate()-7+i)<10?"0":"")+(today.getDate()-7+i);
$("#history_date").empty();
var history_date_html = '';
history_date_html += '<select id="history_date_select">';
history_date_html += '<option value="' + history_date[0] + '">' + history_date[0] + '</option>';
history_date_html += '<option value="' + history_date[1] + '">' + history_date[1] + '</option>';
history_date_html += '<option value="' + history_date[2] + '">' + history_date[2] + '</option>';
history_date_html += '<option value="' + history_date[3] + '">' + history_date[3] + '</option>';
history_date_html += '<option value="' + history_date[4] + '">' + history_date[4] + '</option>';
history_date_html += '<option value="' + history_date[5] + '">' + history_date[5] + '</option>';
history_date_html += '<option value="' + history_date[6] + '" selected="selected">' + history_date[6] + '</option>';
history_date_html += '</select>';
$("#history_date").append(history_date_html);

function recommend_date_button(){
  console.log($("#recommend_date_select").val());
}

function history_date_button(){
  console.log($("#history_date_select").val());
}

function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function compute_all(){
  $('input[name="compute_status"]:not(:disabled)').prop('checked', $("#compute_all").prop('checked'));
}
