function Search_weibo_result(url, div){
  that = this;
  this.ajax_method = 'GET';
  this.url = url;
  this.div = div;
}

Search_weibo_result.prototype = {
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
    html += '<thead><tr><th>uid</th><th>用户名</th><th>性别</th><th>注册地</th><th>领域</th><th>话题</th><th>' + '<input name="choose_all" id="choose_all" type="checkbox" value="" onclick="choose_all()" />' + '</th></tr></thead>';
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
      html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + i + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  }
}

var url_search_result = '/recommentation/show_in/?date=2013-09-07';
draw_table_search_result = new Search_weibo_result(url_search_result, '#search_result');
draw_table_search_result.call_sync_ajax_request(url_search_result, draw_table_search_result.ajax_method, draw_table_search_result.Draw_table);


function compare_button(){
  var compare_uids = [];
  $('input[name="search_result_option"]:checked').each(function(){
      compare_uids.push($(this).attr('value'));
  })
  console.log(compare_uids);
}

function group_button(){
  var group_uids = [];
  $('input[name="search_result_option"]:checked').each(function(){
      group_uids.push($(this).attr('value'));
  })
  console.log(group_uids);
}

function delete_button(){
  var delete_uids = [];
  $('input[name="search_result_option"]:checked').each(function(){
      delete_uids.push($(this).attr('value'));
  })
  console.log(delete_uids);
}

function choose_all(){
  $('input[name="search_result_option"]').prop('checked', $("#choose_all").prop('checked'));
}