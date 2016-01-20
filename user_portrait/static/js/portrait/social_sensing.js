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
$(' [name="so_mode_choose"]').change(function(){
    seed_user_option = $('[name="so_mode_choose"]:checked').val();
    if (seed_user_option == 'so_all_users'){
        $('#single_user_ext').css('display','block');
        $('#multi_user_ext').css('display','none');
    }
    else{
        $('#single_user_ext').css('display','none');
        $('#multi_user_ext').css('display','block');
    }
    seed_user_init();
    if (!seed_user_flag) seed_user_flag = true; // no more html init
});
var current_date = new Date().format('yyyy/MM/dd hh:mm');
var max_date = '+1970/01/01';
var min_date = '-1970/01/30';
$('#so_end_time').datetimepicker({value:current_date,minDate:min_date,maxDate:max_date,step:10});