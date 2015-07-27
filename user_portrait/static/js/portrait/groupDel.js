 function Group_delete(){
	 this.url = "/group/delete_group_task/?";
}
Group_delete.prototype = {   //群组搜索
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
	$('a[id^="del"]').click(function(e){
		var url = that.url;
		var temp = $(this).parent().prev().prev().prev().prev().prev().html();
		url = url + 'task_name=' + temp;
		//window.location.href = url;
		that.call_sync_ajax_request(url,that.ajax_method,that.del);
		console.log(url);
	});
}

var Group_delete = new Group_delete();
deleteGroup(Group_delete);
