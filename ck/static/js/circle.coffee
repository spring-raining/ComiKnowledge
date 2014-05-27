class window.Circle
  _args = {}
  _viewColor = ["#2699BF", "#B5D145", "#F5CC38", "#F1BC39", "#E68840", "#D2495B"];

  constructor: (@args)->
    $ ->
      _args = args

      Dajaxice.ck.ajax_get_circleknowledgecomments (data) ->
        for k, v of data
          if v.length is 0
            continue
          $comment_container = $(".comment-container")
          for key, comment of v
            $html = makeCommentHtml comment
            $comment_container.append $html
      , "circle_knowledge_id": args.circle_knowledge__circle_knowledge_id

      $("#form-event").change ->
        if Number(do $("#form-event").val) is 1
          $(".visible-on-mode1").removeClass "hidden"
          $(".visible-on-mode2").addClass "hidden"
        else
          $(".visible-on-mode1").addClass "hidden"
          $(".visible-on-mode2").removeClass "hidden"
      $("#form-submit").click register_circleknowledgecomment

  #
  #   makeCommentHtml
  #   .comment-containerに追加するDOM要素を作成
  #
  makeCommentHtml = (co) ->
    $html = $ """
              <div class="panel panel-default">
                <img class="img-thumbnail" align="left" style="height: 73px; padding: 2px;">
                <div class="panel-body">
                </div>
              </div>"
              """

    $img_thumbnail = $html.children ".img-thumbnail"
    $panel_body = $html.children ".panel-body"

    appendZero = (num)->
      if num < 10
        num = "0" + num
      return num

    if co.event_code is 0
      $panel_body
        .text "#{appendZero co.event_time_hour} : #{appendZero co.event_time_min}"
    else if co.event_code is 1
      $panel_body
        .text "#{appendZero co.start_time_hour} : #{appendZero co.start_time_min} 〜 " +
          "#{appendZero co.finish_time_hour} : #{appendZero co.finish_time_min} " +
          "並びました"
    else if co.event_code is 2
      $panel_body
        .text "#{appendZero co.event_time_hour} : #{appendZero co.event_time_min} " +
          "頒布物が売り切れました"
    else if co.event_code is 3
      $panel_body
        .text "#{appendZero co.event_time_hour} : #{appendZero co.event_time_min} " +
          "限数が変わりました"

    if co.comment
      $panel_body
        .append "<br>#{co.comment}"

    if co.onymous
      $img_thumbnail.attr "src", co.parent_user__thumbnail__url
      $panel_body.append "(#{co.parent_user__username})"
    else
      $img_thumbnail.attr "src", _args.static_url + "png/thumbnail_73.png"

    if co.is_my_comment
      $button = $ """
                  <button type="button" class="btn">コメントを削除</div>
                  """
      $button.click ->
        if confirm("このコメントを削除しますか？")
          Dajaxice.ck.ajax_delete_circleknowledgecomment(
            callback_delete_circleknowledgecomment
            "comment_id": co.id
          )
      $html.append $button

    return $html

  #
  #   register_circleknowledgecomment
  #   circleknowledgecommentを登録
  #
  register_circleknowledgecomment = ->
    post = {}
    post["circle_knowledge_id"] = _args.circle_knowledge__circle_knowledge_id;
    post["onymous"] = $("#form-onymous").prop "checked"
    post["event"] = Number $("#form-event").val()
    post["comment"] = $("#form-description").val()

    if post.event is 1
      post["mode"] = 1
      post["start-hour"] = Number $("#form-start-hour").val()
      post["start-min"] = Number $("#form-start-min").val()
      post["finish-hour"] = Number $("#form-finish-hour").val()
      post["finish-min"] = Number $("#form-finish-min").val()
    else
      post["mode"] = 2
      post["event-hour"] = Number $("#form-event-hour").val()
      post["event-min"] = Number $("#form-event-min").val()


    Dajaxice.ck.ajax_register_circleknowledgecomment(
      callback_register_circleknowledgecomment
      "post": post
    )

  #
  #   callback_register_circleknowledgecomment
  #   ajax_register_circleknowledgecommentのコールバック関数
  #
  callback_register_circleknowledgecomment = (data) ->
    $alert = $("#alert")
    $alert
      .removeClass "alert-success alert-danger"
      .hide()

    if data.alert_code is 1
      document.location = _args.url__circle
    else if data.alert_code is 2
      $alert
        .addClass "alert-danger"
        .text "入力された時刻が正しくありません　時刻は10:00〜14:59の範囲で入力できます"
        .show()
    else if data.alert_code is 3
      $alert
        .addClass "alert-danger"
        .text "1人が登録出来る情報は5つまでです"
        .show()
    else if data.alert_code is 4
      $alert
        .addClass "alert-danger"
        .text "タイムチャートに登録できませんでした"
        .show()

  #
  #   callback_delete_circleknowledgecomment
  #   ajax_delete_circleknowledgecommentのコールバック関数
  #
  callback_delete_circleknowledgecomment = (data) ->
    $alert = $("#alert")
    $alert
      .removeClass "alert-success alert-danger"
      .hide()

    if data.alert_code is 1
      document.location = _args.url__circle
    else if data.alert_code is 2
      $alert
        .addClass "alert-danger"
        .text "タイムチャートのコメントを削除できませんでした"
        .show()