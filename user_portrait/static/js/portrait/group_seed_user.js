Date.prototype.format = function(format) {
    var o = {
        "M+" : this.getMonth()+1, //month
        "d+" : this.getDate(), //day
        "h+" : this.getHours(), //hour
        "m+" : this.getMinutes(), //minute
        "s+" : this.getSeconds(), //second
        "q+" : Math.floor((this.getMonth()+3)/3), //quarter
        "S" : this.getMilliseconds() //millisecond
    }
    if(/(y+)/.test(format)){
        format=format.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
    }
    for(var k in o){
        if(new RegExp("("+ k +")").test(format)){
            format = format.replace(RegExp.$1, RegExp.$1.length==1 ? o[k] : ("00"+ o[k]).substr((""+ o[k]).length));
        }
    }
    return format;
}
function bind_button_click(){
    $('#seed_user #'+seed_user_option+' #hop_checkbox').click(function(){
        if($(this).is(':checked')){
            $('#seed_user #'+seed_user_option+' [name="hop_choose"]').attr('disabled',false);
        }
        else{
            $('#seed_user #'+seed_user_option+' [name="hop_choose"]').attr('disabled', true);
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
            console.log(fileInput.value);
            if (!fileInput.value) {
                alert('没有选择文件');
                return;
            }
            // 获取File引用:
            var file = fileInput.value;
            //alert(file);
            if ((file.endsWith('.csv')) || (file.endsWith('.txt'))) {
                console.log('success');
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
            if (ext_flag == 1){
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
                $('#seed_user #multi_user').css('height','440px');
            }
        });
    }
}
function seed_user_init(){
    if (!seed_user_flag){
        var html = $('#seed_user #seed_user_ext').html();
        $('#seed_user #'+seed_user_option).html(html);
        //$('#seed_user #events_from').datetimepicker();
        console.log(seed_user_option);
        $('#seed_user #'+seed_user_option+' #events_from').datetimepicker({value:current_date,minDate:min_date,maxDate:max_date,step:10});
        $('#seed_user #'+seed_user_option+' #events_to').datetimepicker({value:current_date,minDate:min_date,maxDate:max_date,step:10});
        if (seed_user_option == 'multi_user'){
            $('#seed_user #multi_user #attribute').css('display','none');
            $('#seed_user #multi_user #structure').css('display','none');
            $('#seed_user #multi_user #events').css('display','none');
            $('#seed_user #multi_user #extension').css('display','none');
            $('#seed_user #multi_user').css('height','213px');
        }
        bind_button_click();
    }    
}

var seed_user_files = undefined;
var max_date = '+1970/01/01';
var min_date = '-1970/01/30';
var current_date = new Date().format('yyyy/MM/dd hh:mm');
console.log(current_date);
console.log(min_date);

var seed_user_option = $('#seed_user [name="mode_choose"]:checked').val();
var seed_user_flag = false;
seed_user_init();
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
    seed_user_init();
    if (!seed_user_flag) seed_user_flag = true; // no more html init
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
            console.log($('#seed_user #uid_uname').val());
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
        var events_from = seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_from').val());
        var events_to = seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_to').val());
        if (events_from > events_to){
            alert('时间输入不合法！');
            return false;
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
    console.log(group_name, remark);
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
    console.log(data);
    if (data == 'seed user invalid') alert('人物库中不存在该用户！');
    if (data == 'task name invalid') alert('请输入合法的任务名称！');
    if (data == 'no query condition') alert('请选择搜索条件！');
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
    url += '&timestamp_from=' + seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_from').val());
    url += '&timestamp_to=' + seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_to').val());
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
    console.log(url);
    return url;
}
function seed_multi_user_data(){
    var url = '/detect/multi_person/';
    var upload_job = new Array();
    handleFileSelect(upload_job);
    /*
    //attribute
    url += '&attribute_weight=' + $('#seed_user #'+seed_user_option+' #attr_weight').val();
    $('#seed_user #'+seed_user_option+' #attribute .inline-checkbox').each(function(){
        if($(this).is(':checked')){
            url += '&' + $(this).next().attr('id') + '=1';
        }
        else{
            url += '&' + $(this).next().attr('id') + '=0';
        }
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
            else{
                url += '&' + $(this).next().attr('id') + '=0';
            }
        }
    });
    //events
    url += '&text=' + $('#seed_user #'+seed_user_option+' #events_keywords').val();
    url += '&timestamp_from=' + seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_from').val());
    url += '&timestamp_to=' + seed_user_timepicker($('#seed_user #'+seed_user_option+' #events_to').val());
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
    console.log(url);
    */
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
    console.log(final_date);
    return final_date;
}

function handleFileSelect(upload_job){
    var files = seed_user_files;
    for(var i=0,f;f=files[i];i++){
        var reader = new FileReader();
        reader.onload = function (oFREvent) {
            var a = oFREvent.target.result;
            console.log(a);
            upload_job['upload_data'] = a;
            console.log(upload_job);
            /*
            $.ajax({   
                type:"POST",  
                url:"/group/upload_file/",
                dataType: "json",
                data:JSON.stringify(job),
                success: function(){
                            var show_url = "/group/show_task/";
                }
            });
            */
        };            
        reader.readAsText(f,'GB2312');                                                        
    }
}

