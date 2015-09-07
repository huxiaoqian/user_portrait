function Tag_show(){
  this.ajax_method = 'GET';
}
Tag_show.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_tag:function(data){
	//console.log(data);
	var item;
	var name;
	var value;
	var attrTag;
    for(var key in data){
		item = data[key];
	}
    for(i=0;i<item.length;i++){
		attrTag = item[i].split(':');
		console.log(attrTag[0]);
	}
  }
}
//url ="/tag/show_user_tag/?uid_list="+parent.personalData.uid;
url ="/tag/show_user_tag/?uid_list=3697357313"
var Tag_show = new Tag_show();
Tag_show.call_sync_ajax_request(url, Tag_show.ajax_method, Tag_show.Draw_tag);

