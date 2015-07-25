 function Search_weibo(){
  this.ajax_method = 'GET';
}


Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    console.log(url);
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  Draw_table: function(data){
    console.log(data);
}
}
 
var Search_weibo = new Search_weibo(); 

this.ajax_url = function(date){
    return "/overview/show/?date=2013-09-07";
}

$(document).ready(function(){
	var downloadurl = window.location.host;
    weibo_url =  'http://' + downloadurl + "/overview/show/?date=2013-09-07";
    Search_weibo.call_sync_ajax_request(weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_table);
})
