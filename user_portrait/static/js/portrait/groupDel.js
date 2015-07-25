 function Group_delete(){
	 this.url = "/group/delete_group_task/?";
}
Group_delete.prototype = {   //群组搜索
call_sync_ajax_request:function(url, method, callback){
	console.log(url);
    $.ajax({
      url: url,
      type: 'GET',
      dataType: 'json',
      async: false,
      success:callback
    });
}
}

function deleteGroup(that){
	$('#del').off("click").click(function(){
		var url = that.url;
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		url = url + 'task_name=' + temp;
		window.location.href = url;
		alert(url);
	});
}

var Group_delete = new Group_delete();
deleteGroup(Group_delete);
