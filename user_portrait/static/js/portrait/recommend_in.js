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
  Re_Draw_table: function(data){
        //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="recommend_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>粉丝数</th><th>微博数</th><th>影响力</th><th>' + '<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][5]!='未知')
        item[i][5] = item[i][5].toFixed(2);
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][3] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][4] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][5] +'</td>';
      html += '<td class="center"><input name="in_status" class="in_status" type="checkbox" value="' + item[i][0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#recommend_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "recommend_boot",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
    // page control start
    recommend_pre_page = 1;
    recommend_choose_uids = new Array();
    // page control end
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
  Re_Draw_table: function(data){
    //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url;
    //console.log(user_url);
    html = '';
    html += '<table id="compute_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>粉丝数</th><th>微博数</th><th>影响力</th><th>入库时间</th><th>计算状态</th><th>' + '<input name="compute_all" id="compute_all" type="checkbox" value="" onclick="compute_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][5]!='未知')
        item[i][5] = item[i][5].toFixed(2);
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      var compute_status;
      if(item[i][7]==2)
        compute_status = "正在计算";
      else if(item[i][7]==1)
        compute_status = "确定计算";
      else if(item[i][7]==0)
        compute_status = "未计算";
      else
        compute_status = "Error!";
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '<td class="center">'+ item[i][5] +'</td>';
      html += '<td class="center">'+ item[i][6] +'</td>';
      html += '<td class="center" id="'+ i +'">'+ compute_status +'</td>';
      if(item[i][7]==0)
        html += '<td class="center">'+ '<input name="compute_status" type="checkbox" id="' + item[i][0] + '" value="' + item[i][6] + '" />' +'</td>';
      else if(item[i][7]==1||item[i][7]==2)
        html += '<td class="center">'+ '<input name="compute_status" type="checkbox" id="' + item[i][0] + '" value="' + item[i][6] + '" disabled="true" checked="true" />' +'</td>';
      else
        html += '<td class="center">'+ 'Error!' +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#compute_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "compute_boot",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
    // page control start
    compute_pre_page = 1;
    compute_choose_uids = new Array();
    // page control end
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
  Re_Draw_table: function(data){
        //console.log(data);
    var div = that.div;
    //console.log(div);
    $(div).empty();
    var user_url ;
    //console.log(user_url);
    html = '';
    html += '<table id="history_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>注册地</th><th>粉丝数</th><th>微博数</th><th>影响力</th><th>入库状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][5]!='未知')
        item[i][5] = item[i][5].toFixed(2);
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      var in_status;
      if(item[i][6]==1)
        in_status = "已入库";
      else if(item[i][6]==0)
        in_status = "未入库";
      else
        in_status = "Error!";
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '<td class="center">'+ item[i][5] +'</td>';
      html += '<td class="center" id="'+ item[i][0] +'">'+ in_status +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#history_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "history_boot",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
  }
}

function confirm(data){
  console.log(data);
  if(data)
    alert('操作成功！');
}

function bindOption(){

      $('#recommend_button').click(function(){
            var cur_uids = [];
            $('input[name="in_status"]:checked').each(function(){
              cur_uids.push($(this).attr('value'));
          })
          recommend_choose_uids[recommend_pre_page] = cur_uids;
          var recommend_uids = [];
          for (var key in recommend_choose_uids){
              var temp_list = recommend_choose_uids[key];
              for (var i = 0;i < temp_list.length;i++){
                  recommend_uids.push(temp_list[i]);
              }
          }
          var recommend_date = $("#recommend_date_select").val()
          console.log(recommend_date);
          console.log(recommend_uids);
          var uids_trans = '';
          for(var i in recommend_uids){
              uids_trans += recommend_uids[i];
              if(i<(recommend_uids.length-1))
                uids_trans += ',';
          }
          var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + uids_trans;
          console.log(recommend_confirm_url);
          draw_table_recommend.call_sync_ajax_request(recommend_confirm_url, draw_table_recommend.ajax_method, confirm);
          var url_recommend_new = '/recommentation/show_in/?date=' + $("#recommend_date_select").val();
          draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
          draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
          var url_compute_new = '/recommentation/show_compute/?date=' + now;
          draw_table_compute_new = new Search_weibo_compute(url_compute_new, '#compute');
          draw_table_compute_new.call_sync_ajax_request(url_compute_new, draw_table_compute_new.ajax_method, draw_table_compute_new.Re_Draw_table);
          var url_history_new = '/recommentation/show_in_history/?date=' + $("#history_date_select").val();
          draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
          draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);
    });
  $('#compute_button').click(function(){
       var cur_uids = [];
      $('input[name="compute_status"]:checked:enabled').each(function(){
          $(this).attr('disabled',true);
          $("#"+$(this).attr('id')).html("确定计算");
          cur_uids.push([$(this).attr('id'), $(this).attr('value')]);
      });
      compute_choose_uids[compute_pre_page] = cur_uids;
      var compute_dates = [];
      var compute_uids = [];
      for (var key in compute_choose_uids){
          var temp_list = compute_choose_uids[key];
          for (var i = 0;i < temp_list.length;i++){
              compute_uids.push(temp_list[i][0]);
              compute_dates.push(temp_list[i][1]);
          }
      }
      console.log(compute_dates);
      console.log(compute_uids);
      var uids_compute = '';
      var dates_compute = '';
      for(var i in compute_uids){
          uids_compute += compute_uids[i];
          if(i<(compute_uids.length-1))
            uids_compute += ',';
      }
      for(var j in compute_dates){
          dates_compute += compute_dates[j];
          if(j<(compute_dates.length-1))
            dates_compute += ',';
      }
      var compute_confirm_url = '/recommentation/identify_compute/?date=' + dates_compute + '&uid_list=' + uids_compute;
      console.log(compute_confirm_url);
      draw_table_compute.call_sync_ajax_request(compute_confirm_url, draw_table_compute.ajax_method, confirm);
      var url_compute_new = '/recommentation/show_compute/?date=' + now;
      draw_table_compute_new = new Search_weibo_compute(url_compute_new, '#compute');
      draw_table_compute_new.call_sync_ajax_request(url_compute_new, draw_table_compute_new.ajax_method, draw_table_compute_new.Re_Draw_table);
  });
    $('#recommend_date_button').click(function(){
      //console.log($("#recommend_date_select").val());
      var url_recommend_new = '/recommentation/show_in/?date=' + $("#recommend_date_select").val();
      //console.log(url_recommend_new);
      draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
      draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
    });

    $('#history_date_button').click(function(){
      //console.log($("#history_date_select").val());
      var url_history_new = '/recommentation/show_in_history/?date=' + $("#history_date_select").val();
      //console.log(url_history_new);
      draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
      draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);
    });
}

// page control start
var recommend_pre_page = 1;
var compute_pre_page = 1;

var recommend_choose_uids = new Array();
var compute_choose_uids = new Array();
// page control end

var tomorrow = new Date(2013,8,8);
var now_date = new Date(tomorrow-24*60*60*1000);
var now = now_date.getFullYear()+"-"+((now_date.getMonth()+1)<10?"0":"")+(now_date.getMonth()+1)+"-"+((now_date.getDate())<10?"0":"")+(now_date.getDate());

var url_recommend = '/recommentation/show_in/?date=' + now;
draw_table_recommend = new Search_weibo_recommend(url_recommend, '#recommend');
draw_table_recommend.call_sync_ajax_request(url_recommend, draw_table_recommend.ajax_method, draw_table_recommend.Re_Draw_table);

var url_compute = '/recommentation/show_compute/?date=' + now;
draw_table_compute = new Search_weibo_compute(url_compute, '#compute');
draw_table_compute.call_sync_ajax_request(url_compute, draw_table_compute.ajax_method, draw_table_compute.Re_Draw_table);

var url_history = '/recommentation/show_in_history/?date=' + now;
draw_table_history = new Search_weibo_history(url_history, '#history');
draw_table_history.call_sync_ajax_request(url_history, draw_table_history.ajax_method, draw_table_history.Re_Draw_table);

var recommend_date = [];
for(var i=0;i<7;i++){
  var today = new Date(tomorrow-24*60*60*1000*(7-i));
  recommend_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
}
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
for(var i=0;i<7;i++){
  var today = new Date(tomorrow-24*60*60*1000*(7-i));
  history_date[i] = today.getFullYear()+"-"+((today.getMonth()+1)<10?"0":"")+(today.getMonth()+1)+"-"+((today.getDate())<10?"0":"")+(today.getDate());
}
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

bindOption();

function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function compute_all(){
  $('input[name="compute_status"]:not(:disabled)').prop('checked', $("#compute_all").prop('checked'));
}

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}