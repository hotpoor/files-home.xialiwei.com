// Generated by CoffeeScript 2.7.0
(function() {
  var Hs, WS_DEVICE, hotpoor_timestamp, hotpoor_ws, hotpoor_ws_device, root;

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  // !!!! Hotpoor root object
  root.Hs || (root.Hs = {});

  Hs = root.Hs;

  Hs.DEVICE_USER = null;

  hotpoor_ws = null;

  hotpoor_timestamp = null;

  hotpoor_ws_device = null;

  WS_DEVICE = {
    UNKNOWN: 0,
    READY: 1,
    OPEN: 2,
    POST: 3,
    BAD: 4
  };

  root.video_play = function() {
    $("video")[0].currentTime = 0;
    return $("video")[0].play();
  };

  root.join_info = function(content_json, m_aim) {
    console.log("content_json", content_json);
    return console.log("m_aim", m_aim);
  };

  $(function() {
    var heartCheck, hotpoor_ws_device_open, hotpoor_ws_timer, restart_ws_connection;
    if (typeof BLOCK_ID !== "undefined" && BLOCK_ID !== null) {
      hotpoor_ws_device = WS_DEVICE.UNKNOWN;
      hotpoor_ws_device_open = false;
      hotpoor_ws_timer = null;
      heartCheck = function(num = 0) {
        var message;
        message = JSON.stringify(["PING", num]);
        console.log("hotpoor_ws_device", hotpoor_ws_device, hotpoor_ws);
        if (hotpoor_ws_device === WS_DEVICE.OPEN) {
          return setTimeout(function() {
            return hotpoor_ws.send(message);
          }, 10000);
        } else {
          return setTimeout(function() {
            return heartCheck(num);
          }, 1000);
        }
      };
      restart_ws_connection = function() {
        var on_message;
        console.log("restart_ws_connection");
        on_message = function(params) {
          var content_json, m_aim, m_plus, m_type, num;
          // console.log params
          m_type = params[0];
          content_json = params[1];
          m_plus = "";
          m_aim = params[2];
          if (m_type === "PONG") {
            num = content_json + 1;
            return heartCheck(num);
          } else if (m_type === "JOIN" || m_type === "LEAVE") {
            return join_info(content_json, m_aim);
          } else if (m_type === "VIDEO_PLAY") {
            return root.video_play();
          }
        };
        // Hs.video_list.push video_uri
        // console.log Hs.video_list
        if ("WebSocket" in window && hotpoor_ws_device === WS_DEVICE.UNKNOWN) {
          if (hotpoor_ws != null) {
            hotpoor_ws.close();
          }
          hotpoor_ws = new WebSocket(WEBSOCKET_URL);
          hotpoor_ws_device = WS_DEVICE.READY;
          hotpoor_ws.onopen = function() {
            heartCheck();
            if (hotpoor_ws_device !== WS_DEVICE.POST) {
              hotpoor_ws_device = WS_DEVICE.OPEN;
              hotpoor_ws_device_open = true;
              // load_chat_list() #开启hotpoor_ws成功，加载列表页
              return console.log("开启hotpoor_ws成功，加载列表页");
            }
          };
          // if root.check_is_subscribe?
          //     root.check_is_subscribe()
          hotpoor_ws.onmessage = function(evt) {
            var params;
            if (hotpoor_ws_device !== WS_DEVICE.POST) {
              params = JSON.parse(evt.data);
              on_message(params);
            }
            return console.log("ws 收到消息");
          };
          hotpoor_ws.onclose = function() {
            console.log(`hotpoor_ws_device:${hotpoor_ws_device}`);
            if (hotpoor_ws_device !== WS_DEVICE.POST) {
              if (hotpoor_ws_device === WS_DEVICE.OPEN || hotpoor_ws_device === WS_DEVICE.READY) {
                hotpoor_ws_device = WS_DEVICE.UNKNOWN;
                console.log("wait");
                if (hotpoor_ws_timer) {
                  clearTimeout(hotpoor_ws_timer);
                }
                if (USER_ID) {
                  return hotpoor_ws_timer = setTimeout(restart_ws_connection(), 500);
                }
              } else {
                return hotpoor_ws_device = WS_DEVICE.BAD;
              }
            }
          };
          hotpoor_ws.onerror = function() {
            return console.log("ws error");
          };
          if (hotpoor_ws_timer) {
            clearTimeout(hotpoor_ws_timer);
          }
          if (USER_ID) {
            return hotpoor_ws_timer = setTimeout(restart_ws_connection, 10000);
          }
        } else {
          if (hotpoor_ws_device_open) {
            if (hotpoor_ws_timer) {
              clearTimeout(hotpoor_ws_timer);
            }
            if (USER_ID) {
              hotpoor_ws_timer = setTimeout(restart_ws_connection, 10000);
            }
          }
        }
      };
      return restart_ws_connection();
    }
  });

}).call(this);
