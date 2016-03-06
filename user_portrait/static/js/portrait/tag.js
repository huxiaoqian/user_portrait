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
		var item_value = item[i].attribute_value.split('&').join('/');
        if (!item_value){
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" onclick="editclick()" style="color:darkred;font-size:10px;" title="添加标签名">添加</a></td>';
        }
        else{
            html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" onclick="editclick()" title="点击编辑">'+item_value+'</a></td>';
        }
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
var url ="/tag/search_attribute/";
var Tag = new Tag();
Tag.call_sync_ajax_request(url, Tag.ajax_method, Tag.Draw_tag_table);

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
		html += '<td name="attribute_value"><a href="" data-toggle="modal" data-target="#editor" id="currentEdit" onclick="editclick()"  title="点击编辑">'+item[i].attribute_value+'</a></td>';
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
		console.log(url);
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
	temp = temp.substring(0, temp.length-1);
	return temp;
}

var fbase = new Tag_search();
searchbtnFun(fbase);

function Tag_add(){
  this.url = '/tag/submit_attribute/?';
}
Tag_add.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

NewTag:function(data){
  location.reload();
  }
}

function tagAddFun(that){
	$('#newTag').off("click").click(function(){
		var url = that.url;
        var choose_data = get_input_data();
        if (choose_data != false){
            url += choose_data;
            that.call_sync_ajax_request(url,that.ajax_method,that.NewTag);
        }
	});
}

function get_input_data(){
	var temp='';
    var input_value;
    var input_name;
	var tagnames = document.getElementsByName("attribute_name");
	input_name = "attribute_name=";
	input_value = document.getElementsByName("attribute_name")[tagnames.length-1].value;
	var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]";
	if(!input_value.match(reg)){
		alert('标签类型只能包含英文、汉字、数字和下划线，请重新输入');
		return false;
	}
	temp += input_name;
    temp = temp + input_value +'&';
	var tagnames = document.getElementsByName("attribute_value");
	input_name = "attribute_value=";
	var value = '';
    var value_list = new Array();
	for(i=4;i<tagnames.length;i++){
        var this_value = document.getElementsByName("attribute_value")[i].value;
		if(this_value){
			value_list.push(this_value);
		}
	}
	value = value_list.join(',');
	input_value = value+'&';
	temp += input_name;
    temp += input_value;
	input_name = "user=";
	input_value ="admint&";
	temp += input_name;
    temp += input_value;
	input_name = "date=";
	input_value = new Date().format('yyyy-MM-dd') + '&';
	temp += input_name;
    temp += input_value;
	temp = temp.substring(0, temp.length-1);
	return temp;
}
var TagAdd = new Tag_add();
tagAddFun(TagAdd);

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
		url = url + 'attribute_name=' + temp;
		if(confirm("确认要删除吗？")){
			that.call_sync_ajax_request(url,that.ajax_method,that.del);
		}
		//window.location.href = url;
	});
}

var Tag_delete = new Tag_delete();
deleteGroup(Tag_delete);

function TagChange(){
  this.url = '/tag/change_attribute/?';
}
TagChange.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

ChangeTag:function(data){
   location.reload();
  }
}

function tagChangeFun(that){
	$('#modifySave').off("click").click(function(){
		var url = that.url;
		url += input_data();
		that.call_sync_ajax_request(url,that.ajax_method,that.ChangeTag);
	});
}

function input_data(){
	var temp='';
    var input_value;
    var input_name;
	input_name = "attribute_name=";
	input_value = $('#attributeName').html()+'&';
	temp += input_name;
    temp += input_value;

	var tagnames = $('.tagName').length;
	input_name = "attribute_value=";
	var value = '';
	var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";	
	for(i=0;i<tagnames;i++){
		value += $(".tagName").eq(i).html()+',';
	}
	value = value.substring(0,value.length-1);
	input_value = value+'&';
	temp += input_name;
    temp += input_value;

	input_name = "user=";
	input_value ="admint&";
	temp += input_name;
    temp += input_value;
	input_name = "date=";
	input_value =new Date().format('yyyy-MM-dd') + '&';
	temp += input_name;
    temp += input_value;
	temp = temp.substring(0, temp.length-1);
	return temp;
}

function editclick(){
	    add_flag = false;
        var tagNames =  $(this).text();
        console.log(tagNames);
        if (tagNames.indexOf('/') > -1){
            tagname = tagNames.split('/');
        }
  		$('#EDIT').empty();
  		var html = '';
  		html += '<div class="" style="margin-bottom:10px;"><span style="">标签类别&nbsp;&nbsp;&nbsp;&nbsp;</span>';
  		html += '<span style="color:blue;" id="attributeName">'+$(this).parent().prev().html()+'</span ></div>';
  		html += '<div class="" id=""><span style="margin-right:15px;">标签名</span>';
  		for(i=0;i<tagname.length;i++){
  			html += '<span class="tagbg" id="" name="attrName"><span class="tagName">'+tagname[i]+'</span><a  class="delCon" id="delIcon"></a></span>';
  		}
  		//html += '<input name="attribute_value" class="inputbox " type="text" value="" style="line-height:36px;">'
  		html += '<span class="smallAdd"></span>'
  		html += '</div>';
  		$('#EDIT').append(html);
  		$(".smallAdd").click(function(){
              //console.log("sadsd");
              if (!add_flag){
                  add_flag = true;
                  $(".smallAdd").before('<input name="newtag" id="newtag" class="input_tag_box" style="width:110px;" onkeydown="javascript:if (event.keyCode==13) addNew();"type="text" value="" style="line-height:36px;">');
              }
          });
  		$('a[id^="delIcon"]').click(function(e){
  			$(this).parent().remove();
  		});
}

var TagChange = new TagChange();
//Tag.call_sync_ajax_request(url, Tag.ajax_method, Tag.AddTag);
tagChangeFun(TagChange);

