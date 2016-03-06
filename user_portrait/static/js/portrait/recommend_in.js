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
    var user_url;
    html = '';
    html += '<table id="recommend_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="width:140px">用户ID</th><th>昵称</th><th>注册地</th><th style="width:100px">粉丝数</th><th style="width:100px">微博数</th><th style="width:100px">影响力</th><th style="width:100px">用户详情</th><th>' + '<input name="recommend_all" id="recommend_all" type="checkbox" value="" onclick="recommend_all()" />' + '</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][5]!='未知'){
        item[i][5] = item[i][5].toFixed(2);
      }
      else{
          item[i][5] = '';
      }
      if (item[i][3] == '未知'){
          item[i][3] = '';
      }
      if (item[i][4] == '未知'){
          item[i][4] = '';
      }
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][3] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][4] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][5] +'</td>';
      html += '<td class="center" style="width:100px"><a style="cursor:pointer;" name="details" id="'+ item[i][0] +'" title="'+ item[i][1] +'">详情</a></td>';
      html += '<td class="center"><input name="in_status" class="in_status" type="checkbox" value="' + item[i][0] + '" /></td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);

    $('[name="details"]').click(function(){
      var detail_uid = $(this).attr('id');
      var detail_uname = $(this).attr('title');
      var detail_url = '/recommentation/show_in_more/?uid=' + detail_uid;
      $.ajax({
        url: detail_url,
        type: 'GET',
        dataType: 'json',
        async: false,
        success:show_details
      });
      function show_details(data){
        if(data['time_trend'].length==0){
          $('#line_chart').empty();
          $('#line_chart').append('<div style="text-align:center">暂无数据！</div>');
        }
        else{
          //$('#line_chart').empty();
          var line_chart_xaxis = [];
          for(var k in data['time_trend'][0])
            line_chart_xaxis.push(new Date(parseInt(data['time_trend'][0][k])*1000).format("MM-dd hh:mm"));
          var line_chart_yaxis = data['time_trend'][1];
          draw_line_chart(line_chart_xaxis.reverse(), line_chart_yaxis.reverse(), 'line_chart', detail_uname);
        }
        $('#place').empty();
        if(data['activity_geo'].length==0){
          $('#in_detail').css('height','70px');
          $('#place').append('<h4 style="text-align:center">活跃地点</h4><div style="text-align:center">暂无数据！</div>');
        }
        else{
          $('#in_detail').css('height','300px');
          var place_html = '';
          place_html += '<h4 style="text-align:center">活跃地点</h4>';
          place_html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
          place_html += '<thead><tr><th style="text-align:center;vertical-align:middle;width:80px">排名</th><th style="text-align:center;vertical-align:middle;width:200px">地点</th><th style="text-align:center;vertical-align:middle;width:80px">微博数</th></tr></thead>';
          place_html += '<tbody>';
          for(var m in data['activity_geo']){
            if(parseInt(m)<5){
              place_html += '<tr>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ (parseInt(m)+1) +'</td>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['activity_geo'][m][0] +'</td>';
              place_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['activity_geo'][m][1] +'</td>';
              place_html += '</tr>';
            }
          }
          place_html += '</tbody>';
          place_html += '</table>';

          $('#place').append(place_html);
        }

        $('#hashtag').empty();
        if(data['hashtag'].length==0){
          $('#hashtag').append('<h4 style="text-align:center">HashTag</h4><div style="text-align:center">暂无数据！</div>');
        }
        else{
          $('#in_detail').css('height','300px');
          var hashtag_html = '';
          hashtag_html += '<h4 style="text-align:center">HashTag</h4>';
          hashtag_html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
          hashtag_html += '<thead><tr><th style="text-align:center;vertical-align:middle;width:80px">排名</th><th style="text-align:center;vertical-align:middle;width:200px">HashTag</th><th style="text-align:center;vertical-align:middle;width:80px">微博数</th></tr></thead>';
          hashtag_html += '<tbody>';
          for(var n in data['hashtag']){
            if(parseInt(n)<5){
              hashtag_html += '<tr>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ (parseInt(n)+1) +'</td>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['hashtag'][n][0] +'</td>';
              hashtag_html += '<td class="center" style="text-align:center;vertical-align:middle">'+ data['hashtag'][n][1] +'</td>';
              hashtag_html += '</tr>';
            }
          }
          hashtag_html += '</tbody>';
          hashtag_html += '</table>';
          $('#hashtag').append(hashtag_html);
        }

        $('#details_modal').modal();
      }
    });

    $('#recommend_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "recommend_boot",
        "aoColumnDefs":[ {"bSortable": false, "aTargets":[7]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页",
        }
    });
    // page control start
    recommend_pre_page = 1;
    recommend_choose_uids = new Array();
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
    var user_url ;
    html = '';
    html += '<table id="history_table_new" class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<thead><tr><th style="width:140px">用户ID</th><th>昵称</th><th>注册地</th><th style="width:100px">粉丝数</th><th style="width:100px">微博数</th><th style="width:100px">影响力</th><th>计算状态</th></tr></thead>';
    var item = data;
    html += '<tbody>';
    for(var i in item){
      item[i] = replace_space(item[i]);
      if(item[i][5]!='未知'){
        item[i][5] = item[i][5].toFixed(2);
      }
      else{
        item[i][5] = '';
      }
      if (item[i][3] == '未知'){
          item[i][3] = '';
      }
      if (item[i][4] == '未知'){
          item[i][4] = '';
      }
      user_url = 'http://weibo.com/u/';
      user_url = user_url + item[i][0];
      var in_status;
      if(item[i][7]==2)
        in_status = "预约计算";
      else if(item[i][7]==3)
        in_status = "正在计算";
      else
        in_status = "计算完成";
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ ' target="_blank">'+ item[i][0] +'</td>';
      html += '<td class="center">'+ item[i][1] +'</td>';
      html += '<td class="center">'+ item[i][2] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][3] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][4] +'</td>';
      html += '<td class="center" style="width:100px">'+ item[i][5] +'</td>';
      html += '<td class="center">'+ in_status +'</td>';
      html += '</tr>';
    }
    html += '</tbody>';
    html += '</table>';
    $(div).append(html);
    $('#history_table_new').dataTable({
        "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "history_boot",
        //"aoColumnDefs":[ {"bSortable": false, "aTargets":[6]}],
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
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
          var uids_trans = '';
          for(var i in recommend_uids){
              uids_trans += recommend_uids[i];
              if(i<(recommend_uids.length-1))
                uids_trans += ',';
          }
          if(recommend_uids.length == 0){
            alert("请选择至少一个用户！");
          }
          else{
            var compute_time;
            if($('input[name="instant"]:checked').val()==1){
              compute_time = '1';
              var sure = confirm('立即计算会消耗系统较多资源，您确定要立即计算吗？');
              if(sure==true){
                  $('#recommend').empty();
                  var waiting_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
                  $('#recommend').append(waiting_html);

                  var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + uids_trans + '&status=' + compute_time;
                  draw_table_recommend.call_sync_ajax_request(recommend_confirm_url, draw_table_recommend.ajax_method, confirm_ok);
                  
                  var url_recommend_new = '/recommentation/show_in/?date=' + $("#recommend_date_select").val();
                  draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
                  draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
                  

                  var url_history_new = '/recommentation/show_compute/?date=' + $("#history_date_select").val();
                  draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
                  draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);
              }
            }
            else{
                compute_time = '2';
                alert('您选择了预约计算，系统将在今日24:00自动启动计算！');
                $('#recommend').empty();
                var waiting_html = '<div style="text-align:center;vertical-align:middle;height:40px">数据正在加载中，请稍后...</div>';
                $('#recommend').append(waiting_html);

                var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + uids_trans + '&status=' + compute_time;
                draw_table_recommend.call_sync_ajax_request(recommend_confirm_url, draw_table_recommend.ajax_method, confirm_ok);
                
                var url_recommend_new = '/recommentation/show_in/?date=' + $("#recommend_date_select").val();
                draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
                draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);

                var url_history_new = '/recommentation/show_compute/?date=' + $("#history_date_select").val();
                draw_table_history_new = new Search_weibo_history(url_history_new, '#history');
                draw_table_history_new.call_sync_ajax_request(url_history_new, draw_table_history_new.ajax_method, draw_table_history_new.Re_Draw_table);
            }
          }
      });
      
      $('#recommend_date_button').click(function(){
          var url_recommend_new = '/recommentation/show_in/?date=' + $("#recommend_date_select").val();
          draw_table_recommend_new = new Search_weibo_recommend(url_recommend_new, '#recommend');
          draw_table_recommend_new.call_sync_ajax_request(url_recommend_new, draw_table_recommend_new.ajax_method, draw_table_recommend_new.Re_Draw_table);
      });
      $('#history_date_button').click(function(){
          var url_history_new = '/recommentation/show_compute/?date=' + $("#history_date_select").val();
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

var now_date = choose_time_for_mode();
var last_date = new Date(now_date - 24*60*60*1000)
var last = last_date.format('yyyy-MM-dd');

var url_recommend = '/recommentation/show_in/?date=' + last;
draw_table_recommend = new Search_weibo_recommend(url_recommend, '#recommend');
draw_table_recommend.call_sync_ajax_request(url_recommend, draw_table_recommend.ajax_method, draw_table_recommend.Re_Draw_table);


var url_history = '/recommentation/show_compute/?date=' + last;
draw_table_history = new Search_weibo_history(url_history, '#history');
draw_table_history.call_sync_ajax_request(url_history, draw_table_history.ajax_method, draw_table_history.Re_Draw_table);

function date_initial(){
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

function draw_line_chart(xaxis, yaxis, div, uname){
  var uname_text = '"' + uname + '"的微博数';
  var line_chart_option = {
    title : {
        text: '用户微博走势图',
        subtext: '',
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:[uname_text]
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
            boundaryGap : false,
            axisLabel:{
              interval:5,
            },
            data : xaxis,
        }
    ],
    yAxis : [
        {
            type : 'value',
        }
    ],
    series : [
        {
            name:uname_text,
            type:'line',
            data:yaxis,
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
    ]
  };
  var draw_init2 = echarts.init(document.getElementById(div));
  draw_init2.setOption(line_chart_option);
}

