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
    //console.log(data);
    $('#content_manage').empty();
    var item = data;
	var html = '';
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
	html += '<tr><td>名称</td><td>人</td><td>20160107</td><td>发现</td><td>1</td><td> </td><td><a href="javascript:void(0)" id="group_commit_analyze">提交分析</a>&nbsp;&nbsp;&nbsp;<a href="javascript:void(0)" id="group_commit_control" >提交监控</a></td></tr>';
	html += '</tbody>';
	html += '</table>';
	$('#dis_table').append(html);
}

}
var Group_identify_task = new Group_identify_task();
url = '/group/show_task/' 
Group_identify_task.call_sync_ajax_request(url, Group_identify_task.ajax_method, Group_identify_task.Draw_resultTable);
Group_identify_task.call_sync_ajax_request(url, Group_identify_task.ajax_method, Group_identify_task.Draw_dis_Table);

function Group_delete_task(){
	 this.url = "/group/delete_group_task/?";
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


function submit_analyze(that){
	$('a[id^="group_commit_analyze"]').click(function(e){
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		url = url + 'task_name=' + temp;
		//that.call_sync_ajax_request(url,that.ajax_method,draw_table);
		draw_table('1',"#group_analyze_confirm");
		$('#group_analyze').modal();
	});	
}

function submit_control(that){
	$('a[id^="group_commit_control"]').click(function(e){
		console.log('aaaa');
		var temp = $(this).parent().prev().prev().prev().prev().prev().prev().html();
		url = url + 'task_name=' + temp;
		//that.call_sync_ajax_request(url,that.ajax_method,draw_table);
		draw_table('1',"#group_control_confirm");
			console.log(1);
		$('#group_control').modal();
			console.log(2);
	});	
}


function draw_table(data,div){
	$(div).empty();
	//var datas = data['topic'];
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatable responsive">';
    html += '<tr><th style="text-align:center">用户ID</th><th style="text-align:center">昵称</th><th style="text-align:center">活跃度</th><th style="text-align:center">重要度</th><th style="text-align:center">影响力</th><th><input name="analyze_choose_all" id="analyze_choose_all" type="checkbox" value="" onclick="analyze_choose_all()" /></th></tr>';
    var i = 1;
    //for (var key in datas) {
        html += '<tr><th style="text-align:center">' + 'id' + '</th><th style="text-align:center">' + '昵称' + '</th><th style="text-align:center">' + '10' + '</th><th style="text-align:center">' + '20' + '</th><th style="text-align:center">' + '30' + '</th><th><input name="analyze_list_option" class="search_result_option" type="checkbox" value="' + '1' + '" /></th></tr>';
    //	i = i + 1;
 	//}
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