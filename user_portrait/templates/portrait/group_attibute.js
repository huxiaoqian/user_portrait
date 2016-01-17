	console.log("bbbbbbbbb");
    $('#group_tag_add').click(function(){
    	console.log('aaaaaaaaaa');
    	var chosen = new Array();
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