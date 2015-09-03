 function Tag_search(){
	 this.url = "/tag/submit_attribute/?";
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
		html += '<td name="operate" style="cursor:pointer;" ><a href="javascript:void(0)" data-toggle="modal" data-target="#editor" >编辑</a></td>';
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
		url += get_input_data();
		that.call_sync_ajax_request(url,that.ajax_method,that.searchResult);
	});
}


function get_input_data(){
	var temp='';
    var input_value;
    var input_name;
	 $('.searchinput').each(function(){
        input_name = $(this).attr('name')+'=';
        input_value = $(this).val()+'&';
        temp += input_name;
        temp += input_value;;
    });
	console.log(temp);
	temp = temp.substring(0, temp.length-1);
	return temp;
}

var fbase = new Tag_search();
searchbtnFun(fbase);