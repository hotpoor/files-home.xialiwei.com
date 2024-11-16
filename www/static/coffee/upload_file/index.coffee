root = exports ? this
# !!!! Hotpoor root object
root.Hs or= {}
Hs = root.Hs

$ ->
    load_page_btns_ajax = null
    load_page_btns = (page_index=0,page_each=10)->
        if load_page_btns_ajax != null
            load_page_btns_ajax.abort()
            load_page_btns_ajax = null
        load_page_btns_ajax=$.ajax
            url:"/api/upload/list"
            method:"GET"
            dataType:"json"
            data:
                page_index:page_index
                page_each:page_each
            success:(data)->
                console.log data
                $(".file_list_show_page_btns").empty()
                $(".file_list_show_page_main").empty()
                for i in [0..parseInt(data.files_num/page_each)]
                    $(".file_list_show_page_btns").append """
                    <button class="page_btns_btn" data-index="#{i}" >#{i+1}</button>
                    """
                for result_item in data.result
                    thumbnail = "/static/img/files-home-no-thumbnail.jpg"
                    down_load_path = "/#{SOURCE_PATH}/#{result_item[0]}" 
                    if result_item[7].indexOf("image")>-1
                        thumbnail = "/#{SOURCE_PATH}/#{result_item[0]}"
                    $(".file_list_show_page_main").append """
                    <div class="page_main_item">
                        <div class="page_main_item_card">
                            <div class="page_main_item_card_line">
                                <img src="#{thumbnail}">
                            <div>
                            <div class="page_main_item_card_line">
                                <div>filename: #{result_item[1]}</div>
                            <div>
                            <div><a href="#{down_load_path}" target="_blank">下载</a></div>
                        </div>
                    </div>
                    """

            error:(data)->
                console.log data

    $(window).on "load",()->
        load_page_btns()
    $("body").on "click",".page_btns_btn",(evt)->
        current_index = $(this).attr "data-index"
        load_page_btns(current_index)