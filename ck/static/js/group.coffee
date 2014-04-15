class window.Group
  constructor: ->
    $ ->
      $("#navbar-group").addClass("active");
      $("#submit_create_group").click ->
        Dajaxice.ck.ajax_create_group callback_create_group,
          "form": $("#form_create_group").serialize true

      $(".submit_verify_join").click ->
        Dajaxice.ck.ajax_verify_join callback_verify_join,
          "group_id": $(this).attr "value"

      $(".submit_reject_join").click ->
          Dajaxice.ck.ajax_reject_join callback_reject_join,
            "group_id": $(this).attr "value"

  callback_create_group = (data)->
    $("#alert")
      .removeClass "alert-success alert-danger"
      .hide()
    $(".form-group")
      .removeClass "has-error"

    if data.alert_code is 1
      $("#alert")
        .addClass "alert-success"
        .text data.group_name + "が作成されました！"
        .show()
      $("#groups")
        .append '<tr><td><a href="/group/'+data.group_id+'">'+data.group_name+'</a></td></tr>'
      $(".form-control")
        .val ""

    else if data.alert_code is 2
      $("#alert")
        .addClass "alert-danger"
        .text "空欄に内容を入力してください"
        .show()
      $(".form-group").each ->
        if $(this).find(".form-control").val() is ""
          $(this).addClass "has-error"

    else if data.alert_code is 3
      $("#alert")
        .addClass "alert-danger"
        .text "すでに同じグループIDが使われています"
        .show()
      $("#form_id")
        .parents ".form-group"
        .addClass "has-error"

    else if data.alert_code is 4
      $("#alert")
        .addClass "alert-danger"
        .text "このグループIDは登録できません"
        .show()
      $("#form_id")
        .parents ".form-group"
        .addClass "has-error"

    else if data.alert_code is 5
      $("#alert")
        .addClass "alert-danger"
        .text "1人が参加出来るグループは30個までです"
        .show()


  callback_verify_join = (data)->
    $("#alert_join")
      .removeClass "alert-success alert-danger"
      .hide()
    $(".form-group")
      .removeClass "has-error"

    if data.alert_code is 1
      $("#alert_join")
        .addClass "alert-success"
        .text data.group_name + "に参加しました！"
        .show()
      $("tr[title='"+data.group_id+"']")
        .remove()
      $("#groups")
        .append '<tr><td><a href="/group/'+data.group_id+'">'+data.group_name+'</a></td></tr>'

    else if data.alert_code is 2
      $("#alert_join")
        .addClass "alert-danger"
        .text "1人が参加出来るグループは30個までです"
        .show()


  callback_reject_join = (data)->
    $("#alert_join")
      .addClass "alert-success"
      .text data.group_name + "の招待を却下しました"
      .show()
    $("tr[title='"+data.group_id+"']")
      .remove()