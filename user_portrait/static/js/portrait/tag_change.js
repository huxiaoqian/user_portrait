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
	//console.log(data);
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
	var tagnames = document.getElementsByName("attribute_name");
	//console.log(tagnames);
	input_name = "attribute_name=";
	input_value = document.getElementsByName("attribute_name")[tagnames.length-2].value+'&';
	temp += input_name;
    temp += input_value;
	var tagnames = document.getElementsByName("attribute_value");
	input_name = "attribute_value=";
	var value = '';
	var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
	for(i=4;i<tagnames.length-1;i++){
		/*
		console.log(document.getElementsByName("attribute_value")[i].value);
		if(!document.getElementsByName("attribute_value")[i].value.match(reg)){
			alert('标签名只能包含英文、汉字、数字和下划线，请重新输入');
			return;
		}
		*/
		if(document.getElementsByName("attribute_value")[i].value==undefined){
			value += '';
		}else{
			value += document.getElementsByName("attribute_value")[i].value;
			value += ',';
		}
		
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
	input_value =currentDate()+'&';
	temp += input_name;
    temp += input_value;
	temp = temp.substring(0, temp.length-1);
	console.log(temp);
	return temp;
}
function currentDate(){
	var myDate = new Date();
	var yy = myDate.getFullYear();
	var mm = myDate.getMonth() + 1;
	if(mm<10){
		mm = '0'+mm.toString();
		
	}
	var dd = myDate.getDate();
	if(dd<10){
		dd = '0'+dd.toString();
	}
	
	var date = yy.toString()+ '-' + mm.toString() + '-' + dd.toString();
	console.log(date);
	return date;
}
var TagChange = new TagChange();
//Tag.call_sync_ajax_request(url, Tag.ajax_method, Tag.AddTag);
tagChangeFun(TagChange);

