 function Search_weibo(){
  this.ajax_method = 'GET';
}

Search_weibo.prototype = {
  call_sync_ajax_request:function(url, method, callback){
    // console.log(url);
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
    html += '<div style="float:right"><a  role="button" id = "download">全部导出</a></div>';
    html += '<thead><tr><th>uid</th><th>昵称</th><th>性别</th><th>注册地</th><th>关注数</th><th>粉丝数</th><th>微博数</th></tr></thead>';
    var item = data['hits']['hits'];
    html += '<tbody>';
    for(var i = 0; i < item.length; i++){
      if (item[i]['_source']['sex']=='1'){
        item[i]['_source']['sex']= '男';
      }
      else{
        item[i]['_source']['sex']= '女';
      }
      user_host = window.location.host;
      user_url = "http://" + user_host + "/profile/" + item[i]['_id'];
      html += '<tr>';
      html += '<td class="center"><a href='+ user_url+ '>'+ item[i]['_id'] +'</td>';
      html += '<td class="center">'+ item[i]['_source']['nick_name'] +'</td>';
      html += '<td class="center">'+ item[i]['_source']['sex'] +'</td>';
      html += '<td class="center">'+ item[i]['_source']['user_location'] +'</td>';
      html += '<td class="center">'+ item[i]['_source']['friendsnum'] +'</td>';
      html += '<td class="center">'+ item[i]['_source']['fansnum'] +'</td>';
      html += '<td class="center">'+ item[i]['_source']['statusnum'] +'</td>';
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
  html += '<div style="float:left;width:50%"class="list-group-item list-group-item-success">耗时：' + took + 'ms</div>';
  html += '<div style="float:right;width:50%"class="list-group-item list-group-item-success">命中：' + term +　'个</div>';
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

var Search_weibo = new Search_weibo(); 

function click_data(){
  weibo_url = '/profile/user/?';
  weibo_url += get_input_data();
  weibo_url = weibo_url.substring(0,weibo_url.length-1);
  console.log(weibo_url);
  Search_weibo.call_sync_ajax_request(weibo_url, Search_weibo.ajax_method, Search_weibo.Draw_table);
  $('#download').click(function(){
        console.log('download');
        var download_url = 'http://'+ window.location.host + '/static/download/test.csv';
        window.location.href = download_url;
  });
       $('.datatype').dataTable({
        "sDom": "<'row'<'col-md-6'l><'col-md-6'f>r>t<'row'<'col-md-12'i><'col-md-12 center-block'p>>",
        "sPaginationType": "bootstrap",
        "bSort": false, 
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