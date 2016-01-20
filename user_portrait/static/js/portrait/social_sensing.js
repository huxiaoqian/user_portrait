Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}
function Social_sense(){
  this.ajax_method = 'GET';
}
Social_sense.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },
  Draw_group_table: function(data){
 	$('#so_group_task').empty();
    var item = data;
    console.log('11');
	var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>发现方式</th><th>操作<input name="so_choose_all" id="so_choose_all" type="checkbox" value="" onclick="so_choose_all()" /></th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
		html += '<tr>';
		for(j=0;j<item[i].length-1;j++){
			if (j==0){
				html += '<td name="task_name">'+item[i][j]+'</td>';
			}else{
				html += '<td>'+item[i][j]+'</td>';
			}
		}
		if(item[i][4]==1){
			html += '<td><a style="cursor:hand;" href="/index/group_analysis/?name=' + item[i][0]+ '">已完成</a></td>';
		}else{
			html += '<td>正在计算</td>';
		}
		html +='<td>发现方式</td>';
		html +='<td><input name="so_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></td>';
		html += '</tr>';
	}
	html += '</tbody>';
    html += '</table>';
	$('#so_group_task').append(html);
  },
  Draw_task_table: function(data){
  	$('#so_task_table').empty();
  	var item = data;
  	var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;"><th>任务名称</th><th>创建人</th><th>创建时间</th><th>终止时间</th><th>备注</th><th>传感器与关键词</th><th>预警状态</th><th>历史状态</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	// for (i=0;i<item.length;i++){
	// 	html += '<tr>';
	// 	for(j=0;j<item[i].length-1;j++){
	// 		if (j==0){
	// 			html += '<td name="task_name">'+item[i][j]+'</td>';
	// 		}else{
	// 			html += '<td>'+item[i][j]+'</td>';
	// 		}
	// 	}
	// 	if(item[i][4]==1){
	// 		html += '<td><a style="cursor:hand;" href="/index/group_analysis/?name=' + item[i][0]+ '">已完成</a></td>';
	// 	}else{
	// 		html += '<td>正在计算</td>';
	// 	}
		html += '<td>名称</td><td>人</td><td>时间</td><td>终止时间</td><td>备注</td><td><a href="javascript:void(0)" id="so_keys">查看传感器</a></td><td>状态</td>'
		html +='<td><a href="javascript:void(0)" id="so_history">查看详情</a></td><td><a href="javascript:void(0)" id="task_del">change_type</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="so_task_del">删除</a></td>';
		html += '</tr>';
	//}
	html += '</tbody>';
    html += '</table>';
	$('#so_task_table').append(html);
  }
}

$('input[name="so_mode_choose"]').change(function(){
    var so_user_option = $('input[name="so_mode_choose"]:checked').val();
    if (so_user_option == 'so_all_users'){
        $('#so_have_users_ext').css('display','none');
    }
    else{
        $('#so_have_users_ext').css('display','block');
    }
    //seed_user_init();
    //if (!seed_user_flag) seed_user_flag = true; // no more html init
});
var current_date = new Date().format('yyyy/MM/dd hh:mm');
var max_date = '+1970/01/01';
var min_date = '-1970/01/30';
$('#so_end_time').datetimepicker({value:current_date,minDate:min_date,maxDate:max_date,step:10});

function prepare(that){
	console.log(that);
	$('a[id^="so_keys"]').click(function(e){
		console.log('aaa');
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		url = "/detect/show_detect_result/?task_name=" + temp;
		that.call_sync_ajax_request(url,that.ajax_method,draw_sensor);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().html();
		$('span[id^="so_group_name0"]').html(temp);
		$('span[id^="so_remark0"]').html(remark0);
		$('#so_keys_block').modal();
	});
	$('a[id^=so_history]').click(function(){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().html();
	});
}
var Social_sense= new Social_sense();
prepare(Social_sense);

function draw_result(){
	url = '/group/show_task/'; 
	Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, Social_sense.Draw_group_table);
}
draw_result();

	//Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, Social_sense.Draw_task_table);
Social_sense.Draw_task_table();
function so_choose_all(){
  $('input[name="so_list_option"]').prop('checked', $("#so_choose_all").prop('checked'));
}



function draw_sensor(data){
	$('#so_sensor_content').empty();
	var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;height:300px;">';
    html += '<tr><th style="text-align:center">用户ID</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th><input name="analyze_choose_all" id="analyze_choose_all" type="checkbox" value="" onclick="analyze_choose_all()" /></th></tr>';
    for (var i=0;i<data.length;i++) {
        html += '<tr><th style="text-align:center">' + data[i][0] + '</th><th style="text-align:center">' + data[i][1] + '</th><th style="text-align:center">' + data[i][2].toFixed(2) + '</th><th style="text-align:center">' + data[i][3].toFixed(2) + '</th><th style="text-align:center">' + data[i][4].toFixed(2) + '</th><th><input name="analyze_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></th></tr>';
    	i = i + 1;
 	}
    html += '</table>'; 
    $('#so_sensor_content').append(html); 
}

function draw_keys(data){
    $('#so_keys_content').empty();
    var html = '';

    $('#so_keys_content').append(html);    
}

	$('a[id^="so_keys"]').click(function(e){
		console.log('aaa');
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		url = "/detect/show_detect_result/?task_name=" + temp;
		//that.call_sync_ajax_request(url,that.ajax_method,draw_sensor);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().html();
		$('span[id^="so_group_name0"]').html(temp);
		$('span[id^="so_remark0"]').html(remark0);
		$('#so_keys_block').modal();
	});