function Base(){
}
Base.prototype.simple_search_url = function (term){
    return "/index/search_result/?stype=1&term=" + term;
}
Base.prototype.advanced_search_url = function (term){
    return "/index/search_result/?stype=2&term=" + term;
}

Base.prototype.call_ajax_request = function(url, callback){
    $.ajax({
        url:url,
        type:"get",
        dataType: "json",
        async: true,
        success: callback
    })
}

function bindSearchFunc(that){ 
    var simple_url = that.simple_search_url('');
    var advanced_url = that.advanced_search_url('');
    $("#simple_search").click(function(){
        window.location.href = simple_url
    });
}

var base = new Base();
bindSearchFunc(base);
