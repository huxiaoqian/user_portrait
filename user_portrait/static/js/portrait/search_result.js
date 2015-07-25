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
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      user_url = window.location.href;
      user_url = user_url + item[0];
      html += '<tr>';
      html += '<td class="center" name="uids"><a href='+ user_url+ '>'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item[i] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  }
}

var global_pre_page = 1;
var global_choose_uids = new Array();
console.log(url_search_result);
draw_table_search_result = new Search_weibo_result(url_search_result, '#search_result');
draw_table_search_result.call_sync_ajax_request(url_search_result, draw_table_search_result.ajax_method, draw_table_search_result.Draw_table);


function compare_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids
  var compare_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        compare_uids.push(temp_list[i]);
      }
  }
  
  console.log(compare_uids);
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
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  var group_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        group_uids.push(temp_list[i]);
      }
  }
  /*
  $('input[name="search_result_option"]:checked').each(function(){
      group_uids.push($(this).attr('value'));
  });
  */
  console.log(group_uids);
  var len = group_uids.length;
  if (len < 1){
      alert("请选择至少1个用户!");
  }
  else{
      draw_table_group_confirm(group_uids, "#group_comfirm");
      $("#group").modal();
  }
}

function delete_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  var delete_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        delete_uids.push(temp_list[i]);
      }
  }
  /*
  $('input[name="search_result_option"]:checked').each(function(){
      delete_uids.push($(this).attr('value'));
  });
  */
  console.log(delete_uids);
  var len = delete_uids.length;
  if (len < 1){
      alert("请选择至少1个用户!");
  }
  else{
      draw_table_delete_confirm(delete_uids, "#delete_comfirm");
      $('#delete').modal();
  }
}

function choose_all(){
  $('input[name="search_result_option"]').prop('checked', $("#choose_all").prop('checked'));
}

function draw_table_compare_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>uid</th><th>用户名</th><th>性别</th><th>注册地</th><th>领域</th><th>话题</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      html += '<tr>';
      html += '<td class="center" name="compare_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function draw_table_group_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>uid</th><th>用户名</th><th>性别</th><th>注册地</th><th>领域</th><th>话题</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      html += '<tr>';
      html += '<td class="center" name="group_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
}

function draw_table_delete_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>uid</th><th>用户名</th><th>性别</th><th>注册地</th><th>领域</th><th>话题</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      html += '<tr>';
      html += '<td class="center" name="delete_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center">'+ '' +'</td>';
      html += '<td class="center"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
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
  console.log(compare_confirm_uids);
}

function group_confirm_button(){
  var group_confirm_uids = [];
  $('[name="group_confirm_uids"]').each(function(){
      group_confirm_uids.push($(this).text());
  })
  console.log(group_confirm_uids);
}

function delete_confirm_button(){
  var delete_confirm_uids = [];
  $('[name="delete_confirm_uids"]').each(function(){
      delete_confirm_uids.push($(this).text());
  })
  console.log(delete_confirm_uids);
  self.location.reload();

  /*
  $('[name="uids"]').each(function(){
    for(var i in delete_confirm_uids)
      if($(this).text()==delete_confirm_uids[i])
        $(this).parent().remove();
  })
  */
}
