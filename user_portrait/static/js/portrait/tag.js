function Tag(){
  this.ajax_method = 'GET';
}
Tag.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_tag_table:function(data){
	//console.log(data);
    $('#Tagtable').empty();
    var item = data;
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th style="width:100px;">全选<input type="checkbox" style="margin-left:10px;"></th><th>标签类别</th><th>标签名</th><th>创建者</th><th>时间</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(i=0;i<item.length;i++){
		html += '<tr>'
		html += '<td name="chose" style="text-align:center;"><input type="checkbox"></input></td>';
		html += '<td name="tagClass">'+item[i].attribute_name+'</td>';
		html += '<td name="tagName">'+item[i].attribute_value+'</td>';
		html += '<td name="creater">'+item[i].user+'</td>';
		html += '<td name="time">'+item[i].date+'</td>'
		html += '<td name="operate" style="cursor:pointer;" ><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" >编辑</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#Tagtable').append(html);
  }
}
url ="/tag/search_attribute/";
var Tag = new Tag();
Tag.call_sync_ajax_request(url, Tag.ajax_method, Tag.Draw_tag_table);

