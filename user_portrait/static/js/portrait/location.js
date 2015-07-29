function Location(){
  this.ajax_method = 'GET';
}
Location.prototype = {   //获取数据，重新画表
  call_sync_ajax_request:function(url, method, callback){
    $.ajax({
      url: url,
      type: method,
      dataType: 'json',
      async: false,
      success:callback
    });
  },

  location:function(data){
	var description = document.getElementById('location_description');
	description.innerHTML = data['description'];
  }
}
 url ="/attribute/location/?uid="+parent.personalData.uid;
	var Location = new Location();
	Location.call_sync_ajax_request(url, Location.ajax_method, Location.location);
