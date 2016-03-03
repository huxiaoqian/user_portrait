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
    var div = that.div;
    $(div).empty();
    var user_url ;
    html = '';
    html += '<table id="recommend_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>领域</th><th>话题</th><th style="width:100px">活跃度</th><th style="width:100px">重要度</th><th style="width:100px">影响力</th><th>' + '<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      for(var j=4;j<7;j++){
        if(item[i][j]!='未知'){
          item[i][j] = item[i][j].toFixed(2)
        }
        else{
            item[i][j] = '';
        }
      }
      user_url = '/index/personal/?uid=';
      user_url = user_url + item[i][0];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][6] +'</td>';
      html += '<td class="center">'+ item[i][5] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '<td class="center"><input name="in_status" class="in_status" type="checkbox" value="' + item[i][0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#recommend_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "recommend_boot",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
    // page control start
    var recommend_pre_page = 1;
    var recommend_choose_uids = new Array();
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
    var div = that.div;
    $(div).empty();
    var user_url;
    html = '';
    html += '<table id="history_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>领域</th><th>话题</th><th style="width:100px">活跃度</th><th style="width:100px">重要度</th><th style="width:100px">影响力</th><th>' + '<input name="history_all" id="history_all" type="checkbox" value="" onclick="history_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      for(var j=4;j<7;j++){
        if(item[i][j]!='未知'){
          item[i][j] = item[i][j].toFixed(2);
        }
        else{
            item[i][j] = '';
        }
      }
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center">'+ item[i][3] +'</td>';
      html += '<td class="center">'+ item[i][6] +'</td>';
      html += '<td class="center">'+ item[i][5] +'</td>';
      html += '<td class="center">'+ item[i][4] +'</td>';
      html += '<td class="center"><input name="history_status" class="history_status" type="checkbox" id="' + item[i][0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#history_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "history_boot",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
    // page control start
    var history_pre_page = 1;
    var history_choose_uids = new Array();
    // page control end
  }
}

function confirm_ok(data){
  if(data)
    alert('操作成功！');
}

function bindOption(){
  $('#recommend_button').click(function(){
      var cur_uids = [];
      $('input[name="in_status"]:checked').each(function(){
          cur_uids.push($(this).attr('value'));
      });
      recommend_choose_uids[recommend_pre_page] = cur_uids;
      var recommend_uids = [];
      for (var key in recommend_choose_uids){
          var temp_list = recommend_choose_uids[key];
          for (var i = 0;i < temp_list.length;i++){
              recommend_uids.push(temp_list[i]);
          }
      }
      var uids_trans = '';
      for(var i in recommend_uids){
          uids_trans += recommend_uids[i];
          if(i<(recommend_uids.length-1))
            uids_trans += ',';
      }
      var recommend_confirm_url = '/recommentation/identify_out/?date=' + now + '&data=' + uids_trans;
      draw_table_recommend.call_sync_ajax_request(recommend_confirm_url, draw_table_recommend.ajax_method, confirm_ok);
      var url_recommend_new = '/recommentation/show_out/?fields=uid,uname,domain,topic,influence,importance,activeness';
      draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
      draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
      
      var date_history = $("#history_date_select").val();
      var url_history_new = '';
      if(date_history=="all")
        url_history_new = '/recommentation/show_all_history_out/';
      else
        url_history_new = '/recommentation/history_delete/?date=' + $("#history_date_select").val();
      draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
      draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);  
  });
  $('#no_recommend_button').click(function(){
      var cur_uids = [];
      $('input[name="in_status"]:checked').each(function(){
          cur_uids.push($(this).attr('value'));
      });
      recommend_choose_uids[recommend_pre_page] = cur_uids;
      var recommend_uids = [];
      for (var key in recommend_choose_uids){
          var temp_list = recommend_choose_uids[key];
          for (var i = 0;i < temp_list.length;i++){
              recommend_uids.push(temp_list[i]);
          }
      }
      var uids_trans = '';
      for(var i in recommend_uids){
          uids_trans += recommend_uids[i];
          if(i<(recommend_uids.length-1))
            uids_trans += ',';
      }
      var no_recommend_confirm_url = '/recommentation/cancel_recommend_out/?date=' + now + '&uid_list=' + uids_trans;
      draw_table_recommend.call_sync_ajax_request(no_recommend_confirm_url, draw_table_recommend.ajax_method, confirm_ok);
      var url_recommend_new = '/recommentation/show_out/?fields=uid,uname,domain,topic,influence,importance,activeness';
      draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
      draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
      
      var date_history = $("#history_date_select").val();
      var url_history_new = '';
      if(date_history=="all")
        url_history_new = '/recommentation/show_all_history_out/';
      else
        url_history_new = '/recommentation/history_delete/?date=' + $("#history_date_select").val();
      draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
      draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);  
  });
  $('#history_button').click(function(){
      var cur_uids = [];
      $('input[name="history_status"]:checked').each(function(){
          $(this).attr('disabled',true);
          cur_uids.push($(this).attr('id'));
      });
      history_choose_uids[history_pre_page] = cur_uids;
      var history_uids = [];
      for (var key in history_choose_uids){
          var temp_list = history_choose_uids[key];
          for (var i = 0;i < temp_list.length;i++){
              history_uids.push(temp_list[i]);
          }
      }

      var history_dates = $("#history_date_select").val();
      var uids_history = '';
      for(var i in history_uids){
          uids_history += history_uids[i];
          if(i<(history_uids.length-1))
            uids_history += ',';
      }
      var history_confirm_url = '/recommentation/cancel_delete/?date=' + history_dates + '&data=' + uids_history;
      draw_table_history.call_sync_ajax_request(history_confirm_url, draw_table_history.ajax_method, confirm_ok);

      var date_history = $("#history_date_select").val();
      var url_history_new = '';
      if(date_history=="all")
        url_history_new = '/recommentation/show_all_history_out/';
      else
        url_history_new = '/recommentation/history_delete/?date=' + $("#history_date_select").val();
      draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
      draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);  
      var url_recommend_new = '/recommentation/show_out/?fields=uid,uname,domain,topic,influence,importance,activeness';
      draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
      draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
  });
  
  /*
  $('#recommend_date_button').click(function(){
    var url_recommend_new = '/recommentation/show_out/?fields=uid,uname,domain,topic,influence,importance,activeness';
    //console.log(url_recommend_new);
    draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
    draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
  });
  */

  $('#history_date_button').click(function(){
    var date_history = $("#history_date_select").val();
    var url_history_new = '';
    if(date_history=="all")
      url_history_new = '/recommentation/show_all_history_out/';
    else
      url_history_new = '/recommentation/history_delete/?date=' + $("#history_date_select").val();
    draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
    draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);
  });
}

// page control start
var recommend_pre_page = 1;
var history_pre_page = 1;
var recommend_choose_uids = new Array();
var history_choose_uids = new Array();
// page control end

var now_date = choose_time_for_mode();
var now = now_date.format('yyyy-MM-dd');
var last_date = new Date(now_date-24*60*60*1000);
var last = last_date.format('yyyy-MM-dd');

var url_recommend = '/recommentation/show_out/?fields=uid,uname,domain,topic,influence,importance,activeness';
draw_table_recommend = new Search_weibo_recommend(url_recommend, '#recommend');
draw_table_recommend.call_sync_ajax_request(url_recommend, draw_table_recommend.ajax_method, draw_table_recommend.Re_Draw_table);

var url_history = '/recommentation/history_delete/?date=' + last;
draw_table_history = new Search_weibo_history(url_history, '#history');
draw_table_history.call_sync_ajax_request(url_history, draw_table_history.ajax_method, draw_table_history.Re_Draw_table);

function date_initial(){
  /* 
  var recommend_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(last_date-24*60*60*1000*(6-i));
    recommend_date[i] = today.format('yyyy-MM-dd');
  }
  $("#recommend_date_select").empty();
  var recommend_date_html = '';
  recommend_date_html += '<option value="' + recommend_date[0] + '">' + recommend_date[0] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[1] + '">' + recommend_date[1] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[2] + '">' + recommend_date[2] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[3] + '">' + recommend_date[3] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[4] + '">' + recommend_date[4] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[5] + '">' + recommend_date[5] + '</option>';
  recommend_date_html += '<option value="' + recommend_date[6] + '" selected="selected">' + recommend_date[6] + '</option>';
  $("#recommend_date_select").append(recommend_date_html);
  */

  var history_date = [];
  for(var i=0;i<7;i++){
    var today = new Date(last_date-24*60*60*1000*(6-i));
    history_date[i] = today.format('yyyy-MM-dd');
  }
  $("#history_date_select").empty();
  var history_date_html = '';
  history_date_html += '<option value="' + history_date[0] + '">' + history_date[0] + '</option>';
  history_date_html += '<option value="' + history_date[1] + '">' + history_date[1] + '</option>';
  history_date_html += '<option value="' + history_date[2] + '">' + history_date[2] + '</option>';
  history_date_html += '<option value="' + history_date[3] + '">' + history_date[3] + '</option>';
  history_date_html += '<option value="' + history_date[4] + '">' + history_date[4] + '</option>';
  history_date_html += '<option value="' + history_date[5] + '">' + history_date[5] + '</option>';
  history_date_html += '<option value="' + history_date[6] + '" selected="selected">' + history_date[6] + '</option>';
  history_date_html += '<option value="all">全部</option>';
  $("#history_date_select").append(history_date_html);
}

date_initial();

bindOption();

function recommend_all(){
  $('input[name="in_status"]:not(:disabled)').prop('checked', $("#recommend_all").prop('checked'));
}

function history_all(){
  $('input[name="history_status"]:not(:disabled)').prop('checked', $("#history_all").prop('checked'));
}

function replace_space(data){
  for(var i in data){
    if(data[i]===""||data[i]==="unknown"){
      data[i] = "未知";
    }
  }
  return data;
}
