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
    // console.log(data);
    $('#table').empty();
    var user_url ='';
    html = '';
    html += '<table class="table table-striped table-bordered bootstrap-datatable datatype responsive">';
    html += '<thead><tr><th class="center" style="text-align:center">头像</th><th class="center" style="text-align:center">昵称</th><th class="center" style="text-align:center">注册地</th><th class="center" style="text-align:center">关注数</th><th class="center" style="text-align:center">粉丝数</th><th class="center" style="text-align:center">微博数</th></tr></thead>';
    var item = data['hits']['hits'];
    html += '<tbody>';
    for(var i = 0; i < item.length; i++){
      if (item[i]['_source']['sex']=='1'){
        item[i]['_source']['sex']= '/static/img/male.png';
      }
      else{
        item[i]['_source']['sex']= '/static/img/female.png';
      }
      user_host = window.location.host;
      user_url = "http://" + user_host + "/profile/" + item[i]['_id'];
      html += '<tr>';
      html += '<td class="center" style="text-align:center;vertical-align:middle"><a href='+ user_url+ '><img src="' + item[i]['_source']['photo_url'] + '"class="img-circle"></td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i]['_source']['nick_name'] +'<img src="'+ item[i]['_source']['sex'] +'"style="height:20px"><img src="/static/img/vertify.png" style="height:20px"</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i]['_source']['user_location'] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i]['_source']['friendsnum'] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i]['_source']['fansnum'] +'</td>';
      html += '<td class="center" style="text-align:center;vertical-align:middle">'+ item[i]['_source']['statusnum'] +'</td>';
      // html += '<td class="center" style="text-align:center">'+ new Date(parseInt(item[i]['_source']['create_at']) +'</td>';
      html += '</tr>';
    }
    $('#table').append(html);
    html += '</tbody>';
    html += '</table>';
    draw_information(data);
  }
}
 function draw_information(data){
  $('#search_information').empty();
  html = ''
  took = data['took'];
  term = data['hits']['total'];
  html += '<div class="page-header" style="margin-top:65px">用户信息列表(耗时：' + took + 'ms' + '命中：' + term + '个)</div><a style="cursor:pointer" role="button" id = "download">全部导出</a>';
  $('#search_information').append(html);
}

function get_input_data(){
  var temp = '';
  var input_value;
  var input_index;
  $('.form-control').each(function(){
    input_value = $(this).val() +'&';
    input_index = $(this).attr('name')+ '=';
    temp += input_index;
    temp += input_value;
  });
  return temp;
}

function toggle(target){
       targetid = target.substr(7, target.length);
       $("#" + targetid).val();
       if (document.getElementById){
           target_search=document.getElementById(target);
               if (target_search.style.display=="block"){
                   target_search.style.display="none";
                   click_data();
               } else {
                   if (targetid == 'isreal'){
                      $("#" + targetid).find("option[value='2']").attr("selected",true);
                   }else if (targetid == 'sex'){
                      $("#" + targetid).find("option[value='3']").attr("selected",true);
                   }else if (targetid == 'select_source'){
                      $("#" + targetid).find("option[value='0']").attr("selected",true);
                   }else if (targetid == 'weibo'){
                      $("#weibo_from").val("");
                      $("#weibo_to").val("");
                   }else if (targetid == 'fans'){
                      $("#fans_from").val("");
                      $("#fans_to").val("");
                   }else if (targetid == 'friends'){
                      $("#friends_from").val("");
                      $("#friends_to").val("");
                   }
                   else {
                      $("#" + targetid).val("");
                   }
                   target_search.style.display="none";                    
                   click_data();
               }
       }
  }
  function search_conditions(){
      $('#search_conditions').empty();
      html = '<div>'
      html += '<span style="float:left">搜索条件：</span>';
      uid = $("#uid").val();
      if (uid == ''){
        html += '';
      }
      else{
        html += '<span class="mouse" style="float:left;margin-bottom:10px"id="search_uid">' + 'UID：' + uid + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_uid") class="cross">X</a></span>';
      }

      nick_name = $("#nick_name").val();

      if (nick_name == ''){
        html += '';
      }
      else{
        html += '<span class="mouse" style="float:left;margin-left:10px;margin-bottom:10px"id="search_nick_name">' + '昵称：' + nick_name + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_nick_name") class="cross">X</a></span>';
      }

      sex = $("#sex").val();
      if (sex == '3'){
        sex = '不限';
      }else if(sex == '0'){
        sex = '未填写';
      }else if(sex == '1'){
        sex = '男';
      }
      else{sex = '女';
      }
      if (sex == '不限'){
        html += '';
      }
      else{
        html += '<span class="mouse" style="float:left;margin-left:10px;margin-bottom:10px"id="search_sex">' + '性别：' + sex + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_sex") class="cross">X</a></span>';
      }

      isreal = $("#isreal").val();
      if (isreal == '2'){
        isreal = '不限';
      }else if(isreal == '0'){
        isreal = '未认证';
      }
      else{isreal = '已认证';
      }
      if (isreal == '不限'){
        html += '';
      }
      else{
        html += '<span class="mouse"style="float:left;margin-left:10px;margin-bottom:10px" id="search_isreal">' + '是否认证：' + isreal + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_isreal") class="cross">X</a></span>'; 
      }

      select_email = $("#select_email").val();
      if (select_email == '0'){
        select_email = '@163.com';
      }else if(select_email == '1'){
        select_email = '@qq.com';
      }else if(select_email == '2'){
        select_email = '@sina.com';
      }else if(select_email == '3'){
        select_email = '@126.com';
      }else{
        select_email = '@sohu.com';
      }

      user_email = $("#user_email").val();
      if (user_email == ''){
        html += '';
      }
      else{
        html += '<span class="mouse" style="float:left;;margin-left:10px;margin-bottom:10px"id="search_user_email">' + '邮箱：' + user_email + select_email + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_user_email") class="cross">X</a></span>';
      }

      user_birth = $("#demo").val();
      if (user_birth == ''){
        html += '';
      }
      else{
        html += '<span class="mouse" style="float:left;margin-left:10px;margin-bottom:10px" id="search_demo">' + '出生年月日：' + user_birth + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_demo") class="cross">X</a></span>';
      }

      select_source = $("#select_source").val();
      if (select_source == '0'){
        select_source = '不限';
      }if(select_source == '1'){
        select_source = '新浪微博';
      }if(select_source == '2'){
        select_source = '腾讯微博';
      }if(select_source == '3'){
        select_source = '搜狐微博';
      }if(select_source == '4'){
        select_source = '网易微博';
      }

      if (select_source == '不限'){
        html += '';
      }
      else{
        html += '<span class="mouse" style="float:left;margin-left:10px;margin-bottom:10px"id="search_source">' + '来源：' + select_source + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_source") class="cross">X</a></span>';
      }

      rel_name = $("#rel_name").val();
      if (rel_name == ''){
        html += '';
      }
      else{
        html += '<span class="mouse"  style="float:left;margin-left:10px;margin-bottom:10px" id="search_rel_name">' + '真实姓名：' + rel_name + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_rel_name") class="cross">X</a></span>';
      }
      datafrom = [];
      datato = [];
      datafrom['weibo_from'] = $("#weibo_from").val();
      datato['weibo_to'] = $("#weibo_to").val();
      datafrom['fans_from'] = $("#fans_from").val();
      datato['fans_to'] = $("#fans_to").val();
      datafrom['friends_from'] = $("#friends_from").val();
      datato['friends_to'] = $("#friends_to").val();
      for (key in datafrom) {
        if (datafrom[key] == ''){
           datafrom[key] = '0'; 
        }
      };
      for (key in datato) {
        if (datato[key] == ''){
           datato[key] = '100000000'; 
        }
      };
      if (datafrom['weibo_from'] == '0'  &&  datato['weibo_to'] == '100000000'){
        html += '';
      }else{
        html += '<span class="mouse"  style="float:left;margin-left:10px;margin-bottom:10px" id="search_weibo">' + '微博数：' + datafrom['weibo_from'] + '-' + datato['weibo_to'] + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_weibo") class="cross">X</a></span>';
      }
      if (datafrom['fans_from'] == '0'  &&  datato['fans_to'] == '100000000'){
        html += '';
      }else{
      html += '<span class="mouse"  style="float:left;margin-left:10px;margin-bottom:10px" id="search_fans">' + '粉丝数：' + datafrom['fans_from'] + '-' + datato['fans_to'] + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_fans") class="cross">X</a></span>';
      }
      if (datafrom['friends_from'] == '0'  &&  datato['friends_to'] == '100000000'){
        html += '';
      }else{
      html += '<span class="mouse"  style="float:left;margin-left:10px;margin-bottom:10px" id="search_friends">' + '好友数：' + datafrom['friends_from'] + '-' + datato['friends_to'] + '&nbsp;&nbsp;' + '<a title="Close" href="#" onclick=toggle("search_friends") class="cross">X</a></span>';
      }
 


      html += '</div>';
     $('#search_conditions').append(html);
  }

var Search_weibo = new Search_weibo(); 

function click_data(){
  weibo_url = '/profile/user/?';
  weibo_url += get_input_data();
  weibo_url = weibo_url.substring(0,weibo_url.length-1);
  Search_weibo.call_sync_ajax_request(weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_table);
  $('#download').click(function(){
        console.log('download');
        var download_url = 'http://'+ window.location.host + '/static/download/test.csv';
        window.location.href = download_url;
  });
       $('.datatype').dataTable({
        "sDom": "<'row'<'col-md-6'l><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "bSort": true, 
        "oLanguage": {
            "sLengthMenu": "_MENU_ 每页"
        }
    });
        $('.btn-close').click(function (e) {
        e.preventDefault();
        $(this).parent().parent().parent().fadeOut();
    });
    $('.btn-minimize').click(function (e) {
        e.preventDefault();
        var $target = $(this).parent().parent().next('.box-content');
        if ($target.is(':visible')) $('i', $(this)).removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        else                       $('i', $(this)).removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        $target.slideToggle();
    });
    $('.btn-setting').click(function (e) {
        e.preventDefault();
        $('#myModal').modal('show');
    });


    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        defaultDate: '2014-06-12',
        events: [
            {
                title: 'All Day Event',
                start: '2014-06-01'
            },
            {
                title: 'Long Event',
                start: '2014-06-07',
                end: '2014-06-10'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2014-06-09T16:00:00'
            },
            {
                id: 999,
                title: 'Repeating Event',
                start: '2014-06-16T16:00:00'
            },
            {
                title: 'Meeting',
                start: '2014-06-12T10:30:00',
                end: '2014-06-12T12:30:00'
            },
            {
                title: 'Lunch',
                start: '2014-06-12T12:00:00'
            },
            {
                title: 'Birthday Party',
                start: '2014-06-13T07:00:00'
            },
            {
                title: 'Click for Google',
                url: 'http://google.com/',
                start: '2014-06-28'
            }
        ]
    });

}

$.fn.dataTableExt.oApi.fnPagingInfo = function (oSettings) {
    return {
        "iStart": oSettings._iDisplayStart,
        "iEnd": oSettings.fnDisplayEnd(),
        "iLength": oSettings._iDisplayLength,
        "iTotal": oSettings.fnRecordsTotal(),
        "iFilteredTotal": oSettings.fnRecordsDisplay(),
        "iPage": Math.ceil(oSettings._iDisplayStart / oSettings._iDisplayLength),
        "iTotalPages": Math.ceil(oSettings.fnRecordsDisplay() / oSettings._iDisplayLength)
    };
}
$.extend($.fn.dataTableExt.oPagination, {
    "bootstrap": {
        "fnInit": function (oSettings, nPaging, fnDraw) {
            var oLang = oSettings.oLanguage.oPaginate;
            var fnClickHandler = function (e) {
                e.preventDefault();
                if (oSettings.oApi._fnPageChange(oSettings, e.data.action)) {
                    fnDraw(oSettings);
                }
                $('input[type=checkbox]').prop('checked', $(check_first).prop('checked'));
            };

            $(nPaging).addClass('pagination').append(
                '<ul class="pagination">' +
                    '<li class="prev disabled"><a href="#">&larr; ' + oLang.sPrevious + '</a></li>' +
                    '<li class="next disabled"><a href="#">' + oLang.sNext + ' &rarr; </a></li>' +
                    '</ul>'
            );
            var els = $('a', nPaging);
            $(els[0]).bind('click.DT', { action: "previous" }, fnClickHandler);
            $(els[1]).bind('click.DT', { action: "next" }, fnClickHandler);
        },

        "fnUpdate": function (oSettings, fnDraw) {
            var iListLength = 5;
            var oPaging = oSettings.oInstance.fnPagingInfo();
            var an = oSettings.aanFeatures.p;
            var i, j, sClass, iStart, iEnd, iHalf = Math.floor(iListLength / 2);

            if (oPaging.iTotalPages < iListLength) {
                iStart = 1;
                iEnd = oPaging.iTotalPages;
            }
            else if (oPaging.iPage <= iHalf) {
                iStart = 1;
                iEnd = iListLength;
            } else if (oPaging.iPage >= (oPaging.iTotalPages - iHalf)) {
                iStart = oPaging.iTotalPages - iListLength + 1;
                iEnd = oPaging.iTotalPages;
            } else {
                iStart = oPaging.iPage - iHalf + 1;
                iEnd = iStart + iListLength - 1;
            }

            for (i = 0, iLen = an.length; i < iLen; i++) {
                // remove the middle elements
                $('li:gt(0)', an[i]).filter(':not(:last)').remove();

                // add the new list items and their event handlers
                for (j = iStart; j <= iEnd; j++) {
                    sClass = (j == oPaging.iPage + 1) ? 'class="active"' : '';
                    $('<li ' + sClass + '><a href="#">' + j + '</a></li>')
                        .insertBefore($('li:last', an[i])[0])
                        .bind('click', function (e) {
                            e.preventDefault();
                            oSettings._iDisplayStart = (parseInt($('a', this).text(), 10) - 1) * oPaging.iLength;
                            fnDraw(oSettings);
                            $('input[type=checkbox]').prop('checked', $(check_first).prop('checked'));
                        });
                }

                // add / remove disabled classes from the static elements
                if (oPaging.iPage === 0) {
                    $('li:first', an[i]).addClass('disabled');
                } else {
                    $('li:first', an[i]).removeClass('disabled');
                }

                if (oPaging.iPage === oPaging.iTotalPages - 1 || oPaging.iTotalPages === 0) {
                    $('li:last', an[i]).addClass('disabled');
                } else {
                    $('li:last', an[i]).removeClass('disabled');
                }
            }
        }
    }
});
  // function selectAll(checkbox,file) {
  //     var checkbox_first = $('input[type=checkbox]').eq(0);
  //     $('input[type=checkbox]').prop('checked', $(checkbox_first).prop('checked'));
  //     var ids = '';
  //     $('input[type=checkbox]').each(function(){
  //       var select_id = $(this).attr('id');
  //       if(select_id){
  //         select_id = select_id + ',';
  //         ids += select_id;
  //       }
  //     });
  //     console.log(ids);
  //     $.ajax({
  //       url: '/profile/download/?id='+ids,
  //       type: "GET",
  //       dataType: "json",
  //       async: false,
  //       success: function(data){
  //         console.log(data);
  //          // window.location.href = file;
  //       }
  //   });
  // }


   function selectAll(file) {
      // $('input[type=checkbox]').prop('checked', $(checkbox).prop('checked'));
      // var obj = $('input[type=checkbox]').eq(0);
      // var q = 1;
      // var ids = '';
      // if (obj.is(":checked")){
      //   var q = obj.attr('name');
      // }
      // if(q==0){
      console.log(file);
      window.location.href = file
      // }
      // else{
      //     $('input[type=checkbox]').each(function(){
      //       var select_id = $(this).attr('id');
      //       if(select_id){
      //         select_id = select_id + ',';
      //         ids += select_id;
      //       }
      //     });
      //     console.log(ids);
      //     $.ajax({
      //       url: 'http://219.224.135.93:9045/profile/download/?q='+q+'&id='+ids,
      //       type: "GET",
      //       dataType: "json",
      //       async: false,
      //       success: function(data){
      //         console.log(data);
      //          window.location.href = file;
      //       }
      //   });
      // }
  }