class window.GroupHome
  _args = {}
  _description = ""

  constructor: (@args)->
    $ ->
      _args = args
      _description = args.group__description

      $("#submit_request_join").click ->
        Dajaxice.ck.ajax_request_join callback_request_join,
          "form": $("#form_request_join").serialize true

      $("#submit_update_description").click ->
        Dajaxice.ck.ajax_update_group_description callback_update_description,
          "form": $("#form_update_description").serialize true

      $(".submit_delete_list").click ->
        if confirm $(this).attr("name") + "を削除しますか？"
          Dajaxice.ck.ajax_delete_list callback_delete_list,
            "list_id": $(this).val()

      $("#submit_leave_group").click ->
        if confirm args.group__name + "から抜けますか？"
          Dajaxice.ck.ajax_leave_group callback_leave_group,
            "group_id": args.group__group_id

      $("#edit_description").click ->
        if _description is "説明文はありません"
          _description = ""
        $("#form_description")
          .attr "rows", _description.split("\n").length + 1
          .val(_description.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, "&"))
        $(this).hide()
        $("#description").hide()
        $("#form_update_description").show()

      $("#cancel_update_description").click ->
        $("#form_update_description").hide()
        $("#description").show()
        $("#edit_description").show()


  callback_request_join = (data)->
    $("#alert")
      .removeClass("alert-success alert-danger")
      .hide()
    $(".form-group")
      .removeClass("has-error")
    if data.alert_code is 1
      $("#alert")
        .addClass "alert-success"
        .text data.user_id + " を招待しました！"
        .show()
      $("#form_name")
        .val ""

    else if data.alert_code is 2
      $("#alert")
        .addClass "alert-danger"
        .text "Twitter IDを入力してください"
        .show()
      $(".form-group")
        .addClass "has-error"

    else if data.alert_code is 3
      $("#alert")
        .addClass "alert-danger"
        .text data.user_id + " はまだComiKnowledgeにログインしていません"
        .show()
      $(".form-group")
        .addClass "has-error"

    else if data.alert_code is 4
      $("#alert")
        .addClass "alert-danger"
        .text data.user_id + " はすでにグループに参加しています"
        .show()
      $(".form-group")
        .addClass "has-error"


  callback_update_description = (data)->
    description = data.description
    if description is ""
      description = "説明文はありません"
    $("#description").text description
    $("#form_update_description").hide()
    $("#description").show()
    $("#edit_description").show()


  callback_delete_list = (data)->
    $("tr[id="+data.list_id+"]").fadeOut("slow")


  callback_leave_group = (data) ->
      document.location = _args.url__group
