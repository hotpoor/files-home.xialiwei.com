root = exports ? this
root.Hs or= {}
Hs = root.Hs

$ ->
    Hs.current_all_device = [1..18]
    $("body").on "click",".device_select_area_btn",(evt)->
        if $(this).hasClass("selected")
            $(this).removeClass("selected")
            $(".device_select_area_btn_item").removeClass("selected")
            Hs.current_all_device=[]
        else
            $(this).addClass("selected")
            $(".device_select_area_btn_item").addClass("selected")
            Hs.current_all_device=[1..18]
    $("body").on "click",".device_select_area_btn_item",(evt)->
        if $(this).hasClass("selected")
            $(this).removeClass("selected")
        else
            $(this).addClass("selected")
        Hs.current_all_device=[]
        for item in $(".device_select_area_btn_item")
            if $(item).hasClass("selected")
                Hs.current_all_device.push parseInt($(item).attr("data-value"))

    for i in [1..18]
        $(".device_select_area").append """
        <button class="device_select_area_btn_item selected" data-value="#{i}">设备 #{i}</button>
        """
    $("body").on "click",".close_enter_door_and_play_video",(evt)->
        console.log "click"
        $.ajax
            url:"http://192.168.200.12:8888/api/door"
            method:"POST"
            dataType:"json"
            data:
                position: "entrance"
                value: "open"
            success:(data)->
                console.log data
            error:(data)->
                console.log data
        $.ajax
            url:"/api/play_video"
            method:"POST"
            dataType:"json"
            data:null
            success:(data)->
                console.log data
            error:(data)->
                console.log data
    $("body").on "click",".open_enter_door_and_close_exit_door",(evt)->
        console.log "click"
        $.ajax
            url:"http://192.168.200.12:8888/api/door"
            method:"POST"
            dataType:"json"
            data:
                position: "entrance"
                value: "close"
            success:(data)->
                console.log data
            error:(data)->
                console.log data
    $("body").on "click",".close_exit_door",(evt)->
        console.log "click"
        $.ajax
            url:"http://192.168.200.12:8888/api/door"
            method:"POST"
            dataType:"json"
            data:
                position: "room"
                value: "open"
            success:(data)->
                console.log data
            error:(data)->
                console.log data
    $("body").on "click",".open_exit_door",(evt)->
        console.log "click"
        $.ajax
            url:"http://192.168.200.12:8888/api/door"
            method:"POST"
            dataType:"json"
            data:
                position: "room"
                value: "close"
            success:(data)->
                console.log data
            error:(data)->
                console.log data


    $("body").on "click",".deivce_action",(evt)->
        device_id = $(this).parents(".device").attr("data-deivce-id")
        action = $(this).attr("data-action")
        tcp_or_udp = $(this).attr("data-tcp-or-udp")
        message = {
            "in_game":action
            "device_id":device_id
        }
        if tcp_or_udp in ["tcp"]
            $.ajax
                url: "/api/tcp_send"
                method: "POST"
                dataType: "json"
                data:
                    "message":JSON.stringify(message)
                    "device_id":device_id
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
        else
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":action
                    "device_id":device_id
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data

    $("body").on "click",".all_ue_start",(evt)->

        for btn in $(".deivce_action[data-tcp-or-udp=tcp][data-action=start]")
            if parseInt($(btn).parents(".device").attr("data-deivce-id")) in Hs.current_all_device
                $(btn).click()

    $("body").on "click",".all_ue_return",(evt)->
        for btn in $(".deivce_action[data-tcp-or-udp=tcp][data-action=return]")
            if parseInt($(btn).parents(".device").attr("data-deivce-id")) in Hs.current_all_device
                $(btn).click()

    $("body").on "click",".all_low",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"down"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_mid",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"center"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_stop",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_stop"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_start",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_start"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_fanlow",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_fanlow"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_fanhigh",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_fanhigh"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_fanstop",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_fanstop"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_turnstart",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_turnstart"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_turnstop",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_turnstop"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_virbon",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_virbon"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
    $("body").on "click",".all_virboff",(evt)->
        for num in Hs.current_all_device
            $.ajax
                url: "/api/udp_send"
                method: "POST"
                dataType: "json"
                data:
                    "action":"all_virboff"
                    "device_id":"#{num}"
                success: (data)->
                    console.log data
                error: (data)->
                    console.log data
