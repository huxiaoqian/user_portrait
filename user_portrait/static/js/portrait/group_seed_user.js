function bind_button_click(){
    $('#seed_user #'+seed_user_option+' #hop_checkbox').click(function(){
        if($(this).is(':checked')){
            $('#seed_user #'+seed_user_option+' [name="hop_choose"]').attr('disabled',false);
        }
        else{
            $('#seed_user #'+seed_user_option+' [name="hop_choose"]').attr('disabled', true);
        }
    });
    $('#seed_user #'+seed_user_option+' #time_checkbox').click(function(){
        if($(this).is(':checked')){
            $('#seed_user #'+seed_user_option+' #events_from').attr('disabled',false);
            $('#seed_user #'+seed_user_option+' #events_to').attr('disabled',false);
        }
        else{
            $('#seed_user #'+seed_user_option+' #events_from').attr('disabled', true);
            $('#seed_user #'+seed_user_option+' #events_to').attr('disabled', true);
        }
    });
    $('#seed_user #'+seed_user_option+' #seed_user_commit').click(function(){
        var valid = seed_user_check();
        if (valid){
            if (seed_user_option == 'single_user'){
                var seed_user_url = seed_single_user_data();
                $.ajax({
                    type:'GET',
                    url:seed_user_url,
                    dataType:'json',
                    success:seed_single_user_callback
                });
            }
            else{
                seed_multi_user_data();
            }
        }
    });
    $('#seed_user #'+seed_user_option+' #attr_weight').change(function(){
        if ((parseFloat($(this).val()) < 0 ) || (parseFloat($(this).val()) > 1)){
            alert('权重应在0-1之间！');
        }
    });
    $('#seed_user #'+seed_user_option+' #stru_weight').change(function(){
        if ((parseFloat($(this).val()) < 0 ) || (parseFloat($(this).val()) > 1)){
            alert('权重应在0-1之间！');
        }
    });
    $('#seed_user #'+seed_user_option+' #influ_from').change(function(){
        if ((parseFloat($(this).val()) < 0 ) || (parseFloat($(this).val()) > 100)){
            alert('影响力应在0-100之间！');
        }
    });
    $('#seed_user #'+seed_user_option+' #influ_to').change(function(){
        if ((parseFloat($(this).val()) < 0 ) || (parseFloat($(this).val()) > 100)){
            alert('影响力应在0-100之间！');
        }
    });
    $('#seed_user #'+seed_user_option+' #impor_from').change(function(){
        if ((parseFloat($(this).val()) < 0 ) || (parseFloat($(this).val()) > 100)){
            alert('重要度应在0-100之间！');
        }
    });
    $('#seed_user #'+seed_user_option+' #impor_to').change(function(){
        if ((parseFloat($(this).val()) < 0 ) || (parseFloat($(this).val()) > 100)){
            alert('重要度应在0-100之间！');
        }
    });
    if (seed_user_option == 'multi_user'){
        $('#seed_user #multi_user_ext #delete_file').click(function(){
            seed_user_files = undefined;
            $('#seed_user #multi_user_ext #file_status').css('display', 'none');
        });
        $('#seed_user #multi_user_ext #uploadbtn').click(function(){
            var fileInput = document.getElementById('seed_file_upload');
            // 检查文件是否选择:
            if (!fileInput.value) {
                alert('没有选择文件');
                return;
            }
            // 获取File引用:
            var file = fileInput.value;
            //alert(file);
            if ((file.endsWith('.csv')) || (file.endsWith('.txt'))) {
                seed_user_files = fileInput.files;
                $('#seed_user #multi_user_ext #add_file').html(file);
                $('#seed_user #multi_user_ext #file_status').css('display', 'block');
                return false;
            }else{
                alert('Can only upload csv or txt file.');
                return;
            }
        });
        $('#seed_user #multi_user_ext [name="ext_choose"]').change(function(){
            var ext_flag = $('#seed_user #multi_user_ext [name="ext_choose"]:checked').val();
            if (ext_flag == 0){
                $('#seed_user #multi_user #attribute').css('display','none');
                $('#seed_user #multi_user #structure').css('display','none');
                $('#seed_user #multi_user #events').css('display','none');
                $('#seed_user #multi_user #extension').css('display','none');
                $('#seed_user #multi_user').css('height','213px');
            }
            else{
                $('#seed_user #multi_user #attribute').css('display','block');
                $('#seed_user #multi_user #structure').css('display','block');
                $('#seed_user #multi_user #events').css('display','block');
                $('#seed_user #multi_user #extension').css('display','block');
                $('#seed_user #multi_user').css('height','450px');
            }
        });
    }
}
function seed_user_init(){
    var html = $('#seed_user #seed_user_ext').html();
    $('#seed_user #'+seed_user_option).html(html);
    //$('#seed_user #events_from').datetimepicker();
    if (global_test_mode == 0){
        $('#seed_user #'+seed_user_option+' #events_from').datetimepicker({value:seed_last_date,step:10});
        $('#seed_user #'+seed_user_option+' #events_to').datetimepicker({value:seed_current_date,step:10});
    }
    else{
        $('#seed_user #'+seed_user_option+' #events_from').datetimepicker({value:seed_last_date,minDate:min_date,maxDate:max_date,step:10});
        $('#seed_user #'+seed_user_option+' #events_to').datetimepicker({value:seed_current_date,minDate:min_date,maxDate:max_date,step:10});
    }
    if (seed_user_option == 'multi_user'){
        $('#seed_user #multi_user #attribute').css('display','none');
        $('#seed_user #multi_user #structure').css('display','none');
        $('#seed_user #multi_user #events').css('display','none');
        $('#seed_user #multi_user #extension').css('display','none');
        $('#seed_user #multi_user').css('height','213px');
    }
    bind_button_click();
}

var seed_user_files = undefined;
var max_date = '+1970/01/01';
var min_date = '-1970/01/30';
var seed_current_date = choose_time_for_mode();
var seed_last_date = new Date();
seed_current_date.setHours(0,0,0);
var current_ts = seed_current_date.getTime();
seed_last_date.setTime(current_ts - 24*60*60*1000);
seed_current_date = seed_current_date.format('yyyy/MM/dd hh:mm');
seed_last_date = seed_last_date.format('yyyy/MM/dd hh:mm');

var seed_user_option = $('#seed_user [name="mode_choose"]:checked').val();
var seed_user_flag = false;
seed_user_init();
$('#seed_user #num-range').change(function(){
    var num = $('#seed_user #'+seed_user_option+' #num-range').val();
    $('#seed_user #show_num').empty();
    $('#seed_user #show_num').append(num);    
})
$('#seed_user [name="mode_choose"]').change(function(){
    seed_user_option = $('#seed_user [name="mode_choose"]:checked').val();
    if (seed_user_option == 'single_user'){
        $('#seed_user #single_user_ext').css('display','block');
        $('#seed_user #multi_user_ext').css('display','none');
    }
    else{
        $('#seed_user #single_user_ext').css('display','none');
        $('#seed_user #multi_user_ext').css('display','block');
    }
    if (!seed_user_flag){
        seed_user_init();
        seed_user_flag = true; // no more html init
    }
});

function seed_user_check(){             // check validation 
    //other form check starts
    if ((seed_user_option == 'multi_user') && ($('#seed_user #multi_user_ext [name="ext_choose"]:checked').val() == 1)){
        if (seed_user_files == undefined){
            alert("请选择文件上传！");
            return false;
        }
    }
    else{              //single_user or multi_user with extension
        if (seed_user_option == 'single_user'){
            if (!($('#seed_user #uid_uname').val())){
                alert('请输入用户ID或昵称！');
                return false;
            }
        }
        else{
            if (seed_user_files == undefined){
                alert("请选择文件上传！");
                return false;
            }
        }
        var attr_weight = parseFloat($('#seed_user #'+seed_user_option+' #attr_weight').val());
        var stru_weight = parseFloat($('#seed_user #'+seed_user_option+' #stru_weight').val());
        if ((attr_weight + stru_weight) != 1){
            alert('属性与结构的权重和应为1！');
            return false;
        }
        var influ_from = parseFloat($('#seed_user #'+seed_user_option+' #influ_from').val());
        var influ_to = parseFloat($('#seed_user #'+seed_user_option+' #influ_to').val());
        if (influ_from > influ_to){
            alert('影响力左侧输入值应小于右侧输入值！');
            return false;
        }
        var impor_from = parseFloat($('#seed_user #'+seed_user_option+' #impor_from').val());
        var impor_to = parseFloat($('#seed_user #'+seed_user_option+' #impor_to').val());
        if (impor_from > impor_to){
            alert('重要度左侧输入值应小于右侧输入值！');
            return false;
        }
        if ($('#seed_user #'+seed_user_option+' #time_checkbox').is(':checked')){
            var events_from = seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_from').val());
            var events_to = seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_to').val());
            if (events_from > events_to){
                alert('时间输入不合法！');
                return false;
            }
            if ((events_from > current_ts) || (events_to > current_ts)){
                alert('选择时间不能超过今日零时！');
            return false;
            }
        }
        if ($('#seed_user #'+seed_user_option+' #num-range').val() == 0){
            alert('人数不能为0！');
            return false;
        }
        if ($('#seed_user #'+seed_user_option+' #hop_checkbox').is(':checked')){
            if ($('#seed_user #'+seed_user_option+' [name="hop_choose"]:checked').val() == undefined){
                alert('请选择跳数！');
                return false;
            }
        }
    }
    //group_information check starts  
    var group_name = $('#seed_user #'+seed_user_option+' #first_name').val();
    var remark = $('#seed_user #'+seed_user_option+' #first_remarks').val();
    if (group_name.length == 0){
        alert('群体名称不能为空');
        return false;
    }

    var reg = "^[a-zA-Z0-9_\u4e00-\u9fa5\uf900-\ufa2d]+$";
    if (!group_name.match(reg)){
        alert('群体名称只能包含英文、汉字、数字和下划线,请重新输入!');
        return false;
    }
    if ((remark.length > 0) && (!remark.match(reg))){
        alert('备注只能包含英文、汉字、数字和下划线,请重新输入!');
        return false;
    }
  return true;
}
function seed_single_user_callback(data){
    if (data == true){
      //redraw_result();
      alert('提交成功！');
      //window.location.reload(); 
    } 
    if (data == 'seed user invalid') alert('人物库中不存在该用户！');
    if (data == 'task name invalid') alert('任务名称已存在！');
    if (data == 'no query condition') alert('请选择搜索条件！');
}
function seed_multi_user_callback(data){
    if (typeof(data) == 'string'){
        if (data == 'no seed user') {
            alert('用户列表为空！');
        }
        else if (data == 'task name invalid') {
            alert('任务名称已存在！');
        }
        else if (data == 'no query condition') {
            alert('请选择搜索条件！');
        }
    }
    else if(typeof(data) == 'object'){
        var out_list = data[1];
        if (out_list.length > 0){
            $('#group_out_list').empty();
            var html = '';
            html += '<table class="table table-bordered table-striped table-condensed datatable"><thead>';
            html += '<tr style="text-align:center;"><th>用户ID</th><th>昵称</th><th>粉丝数</th>';
            html += '<th>好友数</th><th>微博数</th><th>';
            html += '<input id="out_modal_all" type="checkbox" onclick="out_modal_all();"/></th></tr></thead>';
            html += '<tbody>';
            for (i=0;i<out_list.length;i++){
                html += '<tr><td class="center"><a target="_blank" href="http://weibo/com/u/' + out_list[i][0] + '">'+out_list[i][0]+'</a></td>';
                html += '<td class="center">'+out_list[i][1]+'</td>';
                html += '<td class="center">'+out_list[i][2]+'</td>';
                html += '<td class="center">'+out_list[i][4]+'</td>';
                html += '<td class="center">'+out_list[i][3]+'</td>';
                html += '<td><input name="group_recommend_in" type="checkbox" value="' + out_list[i][0] + '" /></td>';
                html += '</tr>';
            }
            html += '</tbody>';
            html += '</table>';
            $('#group_out_list').append(html);
            group_bind_recommend();
            $('#out_list_modal').modal();
        }
        alert('任务提交成功！');
    }
}
function out_modal_all(){
  $('#seed_user input[name="group_recommend_in"]:not(:disabled)').prop('checked', $("#seed_user #out_modal_all").prop('checked'));
}
function group_bind_recommend(){
  $('#seed_user #group_recommend_confirm').click(function(){
      var cur_uids = [];
      $('#seed_user input[name="group_recommend_in"]:checked').each(function(){
        cur_uids.push($(this).attr('value'));
      })
      var recommend_date = new Date().format('yyyy-MM-dd');
      if(cur_uids.length == 0)
        alert("请选择至少一个用户！");
      else{
        var compute_time;
        if($('#seed_user input[name="instant"]:checked').val()==1){
          compute_time = '1';
          var sure = confirm('立即计算会消耗系统较多资源，您确定要立即计算吗？');
          if(sure==true){
              var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + cur_uids.join(',') + '&status=' + compute_time;
              $.ajax({
                    type:'GET',
                    url:recommend_confirm_url,
                    dataType:'json',
                    success:function(){
                        $('#out_list_modal').modal('hide');
                    }
              });
          }
        }
        else{
            compute_time = '2';
            var sure = confirm('您选择了预约计算，系统将在今日24:00自动启动计算！');
            if (sure == true){
                var recommend_confirm_url = '/recommentation/identify_in/?date=' + recommend_date + '&uid_list=' + cur_uids.join(',') + '&status=' + compute_time;
                $.ajax({
                        type:'GET',
                        url:recommend_confirm_url,
                        dataType:'json',
                        success:function(){
                            $('#out_list_modal').modal('hide');
                        }
                });
            }
        }
      }
  });
}
//获取选择的条件，把参数传出获取返回值
function seed_single_user_data(){
    var url = '';
    url += '/detect/single_person/?';
    var uid_uname = $('#seed_user #uid_uname').val();
    url += 'seed_uname=' + uid_uname;
    url += '&seed_uid=' + uid_uname;
    //attribute
    url += '&attribute_weight=' + $('#seed_user #'+seed_user_option+' #attr_weight').val();
    $('#seed_user #'+seed_user_option+' #attribute .inline-checkbox').each(function(){
        if($(this).is(':checked')){
            url += '&' + $(this).next().attr('id') + '=1';
        }
        /* default 0
        else{
            url += '&' + $(this).next().attr('id') + '=0';
        }
        */
    });
    //structure
    url += '&structure_weight=' + $('#seed_user #'+seed_user_option+' #stru_weight').val();
    $('#seed_user #'+seed_user_option+' #structure .inline-checkbox').each(function(){
        if ($(this).attr('id') == 'hop_checkbox'){        //just for hop
            if ($(this).is(':checked')){
                url += '&hop=' + $('#seed_user #'+seed_user_option+' [name="hop_choose"]:checked').val();
            }
        }
        else{
            if($(this).is(':checked')){
                url += '&' + $(this).next().attr('id') + '=1';
            }
            /* default 0
            else{
                url += '&' + $(this).next().attr('id') + '=0';
            }
            */
        }
    });
    //events
    url += '&text=' + $('#seed_user #'+seed_user_option+' #events_keywords').val();
    if ($('#seed_user #'+seed_user_option+' #time_checkbox').is(':checked')){
        url += '&timestamp_from=' + seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_from').val());
        url += '&timestamp_to=' + seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_to').val());
    }
    //extension
    url += '&count=' + $('#seed_user #'+seed_user_option+' #num-range').val();
    url += '&influence_from=' + $('#seed_user #'+seed_user_option+' #influ_from').val();
    url += '&influence_to=' + $('#seed_user #'+seed_user_option+' #influ_to').val();
    url += '&importance_from=' + $('#seed_user #'+seed_user_option+' #impor_from').val();
    url += '&importance_to=' + $('#seed_user #'+seed_user_option+' #impor_to').val();
    // group_task
    url += '&task_name=' + $('#seed_user #'+seed_user_option+' #first_name').val();
    url += '&state=' + $('#seed_user #'+seed_user_option+' #first_remarks').val();
    url += '&submit_user=admin';
    return url;
}
function seed_multi_user_data(){
    var url = '/detect/multi_person/';
    var upload_job = {};
    // group_task
    upload_job['task_name'] = $('#seed_user #'+seed_user_option+' #first_name').val();
    upload_job['state']  = $('#seed_user #'+seed_user_option+' #first_remarks').val();
    upload_job['submit_user'] = 'admin';
    if ($('#seed_user #multi_user_ext [name="ext_choose"]:checked').val() == 0){
        upload_job['extend'] = '0';
    }
    else{
        upload_job['extend'] = '1';
        //attribute
        upload_job['attribute_weight'] = $('#seed_user #'+seed_user_option+' #attr_weight').val();
        $('#seed_user #'+seed_user_option+' #attribute .inline-checkbox').each(function(){
            var attr_id = $(this).next().attr('id');
            if($(this).is(':checked')){
                upload_job[attr_id] = '1';
            }
            else{
                upload_job[attr_id] = '0';
            }
        });
        //structure
        upload_job['structure_weight'] = $('#seed_user #'+seed_user_option+' #stru_weight').val();
        $('#seed_user #'+seed_user_option+' #structure .inline-checkbox').each(function(){
            if ($(this).attr('id') == 'hop_checkbox'){        //just for hop
                if ($(this).is(':checked')){
                    upload_job['hop'] = $('#seed_user #'+seed_user_option+' [name="hop_choose"]:checked').val();
                }
                else{
                    upload_job['hop'] = 1;
                }
            }
            else{
                var attr_id = $(this).next().attr('id');
                if($(this).is(':checked')){
                    upload_job[attr_id] = '1';
                }
                else{
                    upload_job[attr_id] = '0';
                }
            }
        });
        //events
        upload_job['text'] = $('#seed_user #'+seed_user_option+' #events_keywords').val();
        if ($('#seed_user #'+seed_user_option+' #time_checkbox').is(':checked')){
            upload_job['timestamp_from'] = seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_from').val());
            upload_job['timestamp_to'] = seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_to').val());
        }
        //extension
        upload_job['count'] = $('#seed_user #'+seed_user_option+' #num-range').val();
        upload_job['influence_from'] = $('#seed_user #'+seed_user_option+' #influ_from').val();
        upload_job['influence_to'] =  $('#seed_user #'+seed_user_option+' #influ_to').val();
        upload_job['importance_from'] = $('#seed_user #'+seed_user_option+' #impor_from').val();
        upload_job['importance_to'] = $('#seed_user #'+seed_user_option+' #impor_to').val();
    }
    // var test_data = [true, [['00000', '未知','未知','未知','未知']]];
    handleFileSelect(upload_job);
}
function seed_user_timepicker(str){
    var date_time = str.split(' ');
    var dates = date_time[0].split('/');
    var yy = parseInt(dates[0]);
    var mm = parseInt(dates[1]) - 1;
    var dd = parseInt(dates[2]);
    var times = date_time[1].split(':');
    var hh = parseInt(times[0]);
    var minute = parseInt(times[1]);
    var final_date = new Date();
    final_date.setFullYear(yy,mm,dd);
    final_date.setHours(hh,minute);
    final_date = Math.floor(final_date.getTime()/1000);
    return final_date;
}

function handleFileSelect(upload_job){
    var files = seed_user_files;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            upload_job['upload_data'] = a;
            //console.log(upload_job);
            $.ajax({   
                type:"POST",  
                url:"/detect/multi_person/",
                contentType:"application/json",
                data:JSON.stringify(upload_job),
                dataType: "json",
                success: seed_multi_user_callback
            });
        };            
        reader.readAsText(f,'GB2312');                                                        
    }
}

