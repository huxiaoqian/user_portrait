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
