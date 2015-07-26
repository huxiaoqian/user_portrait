 function Group_search(){
	 this.url = "/group/show_task/?";
}
Group_search.prototype = {   //群组搜索
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

function searchGroup(that){
	$('#searchbtn').off("click").click(function(){
		var url = that.url;
		$("#float-wrap").addClass("hidden");
        $("#SearchTab").addClass("hidden");
		url += get_input_data();
		window.location.href = url;
		alert(url);
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
	temp = temp.substring(0, temp.length-1);
	return temp;
}

var Group_search = new Group_search();
searchGroup(Group_search);
