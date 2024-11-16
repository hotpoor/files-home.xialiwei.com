root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs
Hs.DEVICE_USER = null
hotpoor_ws = null
hotpoor_timestamp = null
hotpoor_ws_device = null
WS_DEVICE =
    UNKNOWN  : 0
    READY    : 1
    OPEN     : 2
    POST     : 3
    BAD      : 4
root.video_play = ()->
    $("video")[0].currentTime = 0
    $("video")[0].play()
root.join_info = (content_json,m_aim)->
    console.log "content_json",content_json
    console.log "m_aim",m_aim
$ ->
    if BLOCK_ID?
        hotpoor_ws_device = WS_DEVICE.UNKNOWN
        hotpoor_ws_device_open = false
        hotpoor_ws_timer = null

        heartCheck = (num=0)->
            message = JSON.stringify ["PING",num]
            console.log "hotpoor_ws_device",hotpoor_ws_device,hotpoor_ws
            if hotpoor_ws_device == WS_DEVICE.OPEN
                setTimeout ()->
                        hotpoor_ws.send message
                    ,10000
            else
                setTimeout ()->
                        heartCheck(num)
                    ,1000 
        restart_ws_connection = () ->
            console.log "restart_ws_connection"
            on_message = (params) ->
                # console.log params
                m_type = params[0]
                content_json = params[1]
                m_plus = ""
                m_aim = params[2]
                if m_type == "PONG"
                    num = content_json + 1
                    heartCheck(num)
                else if m_type in ["JOIN","LEAVE"]
                    join_info(content_json,m_aim)
                else if m_type == "VIDEO_PLAY"
                    root.video_play()

                # Hs.video_list.push video_uri
                # console.log Hs.video_list

            if "WebSocket" of window and hotpoor_ws_device == WS_DEVICE.UNKNOWN
                hotpoor_ws.close() if hotpoor_ws?
                hotpoor_ws = new WebSocket WEBSOCKET_URL
                hotpoor_ws_device = WS_DEVICE.READY
                hotpoor_ws.onopen = () ->
                    heartCheck()
                    if hotpoor_ws_device != WS_DEVICE.POST
                        hotpoor_ws_device = WS_DEVICE.OPEN
                        hotpoor_ws_device_open = true
                        # load_chat_list() #开启hotpoor_ws成功，加载列表页
                        console.log "开启hotpoor_ws成功，加载列表页"
                        # if root.check_is_subscribe?
                        #     root.check_is_subscribe()
                hotpoor_ws.onmessage = (evt) ->
                    if hotpoor_ws_device != WS_DEVICE.POST
                        params = JSON.parse(evt.data)
                        on_message(params)
                    console.log "ws 收到消息"
                hotpoor_ws.onclose = () ->
                    console.log "hotpoor_ws_device:#{hotpoor_ws_device}"
                    if hotpoor_ws_device != WS_DEVICE.POST
                        if hotpoor_ws_device == WS_DEVICE.OPEN or hotpoor_ws_device == WS_DEVICE.READY
                            hotpoor_ws_device = WS_DEVICE.UNKNOWN
                            console.log "wait"
                            clearTimeout hotpoor_ws_timer if hotpoor_ws_timer
                            hotpoor_ws_timer = setTimeout restart_ws_connection(), 500 if USER_ID
                        else
                            hotpoor_ws_device = WS_DEVICE.BAD
                hotpoor_ws.onerror = () ->
                    console.log "ws error"
                clearTimeout hotpoor_ws_timer if hotpoor_ws_timer
                hotpoor_ws_timer = setTimeout restart_ws_connection, 10000 if USER_ID
            else
                if hotpoor_ws_device_open
                    clearTimeout hotpoor_ws_timer if hotpoor_ws_timer
                    hotpoor_ws_timer = setTimeout restart_ws_connection, 10000 if USER_ID
                    return
        restart_ws_connection()