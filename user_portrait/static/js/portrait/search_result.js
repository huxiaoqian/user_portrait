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
    html += '<thead><tr><th>用户ID</th><th>昵称</th><th>性别</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th>' + '<input name="choose_all" id="choose_all" type="checkbox" value="" onclick="choose_all()" />' + '</th></tr></thead>';
    html += '<tbody>';
    for(var i = 0; i<data.length;i++){
      var item = data[i];
      global_data[item[0]] = item; // make global data
      user_url = '/index/personal/?uid=' + item[0];
      html += '<tr id=' + item[0] +'>';
      html += '<td class="center" name="uids"><a href='+ user_url+ '>'+ item[0] +'</td>';
      html += '<td class="center">'+ item[1] +'</td>';
      html += '<td class="center">'+ gender(item[2]) +'</td>';
      html += '<td class="center">'+ item[3] +'</td>';
      html += '<td class="center">'+ item[4].toFixed(2) +'</td>';
      html += '<td class="center">'+ item[5].toFixed(2) +'</td>';
      html += '<td class="center">'+ item[6].toFixed(2) +'</td>';
      html += '<td class="center"><input name="search_result_option" class="search_result_option" type="checkbox" value="' + item[0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
  }
}

function gender(num){
    if (num == '1'){
        return '男';
    }
    else if (num == '2'){
        return '女';
    }
    else{
        return '未知';
    }
}
var global_pre_page = 1;
var global_choose_uids = new Array();
var global_data = new Array();

console.log(url_search_result);
draw_table_search_result = new Search_weibo_result(url_search_result, '#search_result');
draw_conditions(draw_table_search_result);
draw_table_search_result.call_sync_ajax_request(url_search_result, draw_table_search_result.ajax_method, draw_table_search_result.Draw_table);

function deleteurl(that, parameter){
    for (var i = 0;i < pars.length;i++){
        var pname = parameter.substring(7, parameter.length);
        if (pname == pars[i]){
            values[i] = '';
        }
    }
    draw_conditions(that);
    url_search_result = '/attribute/portrait_search/?stype=2&' + par2url(pars, values);
    that.call_sync_ajax_request(url_search_result, that.ajax_method, that.Draw_table);
}
function process_par(name, value){
    var result = new Array();
    if (name == 'uid'){
        result[0] = '用户ID';
        result[1] = value;
    }
    else if(name=='uname'){
        result[0] = '昵称';
        result[1] = value;
    }
    else if(name=='location'){
        result[0] = '注册地';
        result[1] = value;
    }
    else if(name=='keywords'){
        result[0] = '关键词';
        result[1] = value;
    }
    else if(name=='hashtag'){
        result[0] = 'hashtag';
        result[1] = value;
    }
    else if(name=='psycho_feature'){
        result[0] = '心理特征';
        switch(value){
            case 'dzz': result[1] = '胆汁质';break;
            case 'dxz': result[1] = '多血质';break;
            case 'nyz': result[1] = '粘液质';break;
            case 'yyz': result[1] = '抑郁质';break;
        }
    }
    else if(name=='psycho_status'){
        result[0] = '心理状态';
        switch(value){
            case 'pos': result[1] = '积极';break;
            case 'neg': result[1] = '消极';break;
            case 'anx': result[1] = '焦虑';break;
            case 'ang': result[1] = '生气';break;
            case 'sad': result[1] = '悲伤';break;
        }
    }
    else if(name=='domain'){
        result[0] = '领域';
        result[1] = '';
        var term_list = value.split(',');
        for (var i = 0;i < term_list.length;i++){
            switch(term_list[i]){
                case 'cul': result[1] += '文化,';break;
                case 'edu': result[1] += '教育,';break;
                case 'ent': result[1] += '娱乐,';break;
                case 'fas': result[1] += '时尚,';break;
                case 'fin': result[1] += '财经,';break;
                case 'med': result[1] += '媒体,';break;
                case 'phy': result[1] += '体育,';break;
                case 'sci': result[1] += '科技,';break;
            }
        }
        result[1] = result[1].substring(0, result[1].length-1);
    }
    else if(name=='topic'){
        result[0] = '话题';
        result[1] = '';
        var term_list = value.split(',');
        for (var i = 0;i < term_list.length;i++){
            switch(value){
                case 'env': result[1] += '环境,';break;
                case 'edu': result[1] += '教育,';break;
                case 'med': result[1] += '医药,';break;
                case 'mil': result[1] += '军事,';break;
                case 'pol': result[1] += '政治,';break;
                case 'tra': result[1] += '交通,';break;
                case 'phy': result[1] += '体育,';break;
                case 'soc': result[1] += '社会,';break;
                case 'art': result[1] += '艺术,';break;
                case 'eco': result[1] += '经济,';break;
                case 'com': result[1] += '计算机,';break;
            }
        }
        result[1] = result[1].substring(0, result[1].length-1);
    }
    else{
        result[0] = '';
        result[1] = '';
    }
    return result;
}
function draw_conditions(that){
    if (stype == 1){
        console.log('=1');
        return;
    }
    else{
        console.log('=2');
        $('#conditions').empty();
        var html = '';
        for (var i = 0;i < pars.length;i++){
            var pre_name = pars[i];
            var pre_value = values[i];

            var fix_result = process_par(pre_name, pre_value);
            var fix_name = fix_result[0];
            var fix_value = fix_result[1];
            if (fix_value){
                html += '<span class="mouse" id=choose_' + pre_name + ' style="margin-left:10px">'+ fix_name + ':'+ fix_value;
                html += '&nbsp;<a class="cross" href="#">X</a></span>';
            }
        }
        $('#conditions').html(html);
        $('.mouse').click(function(){
            deleteurl(that, $(this).attr("id"));
        });
        return;
    }
}


function compare_button(){
  var cur_uids = []
  $('input[name="search_result_option"]:checked').each(function(){
      cur_uids.push($(this).attr('value'));
  });
  global_choose_uids[global_pre_page] = cur_uids;
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
  global_choose_uids[global_pre_page] = cur_uids;
  var group_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        group_uids.push(temp_list[i]);
      }
  }
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
  global_choose_uids[global_pre_page] = cur_uids;
  var delete_uids = [];
  for (var key in global_choose_uids){
      var temp_list = global_choose_uids[key];
      for (var i = 0; i < temp_list.length; i++){
        delete_uids.push(temp_list[i]);
      }
  }
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
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>性别</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr>';
      html += '<td class="center" name="compare_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ gender(item[2]) + '</td>';
      html += '<td class="center">'+ item[3] + '</td>';
      html += '<td class="center">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center">'+ item[5].toFixed(2) + '</td>';
      html += '<td class="center">'+ item[6].toFixed(2) + '</td>';
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
    html += '<table id="group_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>性别</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr>';
      html += '<td class="center" name="group_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ gender(item[2]) + '</td>';
      html += '<td class="center">'+ item[3] + '</td>';
      html += '<td class="center">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center">'+ item[5].toFixed(2) + '</td>';
      html += '<td class="center">'+ item[6].toFixed(2) + '</td>';
      html += '<td class="center"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#group_confirm_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
}

function draw_table_delete_confirm(uids, div){
  $(div).empty();
    var html = '';
    html += '<table id="delete_confirm_table" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th>用户ID</th><th>用户名</th><th>性别</th><th>注册地</th><th>活跃度</th><th>重要度</th><th>影响力</th><th></th></tr></thead>';
    html += '<tbody>';
    for(var i in uids){
      var item = global_data[uids[i]];
      html += '<tr>';
      html += '<td class="center" name="delete_confirm_uids">'+ uids[i] +'</td>';
      html += '<td class="center">'+ item[1] + '</td>';
      html += '<td class="center">'+ gender(item[2]) + '</td>';
      html += '<td class="center">'+ item[3] + '</td>';
      html += '<td class="center">'+ item[4].toFixed(2) + '</td>';
      html += '<td class="center">'+ item[5].toFixed(2) + '</td>';
      html += '<td class="center">'+ item[6].toFixed(2) + '</td>';
      html += '<td class="center"><button class="btn btn-primary btn-sm" style="width:60px;height:30px" onclick="delRow(this)">移除</button></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#delete_confirm_table').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
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
  var compare_url = '/index/contrast/?uid_list='+ compare_confirm_uids.join(',');
  console.log(compare_url);
  window.open(compare_url);
}

function group_confirm_button(){
  var group_confirm_uids = [];
  $('[name="group_confirm_uids"]').each(function(){
      group_confirm_uids.push($(this).text());
  })
  console.log(group_confirm_uids);
  var group_ajax_url = '/group/submit_task/';
  var group_url = '/index/group_result/';
  var group_name = $('input[name="group_name"]').val();
  var remark = $('input[name="remark"]').val();
  console.log(group_name, remark);
  if (group_name.length == 0){
      alert('群体名称不能为空');
      return;
  }

  if(group_name.indexOf(' ')>=0){
    alert('群体名称不能有空格,请重新输入!');
    return;
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
      console.log(data);
      if (data == '1'){
          window.location.href = group_url;
      }
      else{
          alert('已存在相同名称的群体分析任务,请重试一次!');
      }
  }
}

function delete_confirm_button(){
  var now_date = new Date();
  var now = now_date.getFullYear()+"-"+((now_date.getMonth()+1)<10?"0":"")+(now_date.getMonth()+1)+"-"+((now_date.getDate())<10?"0":"")+(now_date.getDate());
  var delete_confirm_uids = [];
  $('[name="delete_confirm_uids"]').each(function(){
      delete_confirm_uids.push($(this).text());
  })
  console.log(delete_confirm_uids);
  var delete_uid_list = '';
  for(var i in delete_confirm_uids){
      delete_uid_list += delete_confirm_uids[i];
      if(i<(delete_confirm_uids.length-1))
        delete_uid_list += ',';
  }
  if(confirm("确认要删除吗?")){
      var delete_url = '/recommentation/identify_out/?date=' + now + '&data=' + delete_uid_list;
      console.log(delete_url);
      $.ajax({
          type:'get',
          url: delete_url,
          dataType: "json",
          success: callback
      });

      function callback(data){
           console.log(data);
           if (data == '1'){
               alert('出库成功！');
           }
           else{
               alert('fail');
           }
      }
  }
}
