// Generated by CoffeeScript 2.7.0
var Hs, root;

root = typeof exports !== "undefined" && exports !== null ? exports : this;

// !!!! Hotpoor root object
root.Hs || (root.Hs = {});

Hs = root.Hs;

$(function() {
  var load_page_btns, load_page_btns_ajax;
  load_page_btns_ajax = null;
  load_page_btns = function(page_index = 0, page_each = 10) {
    if (load_page_btns_ajax !== null) {
      load_page_btns_ajax.abort();
      load_page_btns_ajax = null;
    }
    return load_page_btns_ajax = $.ajax({
      url: "/api/upload/list",
      method: "GET",
      dataType: "json",
      data: {
        page_index: page_index,
        page_each: page_each
      },
      success: function(data) {
        var i, j, k, len, ref, ref1, result_item, results, thumbnail;
        console.log(data);
        $(".file_list_show_page_btns").empty();
        $(".file_list_show_page_main").empty();
        for (i = j = 0, ref = parseInt(data.files_num / page_each); (0 <= ref ? j <= ref : j >= ref); i = 0 <= ref ? ++j : --j) {
          $(".file_list_show_page_btns").append(`<button class="page_btns_btn" data-index="${i}" >${i + 1}</button>`);
        }
        ref1 = data.result;
        results = [];
        for (k = 0, len = ref1.length; k < len; k++) {
          result_item = ref1[k];
          thumbnail = "/static/img/files-home-no-thumbnail.jpg";
          if (result_item[7].indexOf("image") > -1) {
            thumbnail = `/${SOURCE_PATH}/${result_item[0]}`;
          }
          results.push($(".file_list_show_page_main").append(`<div class="page_main_item">
    <div class="page_main_item_card">
        <div class="page_main_item_card_line">
            <img src="${thumbnail}">
        <div>
        <div class="page_main_item_card_line">
            <div>filename: ${result_item[1]}</div>
        <div>
    </div>
</div>`));
        }
        return results;
      },
      error: function(data) {
        return console.log(data);
      }
    });
  };
  $(window).on("load", function() {
    return load_page_btns();
  });
  return $("body").on("click", ".page_btns_btn", function(evt) {
    var current_index;
    current_index = $(this).attr("data-index");
    return load_page_btns(current_index);
  });
});

//# sourceMappingURL=index.js.map