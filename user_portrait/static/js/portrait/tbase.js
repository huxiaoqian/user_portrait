function Base(){
    this.advanced_search_url = "/index/search_result/?stype=2&";
}
Base.prototype.simple_search_url = function (term){
    return "/index/search_result/?stype=1&term=" + term;
}


function bindSearchFunc(that){ 
    $("#keyword").bind('keyup', function(e){
        var ev = document.all?window.event:e;
        if (ev.keyCode == 13){
            var term = $("#keyword").val();
            var simple_url = "/index/search_result/?stype=1&term=" + term;
            //console.log(simple_url);
            window.location.href = simple_url;
        }
    }).bind('keydown', function(e){
        var ev = document.all?window.event:e;
        if (ev.keyCode == 13){
            return false;
        }
    });
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
        advanced_url += get_base_input_data();
        window.location.href = advanced_url;
    });
}
function get_base_input_data(){
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
    
    var psycho_status_by_emotion_url = '&psycho_status_by_emotion=';
    $("[name='psycho_status_by_emotion']:checked").each(function(){
        if($(this).val()=='未知'){
            $(this).val() = '其他';
        }
        psycho_status_by_emotion_url += $(this).val() + ',';
    });
    temp += psycho_status_by_emotion_url;
    temp = temp.substring(0, temp.length-1);

    var psycho_status_by_word_url = '&psycho_status_by_word=';
    $("[name='psycho_status_by_word']:checked").each(function(){
        if($(this).val()=='未知'){
            $(this).val() = '其他';
        }
        psycho_status_by_word_url += $(this).val() + ',';
    });
    temp += psycho_status_by_word_url;
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

    var tag_url = '&tag=';
    $('#tags').children("span").each(function(){
        var text = $(this).html();
        text = text.split('&')[0];
        tag_url += text +',';
    });
    console.log(tag_url)
    temp += tag_url;
    temp = temp.substring(0, temp.length-1);
    //console.log(temp)
    return temp;
}

function base_call_ajax_request(url, callback){
    $.ajax({
        url:url,
        type:"get",
        dataType: "json",
        async: true,
        success: callback
    })
}

function draw_value_option(data){
    //console.log(data);
    if (data == 'no attribute'){
        data = [];
    }
    $('[name=tag_name]').empty();
    var html = '';
    for (var i=0;i<data.length;i++){
        html += '<option value="' + data[i] + '">' + data[i] + '</option>';
    }
    $('[name=tag_name]').html(html);
}

function getAttributeName(){
    var attribute_name_url = '/tag/show_attribute_name/';
    base_call_ajax_request(attribute_name_url, draw_name_option);
    
    function draw_name_option(data){
        // console.log(data);
        $('[name=tag_type]').empty();
        var html = '';
        for (var i=0;i<data.length;i++){
            html += '<option value="' + data[i] + '">' + data[i] + '</option>';
        }
        $('[name=tag_type]').html(html);

        var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
        attribute_value_url += data[0];
        base_call_ajax_request(attribute_value_url, draw_value_option);

        $('[name=tag_type]').change(function(){
            // console.log($(this).val());
            var attribute_value_url = '/tag/show_attribute_value/?attribute_name=';
            attribute_value_url += $(this).val();
            base_call_ajax_request(attribute_value_url, draw_value_option);
        });
    }

}
function bindAddFunction(){
    var chosen = new Array();
    $('#tag_add').click(function(){
        var type = $('[name=tag_type]').val();
        var name = $('[name=tag_name]').val();
        var check_str = type + ':' + name;
        if (chosen[check_str]){
        }
        else{
            var html = '';
            html += '<span class="mouse" style="margin-right:40px;">'+ check_str;
            html += '&nbsp;<a class="cross" href="#">X</a></span>';
            $('#tags').append(html);
            chosen[check_str] = '1';

            $('.mouse>a').click(function(){
                var text = $(this).parent().html();
                text = text.split('&')[0];
                delete chosen[text];
                $(this).parent().remove();
            });
        }

    });
}


var base = new Base();
bindSearchFunc(base);
getAttributeName();
bindAddFunction();
