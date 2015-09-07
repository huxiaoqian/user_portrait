 function Tag_search(){
	 this.url = "/tag/search_attribute/?";
}
Tag_search.prototype = {   //群组搜索
call_sync_ajax_request:function(url, method, callback){
	$.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
},
searchResult:function(data){
	 $('#Tagtable').empty();
    var item = data;
    var html = '';
	html += '<table class="table table-bordered table-striped table-condensed datatable" >';
	html += '<thead><tr style="text-align:center;">';
	html += '<th>标签类别</th><th>标签名</th><th>创建者</th><th>时间</th><th>操作</th></tr>';
	html += '</thead>';
	html += '<tbody>';
	for(i=0;i<item.length;i++){
		html += '<tr>'
		html += '<td name="attribute_name">'+item[i].attribute_name+'</td>';
		html += '<td name="attribute_value"><a href="javascript:void(0)" data-toggle="modal" data-target="#editor" title="点击编辑">'+item[i].attribute_value+'</a></td>';
		html += '<td name="creater">'+item[i].user+'</td>';
		html += '<td name="time">'+item[i].date+'</td>'
		html += '<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" id="delTag">删除</a></td>';
		html += '</tr>';
	}
	html += '</tbody>';
	html += '</table>';
	$('#Tagtable').append(html);
}
}

function searchbtnFun(that){
	$('#searchbtn').off("click").click(function(){
		var url = that.url;
		$("#float-wrap").addClass("hidden");
        $("#SearchTab").addClass("hidden");
		url += get_data();
		that.call_sync_ajax_request(url,that.ajax_method,that.searchResult);
	});
}


function get_data(){
	var temp='';
    var input_value;
    var input_name;
	 $('.searchinput').each(function(){
        input_name = $(this).attr('name')+'=';
        input_value = $(this).val()+'&';
        temp += input_name;
        temp += input_value;;
    });
	//console.log(temp);
	temp = temp.substring(0, temp.length-1);
	return temp;
}

var fbase = new Tag_search();
searchbtnFun(fbase);