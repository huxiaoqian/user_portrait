function Weibo(){
  this.ajax_method = 'GET';
}
Weibo.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

Draw_content:function(data){
	var html = '';
	$('#weibo_text').empty();
    if(data==''){
        html += "<div style='width:100%;'><span style='margin-left:20px;'>该时段用户未发布任何微博</span></div>";
    }else{
        for(i=0;i<data.length;i++){
            //console.log(data[i].text);
            html += "<div style='width:100%;'><img src='/static/img/pencil-icon.png' style='height:10px;width:10px;margin:0px;margin-right:10px;'><span>"+data[i].text+"</span></div>";
        }

    }
	$('#weibo_text').append(html);
  }
}

var date = '';
var time = '';
var dateStr = '';
var ts = '';
date = $('#date_zh').html();
time = '00:00:00';
dateStr = '2013-'+date+' '+time;
ts = get_unix_time(dateStr);
var Weibo = new Weibo();
var url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);

/*
$('#select_date').change(function(){
	date = $('#select_date').val();
	dateStr = '2015-'+date+' '+time+':00';
	ts = get_unix_time(dateStr);
	url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
	Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);
})
$('#select_time').change(function(){
	 time = $('#select_time').val();
	 dateStr = '2015-'+date+' '+time+':00';
	 ts = get_unix_time(dateStr);
	 url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
	 Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);
})
*/
//dateStr = '2015-'+date+' '+time+':00';
//console.log(dateStr);
//dateStr = '2014-05-08 00:22:11 ';
//
/*
$('#choose_date').click(function(){
	date = $('#select_date').val();
	time = $('#select_time').val();
	dateStr = '2013-'+date+' '+time;
	ts = get_unix_time(dateStr);
	url ="/weibo/show_user_weibo_ts/?uid="+parent.personalData.uid+"&ts="+ts;
    console.log(url);
	Weibo.call_sync_ajax_request(url, Weibo.ajax_method, Weibo.Draw_content);
})
*/
function get_unix_time(dateStr){
    var newstr = dateStr.replace(/-/g,'/'); 
    var date =  new Date(newstr); 
    var time_str = date.getTime().toString();
    return time_str.substr(0, 10);
}

