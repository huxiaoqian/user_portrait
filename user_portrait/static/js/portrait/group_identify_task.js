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

var current_date = new Date().format('yyyy/MM/dd hh:mm');
var max_date = '+1970/01/30';
var min_date = '-1970/01/30';
$('input[name="con_end_time"]').datetimepicker({value:current_date,minDate:current_date,step:10});

function Group_identify_task(){
  this.ajax_method = 'GET';
}
Group_identify_task.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_resultTable: function(data){
    console.log('bbb');
    $('#content_manage').empty();
    var item = data;
	var html = '';
	html += '<a id="turnback"  href="javascript:void()" onclick="redraw_result()" style="float:right;margin-right:40px;margin-top:12px;">查看全部任务</a><a data-toggle="modal" id="searchTable" href="#task_search" style="margin-bottom:10px;margin-top:12px;float: right;margin-right: 20px;"">表单搜索</a>';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>计算状态</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	for (i=0;i<item.length;i++){
		html += '<tr>';
		var time0 = new Date(item[i][1]*1000).format('yyyy/MM/dd hh:mm')
		html += '<td name="task_name">'+item[i][0]+'</td>';
		html += '<td>'+time0+'</td>';
		html += '<td>'+item[i][2]+'</td>';
		html += '<td>'+item[i][3]+'</td>';
		if(item[i][4]==1){
			html += '<td><a style="cursor:hand;" href="/index/group_analysis/?name=' + item[i][0]+ '">已完成</a></td>';
		}else{
			html += '<td>正在计算</td>';
		}
		html +='<td><a href="javascript:void(0)" id="analyze_del">删除</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="commit_control">提交监控</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
    html += '</table>';
	$('#content_manage').append(html);
    
	},

Draw_dis_Table:function(data){
	$('#dis_table').empty();
	var html = '';
	html += '<a id="turnback"  href="javascript:void(0)" onclick="redraw()" style="float:right;margin-right:40px;margin-top:12px;">查看全部任务</a><a data-toggle="modal" id="searchTable" href="#table_search" style="margin-bottom:10px;margin-top:12px;float: right;margin-right: 20px;"">表单搜索</a>';
	html += '<table id="dis_table_body" class="table table-bordered table-striped table-condensed datatable"><thead><tr style="text-align:center;"><th>群组名称</th><th>提交人</th><th>时间</th><th>发现方式</th><th>备注</th><th>进度</th><th>操作</th></tr></thead>';
	html += '<tbody>';
	//j = 40;
	var dis_type='';
	for (i=0;i<data.length;i++){
		if(data[i][3]=='single'){
			dis_type='单种子用户群体发现';
		}else if(data[i][3]=='multi'){
			dis_type='多种子用户群体发现';
		}else if(data[i][3]=='attribute'){
			dis_type='特定属性及模式群体发现';
		}else if(data[i][3]=='event'){
			dis_type='特定事件群体发现';
		}else{
			dis_type='社会感知自动群体发现';
		}
		html += '<tr><td>'+data[i][0]+'</td><td>'+data[i][1]+'</td><td>'+data[i][2]+'</td><td>'+dis_type+'</td><td>'+data[i][4]+'</td><td><progress value="'+data[i][5]+'" max="100"></progress>&nbsp;&nbsp;'+data[i][5]+'%</td><td><a href="javascript:void(0)" id="group_commit_analyze">提交分析</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="group_commit_control" >提交监控</a>&nbsp;&nbsp;<a href="javascript:void(0)" id="task_del">删除</a></td></tr>';
		//j += 10;
	}
	html += '</tbody>';
	html += '</table>';
	$('#dis_table').append(html);
    deleteGroup(Group_delete_task);
	submit_analyze();
	submit_control();
    $('#dis_table_body').dataTable({
       "sDom": "<'row'<'col-md-6'l ><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
       "sPaginationType": "bootstrap",
       "oLanguage": {
           "sLengthMenu": "_MENU_ 每页"
       }
    });
	}

}
var Group_identify_task = new Group_identify_task();
function redraw_result(){
	url = '/group/show_task/'; 
	Group_identify_task.call_sync_ajax_request(url, Group_identify_task.ajax_method, Group_identify_task.Draw_resultTable);
	deleteGroup(Group_delete_task);
	control_click();
}
window.setInterval(redraw,30000);
function redraw(){
	deurl= '/detect/show_detect_task/';
	Group_identify_task.call_sync_ajax_request(deurl, Group_identify_task.ajax_method, Group_identify_task.Draw_dis_Table);
}
redraw();
redraw_result();

function Group_delete_task(){
	 this.url = "/detect/delete_task/?";
}
Group_delete_task.prototype = {   //群组搜索
	call_sync_ajax_request:function(url, method, callback){
	    $.ajax({
	      url: url,
	      type: 'GET',
	      dataType: 'json',
	      async: true,
	      success:callback
    	});
	},
	del:function(data){
		location.reload();
	}
}

function deleteGroup(that){
	$('a[id^="task_del"]').click(function(e){
		var a = confirm('确定要删除吗？');
    	if (a == true){
			var url = that.url;
			var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
			url = url + 'task_name=' + temp;
			console.log(url);
			//window.location.href = url;
			that.call_sync_ajax_request(url,that.ajax_method,that.del);
		}
	});	
	$('a[id^="analyze_del"]').click(function(e){
		var a = confirm('确定要删除吗？');
    	if (a == true){
			var url = that.url;
			var temp = $(this).parent().prev().prev().prev().prev().prev().html();
			url = url + 'task_name=' + temp;
			console.log(url);
			//window.location.href = url;
			that.call_sync_ajax_request(url,that.ajax_method,that.del);
		}
	});	
}

var Group_delete_task = new Group_delete_task();
// deleteGroup(Group_delete_task);
// submit_analyze(Group_delete_task);
// submit_control(Group_delete_task);

function control_click(){
	$('a[id^="commit_control"]').click(function(){
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		var remark0 =  $(this).parent().prev().prev().html();
		url = "/detect/show_detect_result/?task_name=" + temp;
		Group_identify_task.call_sync_ajax_request(url,Group_identify_task.ajax_method,draw_control_table);
		$('input[name="con_group_name"]').val(temp);
		$('input[name="con_remark"]').val(remark0);
		$('#group_control').modal();
	});
}
var current_date = new Date().format('yyyy/MM/dd hh:mm');
var max_date = '+1970/01/30';
var min_date = '-1970/01/30';
$('input[name="so_end_time"]').datetimepicker({value:current_date,minDate:current_date,step:10});

function submit_analyze(that){
	$('a[id^="group_commit_analyze"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		var percent = $(this).parent().prev().text();
		if(percent.replace(/[^0-9]/ig,"") != 100){
			alert('进度没有达到100%，无法提交分析任务！');
		}
		else{
			url = "/detect/show_detect_result/?task_name=" + temp;
			Group_identify_task.call_sync_ajax_request(url,Group_identify_task.ajax_method,function(data){draw_table(data,"#group_analyze_confirm")});
			//draw_table('1',"#group_analyze_confirm");
			remark0 = $(this).parent().prev().prev().html();
			$('span[id^="group_name0"]').html(temp);
			$('span[id^="remark0"]').html(remark0);
			$('#group_analyze').modal();
		}
	});	
}

function submit_control(that){
	$('a[id^="group_commit_control"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		var percent = $(this).parent().prev().text();
		var remark0 = $(this).parent().prev().prev().html();
		// if(percent.replace(/[^0-9]/ig,"") != 100){
		// 	alert('进度没有达到100%，无法提交分析任务！');
		// }
		// else{
			url = "/detect/show_detect_result/?task_name=" + temp;
			Group_identify_task.call_sync_ajax_request(url,Group_identify_task.ajax_method,draw_control_table);
			//that.call_sync_ajax_request(url,that.ajax_method,draw_table);
			$('input[name="con_group_name"]').val(temp);
			$('input[name="con_remark"]').val(remark0);
			$('#group_control').modal();
		 //}
	});	
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

function draw_control_table(data){
	$('#group_control_confirm').empty();
	var html='';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" >';
    html += '<tr><th style="text-align:center">用户ID</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th><input name="control_choose_all" id="control_choose_all" type="checkbox" value="" onclick="control_choose_all()" /></th></tr>';
    for (var i=0;i<data.length;i++) {
        html += '<tr><td style="text-align:center">' + data[i][0] + '</td><td style="text-align:center">' + data[i][1] + '</td><td style="text-align:center">' + data[i][2].toFixed(2) + '</td><td style="text-align:center">' + data[i][3].toFixed(2) + '</td><td style="text-align:center">' + data[i][4].toFixed(2) + '</td><td><input name="control_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></td></tr>';
 	}
    html += '</table>'; 
	$('#group_control_confirm').append(html);
}



function draw_table(data,div){
	console.log(data);
	console.log(div);
	$(div).empty();
	//var datas = data['topic'];
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive" style="overflow-y:auto;height:300px;">';
    html += '<tr><th style="text-align:center">用户ID</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th><input name="analyze_choose_all" id="analyze_choose_all" type="checkbox" value="" onclick="analyze_choose_all()" /></th></tr>';
    for (var i=0;i<data.length;i++) {
        html += '<tr><th style="text-align:center">' + data[i][0] + '</th><th style="text-align:center">' + data[i][1] + '</th><th style="text-align:center">' + data[i][2].toFixed(2) + '</th><th style="text-align:center">' + data[i][3].toFixed(2) + '</th><th style="text-align:center">' + data[i][4].toFixed(2) + '</th><th><input name="analyze_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></th></tr>';
    	//i = i + 1;
 	}
    html += '</table>'; 
    $(div).append(html);    
}

function analyze_choose_all(){
	$('input[name="analyze_list_option"]').prop('checked', $("#analyze_choose_all").prop('checked'));
}

function control_choose_all(){
	$('input[name="control_list_option"]').prop('checked', $("#control_choose_all").prop('checked'));
}

function keys_choose_all(){
	$('input[name="keys_list_option"]').prop('checked', $("#keys_choose_all").prop('checked'));	
}

function delRow(obj){
  var Row = obj.parentNode;
  while(Row.tagName.toLowerCase()!="tr"){
    Row = Row.parentNode;
  }
  Row.parentNode.removeChild(Row);
}

function group_analyze_confirm_button(){
  	var group_confirm_uids = [];
  	$('[name="analyze_list_option"]:checked').each(function(){
  	    group_confirm_uids.push($(this).parent().prev().prev().prev().prev().text());
  	});
  	console.log(group_confirm_uids);
  	var group_ajax_url = '/detect/add_detect2analysis/';
  	var group_url = '/index/group_result/';
  	var group_name = $('#group_name0').text();
  	console.log(group_name);
  	var job = {"task_name":group_name, "uid_list":group_confirm_uids};
  	console.log(job);
  	// $.ajax({
  	//     type:'POST',
  	//     url: group_ajax_url,
  	//     contentType:"application/json",
  	//     data: JSON.stringify(job),
  	//     dataType: "json",
  	//     success: callback
  	// });
  	function callback(data){
  	    console.log(data);
  	    if (data == '1'){
  	        alert('提交成功！');
  	    }
  	    else{
  	        alert('已存在相同名称的群体分析任务,请重试一次!');
  	    }
  	}
}

$('#group_control_confirm_button').click(function(){
	group_control_data();
});

function group_control_check(){             // check validation 
    //group_information check starts  
    var group_name = $('input[name="con_group_name"]').val();
    var remark = $('input[name="con_remark"]').val();
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
function group_control_data(){
	var flag = group_control_check();
	var a = new Array();
    a['task_name'] = $('input[name="con_group_name"]').val();
    a['remark'] = $('input[name="con_remark"]').val();
	a['stop_time'] = Date.parse($('input[name="con_end_time"]').val())/1000;
	a['keywords'] = '';
	a['create_at'] =  Date.parse(new Date())/1000;
	a['social_sensors'] =[];
	var url0 = [];
	var url1 = '';
	var url_create = '/social_sensing/create_task/?';
	if(flag = true){
	   a['keywords'] = $('input[name="con_keywords"]').val();
	    if(a['keywords'].length){
		 	a['keywords'] = a['keywords'].split(/\s+/g);
	    }else{
	    	a['keywords'] = [];
	    }
	    $('[name="keys_list_option"]:checked').each(function(){
		  	    a['keywords'].push($(this).val());
		  	});
	    $('[name="control_list_option"]:checked').each(function(){
		  	    a['social_sensors'].push($(this).parent().prev().prev().prev().prev().prev().text());
		  	});
		for(var k in a){
			if(a[k]){
				url0.push(k +'='+a[k]);
			}
		}
		if(url0.length > 1){
			url1 = url0.join('&');
		}else{
			url1 = url0;
		}
		url_create += url1;
		console.log(url_create);
	    // $.ajax({
	    //     type:'GET',
	    //     url: url_create,
	    //     contentType:"application/json",
	    //     dataType: "json",
	    //     success: con_callback
	    // });
	}
}

function con_callback(data){
	if(data.length != 0){
		alert('操作成功！');
	}
}


function group_search_button(){ //表单搜索
	var a = new Array();
	var url0 = [];
	var url1 = '';
	a['task_name'] = $('input[name="task_name"]').val();
	a['submit_date'] = $('input[name="submit_date"]').val();
	a['state'] = $('input[name="state"]').val();
	a['detect_type'] = $('select[name="detect_type"] option:selected').val();
	a['submit_user'] = $('input[name="submit_user"]').val();
	for(var k in a){
		if(a[k]){
			url0.push(k +'='+a[k]);
		}
	}
	if(url0.length > 1){
		url1 = url0.join('&');
	}else{
		url1 = url0;
	}
	var search_url = '/detect/search_detect_task/?'+url1;
	console.log(search_url);
	$.ajax({
  	    type:'GET',
  	    url: search_url,
  	    contentType:"application/json",
  	    dataType: "json",
  	    success: Group_identify_task.Draw_dis_Table
  	});
}

function task_search_button(){ //表单搜索
	var a = new Array();
	var url0 = [];
	var url1 = '';
	a['task_name'] = $('input[name="task_name0"]').val();
	a['submit_date'] = $('input[name="submit_date0"]').val();
	a['state'] = $('input[name="state0"]').val();
	var status =  $('input[name="status0"]').val();
	a['status'] = $('select[name="task_type"] option:selected').val();
	for(var k in a){
		if(a[k]){
			url0.push(k +'='+a[k]);
		}
	}
	if(url0.length > 1){
		url1 = url0.join('&');
	}else{
		url1 = url0;
	}
	var search_url = '/group/show_task/?'+url1;
	console.log(search_url);
	$.ajax({
  	    type:'GET',
  	    url: search_url,
  	    contentType:"application/json",
  	    dataType: "json",
  	    success: Group_identify_task.Draw_resultTable
  	});
}