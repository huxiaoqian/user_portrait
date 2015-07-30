function Base(){
    this.advanced_search_url = "/index/search_result/?stype=2&";
}
Base.prototype.simple_search_url = function (term){
    return "/index/search_result/?stype=1&term=" + term;
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
    $("#simple_search").click(function(){
        var term = $("#keyword").val();
        var simple_url = that.simple_search_url(term);
        console.log(simple_url);
        window.location.href = simple_url;
    });
    $("#bluebtn").off("click").click(function(){
        var advanced_url = that.advanced_search_url;
        $("#float-wrap").addClass("hidden");
        $("#supersearch").addClass("hidden");
        advanced_url += get_input_data();
        window.location.href = advanced_url;
    });
}
function get_input_data(){
    var temp='';
    var input_value;
    var input_name;
    $('.ad-search').each(function(){
        input_name = $(this).attr('name')+'=';
        input_value = $(this).val()+'&';
        temp += input_name;
        temp += input_value;;
    });
    temp = temp.substring(0, temp.length-1);

    var domain_url = '&domain=';
    $("[name='domain']:checked").each(function(){
        domain_url += $(this).val() + ',';
    });
    temp += domain_url;
    temp = temp.substring(0, temp.length-1);

    var topic_url = '&topic=';
    $("[name='topic']:checked").each(function(){
        topic_url += $(this).val() + ',';
    });
    temp += topic_url;
    temp = temp.substring(0, temp.length-1);
    return temp;
}

var base = new Base();
bindSearchFunc(base);
