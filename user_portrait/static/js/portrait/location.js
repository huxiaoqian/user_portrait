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
	
	var description1 = document.getElementById('location_description1');
	var description3 = document.getElementById('location_description3');
	//description.innerHTML = data['description'];
	var length =  data['description'].length;
	if(length==2){
		description1.style.color="red";
		description1.innerHTML = data['description'][0];
		document.getElementById('location_description2').innerHTML = data['description'][1];
	}else{
		description1.style.color="red";
		description1.innerHTML = data['description'][0];
		document.getElementById('location_description2').innerHTML = data['description'][1];
		description3.style.color="red";
		description3.innerHTML = data['description'][2];
		document.getElementById('location_description4').innerHTML = data['description'][3];
	}

  }
}
 url ="/attribute/location/?uid="+parent.personalData.uid;
	var Location = new Location();
	Location.call_sync_ajax_request(url, Location.ajax_method, Location.location);
