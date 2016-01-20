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
	html += '<a id="turnback"  href="javascript:void()" onclick="redraw_result()" style="float:right;margin-right:40px;margin-top:12px;">查看全部任务</a><a data-toggle="modal" id="searchTable" href="#table_search" style="margin-bottom:10px;margin-top:12px;float: right;margin-right: 20px;"">表单搜索</a>';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>计算状态</th><th>发现方式</th><th>操作</th></tr></thead>';
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
		html +='<td><a href="javascript:void(0)" id="task_del">删除</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="commit_control">提交监控</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
    html += '</table>';
	$('#content_manage').append(html);
    
	},

Draw_dis_Table:function(data){
	$('#dis_table').empty();
	var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable"><thead><tr style="text-align:center;"><th>群组名称</th><th>提交人</th><th>时间</th><th>发现方式</th><th>备注</th><th>进度</th><th>操作</th></tr></thead>';
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
	}

}
var Group_identify_task = new Group_identify_task();
function redraw_result(){
	url = '/group/show_task/'; 
	Group_identify_task.call_sync_ajax_request(url, Group_identify_task.ajax_method, Group_identify_task.Draw_resultTable);
}
window.setInterval(redraw,3000);
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
}

var Group_delete_task = new Group_delete_task();
deleteGroup(Group_delete_task);
submit_analyze(Group_delete_task);
submit_control(Group_delete_task);

$('a[id^="commit_control"]').click(function(){
	var a = confirm('确定要提交监控吗？');
 	   if (a == true){
		
		}
	}
);
// $('#turnback').click(function(){
// 	console.log('sdf');
// 	url = '/group/show_task/'; 
// 	Group_identify_task.call_sync_ajax_request(url, Group_identify_task.ajax_method, Group_identify_task.Draw_resultTable);
// });


function submit_analyze(that){
	$('a[id^="group_commit_analyze"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		var percent = $(this).parent().prev().text();
		if(percent.replace(/[^0-9]/ig,"") != 100){
			alert('进度没有达到100%，无法提交分析任务！');
		}
		else{
			url = "/detect/show_detect_result/?task_name=" + temp;
			that.call_sync_ajax_request(url,that.ajax_method,function(data){draw_table(data,"#group_analyze_confirm")});
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
		console.log('aaaa');
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		var percent = $(this).parent().prev().val();
		if(percent != '100%'){
			alert('进度没有达到100%，无法提交监控任务！');
		}
		else{
			url = url + 'task_name=' + temp;
			//that.call_sync_ajax_request(url,that.ajax_method,draw_table);
			draw_table('1',"#group_control_confirm");
			$('#group_control').modal();
		}
	});	
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
    	i = i + 1;
 	}
    html += '</table>'; 
    $(div).append(html);    
}

function analyze_choose_all(){
  $('input[name="analyze_list_option"]').prop('checked', $("#analyze_choose_all").prop('checked'));
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
  	$('[name="analyze_list_option"]').each(function(){
  	    group_confirm_uids.push($(this).parent().prev().prev().prev().prev().text());
  	});
  	console.log(group_confirm_uids);
  	var group_ajax_url = '/detect/add_detect2analysis/';
  	var group_url = '/index/group_result/';
  	var group_name = $('#group_name0').text();
  	console.log(group_name);
  	var job = {"task_name":group_name, "uid_list":group_confirm_uids};
  	console.log(job);
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
  	        alert('提交成功！');
  	    }
  	    else{
  	        alert('已存在相同名称的群体分析任务,请重试一次!');
  	    }
  	}
}

function group_search_button(){ //表单搜索
	var task_name = $('input[name="task_name"]').val();
	var submit_date = $('input[name="submit_date"]').val();
	var state = $('input[name="state"]').val();
	var detect_type = $('select[name="detect_type"] option:selected').val();
	var submit_user = $('input[name="submit_user"]').val();
	console.log(task_name,submit_date,state,detect_type,submit_user);
}