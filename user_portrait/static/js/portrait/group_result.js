 function Group_result(){
  this.ajax_method = 'GET';
}
Group_result.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    console.log(url);
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
    $('#Grouptable').empty();
    var item = data;
	var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">	<th>群组名称</th><th>时间</th><th>群组人数</th><th>备注</th><th>状态</th><th>操作</th></tr></thead>';
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
		if(item[i][5]==1){
			html += '<td>已完成</td>';
		}else{
			html += '<td>正在计算</td>';
		}
		html +='<td><a href="" id="del">删除</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
    html += '</table>';
	$('#Grouptable').append(html);
}
}
var Group_result = new Group_result();
url = '/group/show_task/' 
Group_result.call_sync_ajax_request(url, Group_result.ajax_method, Group_result.Draw_resultTable);

