/**
 * Created by zhengxupeng on 16-5-4.
 */
$(function(){

    $("#acl_add").click(function(){
        var max_id = $("td[name='acl_id']").last().attr('id');
        var add_id = parseInt(max_id,10)+1;

        $("#tab").find("tr:last").before("<tr><td name='acl_id' id='"+add_id+"'>"+add_id+"</td><td><input type='text' name='acl_new_acl_name_"+add_id+"' class='acl_acl_name' required=’required‘></td><td><select name='acl_new_mode_"+add_id+"' id='modeSelect' data-placeholder='选择一种'><option value='hdr(host)' selected>hdr(host)</option><option value='hdr_reg(host)'>hdr_reg(host)</option><option value='hdr_beg(RequestType)'>hdr_beg(RequestType)</option><option value='hdr(RequestType)' selected>hdr(RequestType)</option><option value='path_beg'>path_beg</option><option value='path_end'>path_end</option></select></td><td><input type='text' name='acl_new_defined_"+add_id+"' required=’required‘></td><td><input type='button' value='删除' name='acl_delete' class='acl_delete'/></td></tr>")

    });
    $(".tab").on("click","input[class='acl_delete']",function(){
        var del_id = $(this).parents("tr").children("td:first").attr('id');
        $(this).parents("tr").remove();
        //$("input[class='acl_acl_name']").each(function(){
        //    var big_than_del = $(this).parents("tr").children("td:first");
        //    var big_id_than_del = big_than_del.attr('id');
        //    alert(del_id)
        //    if (big_id_than_del > del_id){
        //        big_than_del.attr('id',del_id);
        //        big_than_del.html(del_id);
        //        del_id = big_id_than_del;
        //    };
        //});
    });


    $("#action_add").click(function(){
        var max_id = $("td[name='action_id']").last().attr('id');
        var add_id = parseInt(max_id,10)+1

        $("#tab2").find("tr:last").before("<tr><td name='action_id' id='"+add_id+"'>"+add_id+"</td><td><input type='text' name='action_new_backend_server_"+add_id+"' class='action_backend_name' required=’required‘></td><td><input type='text' name='action_new_acl_name_"+add_id+"' required=’required‘></td><td><input type='button' value='删除' name='action_delete' class='action_delete'/></td></tr>")

    });
    $(".tab2").on("click","input[class='action_delete']",function(){
        //$(this).parents("tr").remove();
        var del_id = $(this).parents("tr").children("td:first").attr('id');
        $(this).parents("tr").remove();
        //$("input[name='action_new_backend_server']").each(function(){
        //    var big_than_del = $(this).parents("tr").children("td:first");
        //    var big_id_than_del = big_than_del.attr('id');
        //    if (big_id_than_del > del_id){
        //        big_than_del.attr('id',del_id);
        //        big_than_del.html(del_id);
        //        del_id = big_id_than_del;
        //    }
        //});
    });


    $("#backend_add").click(function(){
        var max_id = $("td[name='backend_id']").last().attr('id');
        var add_id = parseInt(max_id,10)+1

    $("#tab3").find("tr:last").before("<tr><td name='backend_id' id='"+add_id+"'>"+add_id+"</td><td><input type='text' name='backend_new_backend_name_"+add_id+"' class='backend_backend_name' required=’required‘></td><td><input type='text' name='backend_new_server0_name_"+add_id+"' required=’required‘></td><td><input type='text' name='backend_new_server0_address_"+add_id+"' required='required' pattern='^\\d{2,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}:\\d{2,5}$' placeholder='IP:端口'></td><td><input type='button' value='删除' name='backend_delete' class='backend_delete'/></td></tr>")

    });
    $(".tab3").on("click","input[class='backend_delete']",function(){
        //$(this).parents("tr").remove();
        var del_id = $(this).parents("tr").children("td:first").attr('id');
        $(this).parents("tr").remove();
        //$("input[name='backend_new_backend_server']").each(function(){
        //    var big_than_del = $(this).parents("tr").children("td:first");
        //    var big_id_than_del = big_than_del.attr('id');
        //    if (big_id_than_del > del_id){
        //        big_than_del.attr('id',del_id);
        //        big_than_del.html(del_id);
        //        del_id = big_id_than_del;
        //    }
        //});
    });



    $("#check_submit").click(function(){
        var check_acl_name = new Array();
        var check_backend_name = new Array();
        var checking = true;

        $(".acl_acl_name").each(function(){
            var i = $(this).val();
            if (check_acl_name[i] == 1){
                alert('ACL重复值:'+i);
                checking = false;
            };
            check_acl_name[i] = 1;
        });

        $(".backend_backend_name").each(function(){
            var i = $(this).val();
            if (check_backend_name[i] == 1){
                alert('BACKEND重复值:'+i);
                checking = false;
            };
            check_backend_name[i] = 1;
        });


        if (checking == true){var form = document.getElementById("data_post");
            form.submit();}else{
            $(document).ready(function(){
                $("form").submit(function(e){
                return false;
                });
            });
        };
    });

})
