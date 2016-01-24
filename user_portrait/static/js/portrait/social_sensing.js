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
	var html = '';
	var item_time = '';
	html += '<table style="so_group_task_body" class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>查看详情</th><th><input name="so_user_choose_all" id="so_user_choose_all" type="checkbox" value="" onclick="so_user_choose_all()" /></th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
		item_time = new Date(item[i][1]*1000).format('yyyy/MM/dd hh:mm')
		html += '<tr><td >'+item[i][0]+'</td><td>'+item_time+'</td><td>'+item[i][2]+'</td><td>'+item[i][3]+'</td>';
		html += '<td><a href=javascript:void(0)  id="so_users">查看详情<a/></td>';
		html += '<td><input name="so_user_list_option" class="search_result_option" type="checkbox"  /></td>'
		html += '</tr>';	
	}
	html += '</tbody>';
    html += '</table>';
	$('#so_group_task').append(html);
	$('#so_group_task_body').dataTable({
       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
       "sPaginationType": "bootstrap",
       "oLanguage": {
           "sLengthMenu": "_MENU_ 每页"
       }
    });
  },
  Draw_task_table: function(data){
  	$('#so_task_table').empty();
  	var item = data;
  	var html = '';
  	var warn = '';
  	var flag = '';
  	var so_flag = '';
  	var time_pro = '';
  	var time_now =  Date.parse(new Date())/1000;
	html += '<table id="so_task_table_body" class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;width:115px;"><th>任务名称</th><th style="width: 60px;">创建人</th><th>创建时间</th><th>终止时间</th><th  style="width: 140px;">进度</th><th style="width:110px;">更多信息</th><th>预警状态</th><th>历史状态</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
	  	var create_d = new Date(item[i]['create_at']*1000).format('yyyy/MM/dd hh:mm'); 
	  	var end_d = new Date(item[i]['stop_time']*1000).format('yyyy/MM/dd hh:mm'); 
	  	time_pro = (((time_now-item[i]['create_at'])/(item[i]['stop_time']-item[i]['create_at']))*100).toFixed(2);
	  	if(time_pro>=100.00){
	  		time_pro=100
	  	}
		if(item[i]['warning_status']==0){
			warn = '无事件';
			//$('#pro').replaceWith('<progress id="pro" progress ::webkit-progress-value{ background: #0064B4; }');
		}else if (item[i]['warning_status']==1){
			warn = '事件爆发';
			$('progress').removeClass('webkit-progress-value').addClass('webkit-progress-value{ background: #333; }');
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
		html += '<td style="width: 60px;">'+item[i]['create_by']+'</td>';
		html += '<td>'+create_d+'</td>';
		html += '<td>'+end_d+'</td>';
		html += '<td "><progress id="pro" style="width:60%"   progress::-webkit-progress-value  { background: #333; } value="'+time_pro+'" max="100"></progress>'+time_pro+'%</td>';
		html += '<td><a href="javascript:void(0)" id="so_keys">查看更多</a></td>';
		html += '<td><a href="javascript:void(0)" id="so_warn">'+warn+'</a></td>';
		html += '<td><a href="javascript:void(0)" id="so_history">查看详情</a></td><td><a href="javascript:void(0)" id="'+so_flag+'">'+flag+'</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="so_task_del">删除</a></td>';
		html += '</tr>';		
	}
	html += '</tbody>';
    html += '</table>';
	$('#so_task_table').append(html);
	$('#so_task_table_body').dataTable({
       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
       "sPaginationType": "bootstrap",
       "oLanguage": {
           "sLengthMenu": "_MENU_ 每页"
       }
    });
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

function draw_control_table(data){
	$('#so_control_confirm').empty();
	var html='';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;height:300px;">';
    html += '<tr><th style="text-align:center">用户ID</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th><input name="so_user_choose_all" id="so_user_choose_all" type="checkbox" value="" onclick="so_user_choose_all()" /></th></tr>';
    for (var i=0;i<data.length;i++) {
        html += '<tr><th style="text-align:center">' + data[i][0] + '</th><th style="text-align:center">' + data[i][1] + '</th><th style="text-align:center">' + data[i][2].toFixed(2) + '</th><th style="text-align:center">' + data[i][3].toFixed(2) + '</th><th style="text-align:center">' + data[i][4].toFixed(2) + '</th><th><input name="so_user_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></th></tr>';
 	}
    html += '</table>'; 
	$('#so_control_confirm').append(html);
}


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

function so_user_choose_all(){
  $('input[name="so_user_list_option"]').prop('checked', $("#so_user_choose_all").prop('checked'));
}

function keys_choose_all(){
  $('input[name="keys_list_option"]').prop('checked', $("#keys_choose_all").prop('checked'));
}

function draw_sensor(data){
	$('#so_sensor_content').empty();
	$('span[id^="so_remark0"]').html(data['remark']);
	var item = data['social_sensors_portrait'];
	var html = '';
	var item_name = '';
	var item_img = '';
	var item_keys = data['keywords'];
    html += '<span  style="margin-right:20px;">关键词：</span>';
    for (var j =0;j<item_keys.length;j++){
    	html += '<span style="margin-right:20px;">'+item_keys[j]+'</span>'
    }
    html += '<table style="margin-top:10px;font-weight:lighter;" class="table table-striped table-bordered bootstrap-datatable datatable responsive" >';
    html += '<tr><th style="text-align:center">头像</th><th style="text-align:center">昵称</th><th style="text-align:center">领域</th><th style="text-align:center">话题</th><th style="text-align:center">重要度</th></tr>';
    for (var i=0;i<item.length;i++) {
    	if(item[i][1]=='unknown'){
    		item_name = '未知';
    	}else{
    		item_name = item[i][1];
    	}
    	if(item[i][2]=='unknown'){
    		item_img = 'http://tp2.sinaimg.cn/1878376757/50/0/1';
    	}else{
    		item_img = item[i][2];
    	}
    	if(item[i][5]==undefined){
    		item_num = '无';
    	}else{
    		item_num = item[i][5].toFixed(2);
    	}
        html += '<tr><td style="text-align:center"><img class="small-photo shadow-5"  title="'+item[i][0]+'"  src="' + item_img + '" ></td><td style="text-align:center">' + item_name + '</td><td style="text-align:center">' + item[i][3]+ '</td><td style="text-align:center">' + item[i][4] + '</td><td style="text-align:center">' + item_num + '</td></tr>';
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
		$('#so_keys_block').modal();
	});
	
	$('a[id^="so_history"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().html();
		url = "/social_sensing/get_task_detail_info/?task_name=" + temp;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_history);
		//draw_table('1',"#group_analyze_confirm");
		remark0 = $(this).parent().prev().prev().prev().html();
		$('span[id^="so_group_name0"]').html(temp);
		$('#so_his_block').modal();
	});

	$('a[id^="so_warn"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		url = "/social_sensing/get_task_detail_info/?task_name=" + temp;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_sensor);
		//draw_table('1',"#group_analyze_confirm");

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
		$('#so_revise').modal();
	});

	$('a[id^="so_users"]').click(function(){
		var temp = $(this).parent().prev().prev().prev().prev().html();
		var remark = $(this).parent().prev().html();
		url = "/detect/show_detect_result/?task_name=" + temp;
		Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,draw_control_table);
		$('span[id^="so_group_name0"]').html(temp);
		$('span[id^="so_remark0"]').html(remark);
		$('#so_control').modal();
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
			var url = '/social_sensing/delete_task/';
			var temp = $(this).parent().prev().prev().prev().prev().prev().prev().prev().prev().html();
			url = url + 'task_name=' + temp;
			console.log(url);
			//window.location.href = url;
			//Social_sense.call_sync_ajax_request(url,Social_sense.ajax_method,callback);
	}
});


function draw_history(data){
	$('#so_his_content').empty();
	$('span[id="so_remark0"]').html(data['remark']);
    var item_his = data['history_status'];
	var html = '';
	var warn = '';
	var item_time = ''
	console.log(item_his);
	console.log(item_his.length);
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;height:300px;">';
    html += '<tr><th style="text-align:center">时间</th><th style="text-align:center">关键词</th><th style="text-align:center">预警状态</th><th style="text-align:center">查看详情</a></th></tr>';
    for (var i=0;i<item_his.length ;i++) {
    	if(item_his[i][2]==0){
			warn = '无事件';
		}else if (item_his[i][2]==1){
			warn = '事件爆发';
		}else {
			warn = '事件跟踪';
		}
		item_time = new Date(item_his[i][0]*1000).format('yyyy/MM/dd hh:mm')
       html += '<tr><td style="text-align:center">' + item_time + '</td><td style="text-align:center">' + item_his[i][1] + '</td><td style="text-align:center">' + warn + '</td><td style="text-align:center"><a href="javascript:void(0)" id="show_detail">查看详情</a></td></tr>';
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
	var key_words0 = '';
	var key_words1 = [];
	console.log(so_time);
	if(flag = true){
	    key_words0 = $('#so_keywords').val();
	 	key_words0 = key_words0.split(/\s+/g);
	    $('[name="keys_list_option"]:checked').each(function(){
		  	    key_words0.push($(this).val());
		  	});
	    if (so_user_option == 'so_all_users'){
	    }
	    else{              //single_user or multi_user with extension
	    	var group_names = [];
		  	$('[name="so_user_list_option"]:checked').each(function(){
		  	    group_names.push($(this).parent().prev().prev().prev().prev().prev().prev().text());
		  	});
		}
	    //key_words0 = key_words0.split(/\s+/g);
	    //key_words0.push(key_words1)
	    console.log(key_words0);
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

have_keys(['sdfa','asdfasg','1231','asdfa','dsga4','12sdfa']);

function have_keys(data){
	$('#show_keys').empty();
	html = '';
	for(var i=0;i<data.length;i++){
		html += '<input name="keys_list_option" class="search_result_option" value="'+data[i]+'" type="checkbox"/><span style="margin-right:40px;">'+data[i]+'</span> ';
	}
	$('#show_keys').append(html);
}