 function Tag_delete(){
	 this.url = "/tag/delete_attribute/?";
}
Tag_delete.prototype = {   //删除
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
	$('a[id^="delTag"]').click(function(e){
		var url = that.url;
		var temp = $(this).parent().prev().prev().prev().prev().html();
		console.log(temp);
		url = url + 'attribute_name=' + temp;
		//window.location.href = url;
		that.call_sync_ajax_request(url,that.ajax_method,that.del);
		console.log(url);
	});
}

var Tag_delete = new Tag_delete();
deleteGroup(Tag_delete);
