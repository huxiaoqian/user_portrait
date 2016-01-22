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
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>发现方式</th><th>操作</th><th><input name="so_choose_all" id="so_choose_all" type="checkbox" value="" onclick="so_choose_all()" /></th></tr></thead>';
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
  	var warn = '';
  	var flag = '';
  	var so_flag = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;"><th>任务名称</th><th style="width: 60px;">创建人</th><th>创建时间</th><th>终止时间</th><th style="width: 180px;">备注</th><th>传感器与关键词</th><th>预警状态</th><th>历史状态</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
	  	var create_d = new Date(item[i]['create_at']*1000).format('yyyy/MM/dd hh:mm'); 
	  	var end_d = new Date(item[i]['stop_time']*1000).format('yyyy/MM/dd hh:mm'); 
		if(item[i]['warning_status']==0){
			warn = '无事件';
		}else if (item[i]['warning_status']==1){
			warn = '事件爆发';
		}else {
			warn = '事件跟踪';
		}
		if(item[i]['finish'] == 0){
			flag = '终止任务';
			so_flag = 'so_stop_task';
		}else{
			flag = '重启任务';
			so_flag = 'so_revise_task';
		}
		html += '<tr>';
		html += '<td name="task_name">'+item[i]['task_name']+'</td>';
		html += '<td>'+item[i]['create_by']+'</td>';
		html += '<td>'+create_d+'</td>';
		html += '<td>'+end_d+'</td>';
		html += '<td>'+item[i]['remark']+'</td>';
		html += '<td><a href="javascript:void(0)" id="so_keys">查看传感器</a></td>';
		html += '<td>'+warn+'</td>';
		html += '<td><a href="javascript:void(0)" id="so_history">查看详情</a></td><td><a href="javascript:void(0)" id="'+so_flag+'">'+flag+'</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="so_task_del">删除</a></td>';
		html += '</tr>';		
	}
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
var max_date = '+1970/01/30';
var min_date = '-1970/01/30';
$('input[name="so_end_time"]').datetimepicker({value:current_date,minDate:current_date,step:10});

// function prepare(that){
// 	console.log(that);
// 	$("#so_keys").click(function(e){
// 		console.log('aaa');
// 		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
// 		url = "/detect/show_detect_result/?task_name=" + temp;
// 		that.call_sync_ajax_request(url,that.ajax_method,draw_sensor);
// 		//draw_table('1',"#group_analyze_confirm");
// 		remark0 = $(this).parent().prev().html();
// 		$('span[id^="so_group_name0"]').html(temp);
// 		$('span[id^="so_remark0"]').html(remark0);
// 		$('#so_keys_block').modal();
// 	});
// 	$('a[id^=so_history]').click(function(){
// 		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().html();
// 	});
// }
var Social_sense= new Social_sense();
//prepare(Social_sense);

function draw_result(){
	url = '/group/show_task/'; 
	Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, Social_sense.Draw_group_table);
}
draw_result();
show_url='/social_sensing/show_task/';
Social_sense.call_sync_ajax_request(show_url, Social_sense.ajax_method, Social_sense.Draw_task_table);
//Social_sense.Draw_task_table();
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
function so_ready(){
	$('a[id^="so_keys"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		url = "/social_sensing/get_task_detail_info/?task_name=" + temp;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_sensor);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().html();
		$('span[id^="so_group_name0"]').html(temp);
		$('span[id^="so_remark0"]').html(remark0);
		$('#so_keys_block').modal();
	});
	
	$('a[id^="so_history"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().html();
		url = "/social_sensing/get_task_detail_info/?task_name=" + temp;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_sensor);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().prev().prev().html();
		$('span[id^="so_group_name0"]').html(temp);
		$('span[id^="so_remark0"]').html(remark0);
		draw_history('1');
		$('#so_his_block').modal();
	});

	$('a[id^="so_stop_task"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().prev().html();
		var a = confirm('确定要终止任务吗？');
		if (a== true){
			url = "/social_sensing/stop_task/?task_name=" + temp;
			Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, callback);
		}
	});	

	$('a[id^="so_revise_task"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().prev().html();
		var remark0 = $(this).parent().prev().prev().prev().prev().html();
		//url = "/social_sensing/revise_task/?task_name=" + temp;
		//Social_sense.call_sync_ajax_request(url, Social_sense.ajax_method, callback);
		$('span[id^="so_group_name0"]').html(temp);
		$('span[id^="so_remark0"]').html(remark0);
		$('#so_revise').modal();
	});	
}
so_ready();
function callback(data){
	if(data.length != 0){
		alert('操作成功！');
	}
}





$('a[id^="so_task_del"]').click(function(e){
	var a = confirm('确定要删除吗？');
    	if (a == true){
			var url = that.url;
			var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
			url = url + 'task_name=' + temp;
			console.log(url);
			//window.location.href = url;
			//that.call_sync_ajax_request(url,that.ajax_method,that.del);
	}
});

function draw_history(data){
	$('#so_his_content').empty();
	var html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;height:300px;">';
    html += '<tr><th style="text-align:center">时间</th><th style="text-align:center">关键词</th><th style="text-align:center">预警状态</th><th style="text-align:center"><a href="javascript:void(0)" id="so_show_history">查看详情</a></th></tr>';
    var his = data['history_status'];
    for (var i=0;i<his.length;i++) {
       html += '<tr><th style="text-align:center">' + his[i][0] + '</th><th style="text-align:center">' + his[i][1] + '</th><th style="text-align:center">' + his[i][2] + '</th><th style="text-align:center"><a href="javascript:void(0)" id="show_detail">查看详情</a></th></tr>';
 	}
    html += '</table>'; 
	$('#so_his_content').append(html);	
}

$('#so_user_commit').click(function(){
	so_group_data();
});

var so_user_option = $('input[name="so_mode_choose"]:checked').val();
function so_user_check(){             // check validation 
    //group_information check starts  
    var group_name = $('#so_name').val();
    var remark = $('#so_remarks').val();
    var sensors = '';
    console.log(group_name, remark); 
    if (group_name.length == 0){
        alert('群体名称不能为空');
        return false;
    }
    var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
    if (!group_name.match(reg)){
        alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
        return false;
    }
    if ((remark.length > 0) && (!remark.match(reg))){
        alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
        return false;
    }
    //other form check starts
  return true;

}
function so_group_data(){
	var flag = so_user_check();
	var url_all = new Array();
    var group_name = $('#so_name').val();
    var remark = $('#so_remarks').val();
	var so_time = Date.parse($('input[name="so_end_time"]').val())/1000;
	console.log(so_time);
	if(flag = true){
	    var key_words = $('#so_keywords').val();
	    if (so_user_option == 'so_all_users'){
	    }
	    else{              //single_user or multi_user with extension
	    	var group_names = [];
		  	$('[name="so_list_option"]').each(function(){
		  	    group_names.push($(this).parent().prev().prev().prev().prev().prev().prev().text());
		  	});
		}
	    key_words = key_words.split(' ');	
	    var remark = $('#so_remarks').val();

	    $.ajax({
	        type:'GET',
	        url: url_create,
	        contentType:"application/json",
	        dataType: "json",
	        success: so_callback
	    });
	}
}

function so_callback(data){
    if (data == 'true'){
      alert('提交成功！');
      window.location.href=window.location.href;
        // window.location.href = group_url;
    } 
    if(data =='task name invalid'){
        alert('已存在相同名称的群体分析任务,请重试!');
    }
    if(data =='invalid input for condition'){
      alert('请至少选择一个分析条件！');
    }
    if(data == 'invalid input for filter'){
      alert('请输入合理的影响力或重要度范围！');
    }
    if(data == 'invalid input for count'){
      alert('请选择合理的人数！')
    }
}