class window.Circle extends Timechart
  _args = {}
  _timechartPressing = false;
  _downedBlock = null;
  _selectingBlock = [];
  _timechartParent = null;
  _viewColor = ["#2699BF", "#B5D145", "#F5CC38", "#F1BC39", "#E68840", "#D2495B"];

  constructor: (@args)->
    $ ->
      _args = args

      super(args, form_cancel, form_submit)

      # timechart-viewにタイムチャートを追加する
      Dajaxice.ck.ajax_get_circleknowledgecomments (data) ->
        for k, v of data
          if v.length is 0
            continue
          height = v.length * 20
          $(".timechart-view-" + k).css "height", height
          for key, comment of v
            top = key * 20
            if comment.event_code is 1
              $timechartViewData = $('<div class="timechart-view-data-mode1"></div>')
              left  = ((comment.start_time_hour  - 10) * 12 + (comment.start_time_min  / 5) % 12) * ($(".timechart-view").width() / 60)
              width = ((comment.finish_time_hour - 10) * 12 + (comment.finish_time_min / 5) % 12) * ($(".timechart-view").width() / 60) - left
              $timechartViewData.css "top", top
              $timechartViewData.css "left", left
              $timechartViewData.css "width", Math.max(width, $(".timechart-view").width() / 90)
              time = comment.finish_time_hour * 60 + comment.finish_time_min - comment.start_time_hour * 60 - comment.start_time_min
              $timechartViewData.css "background-color", ->
                if time < 5
                  _viewColor[0]
                else if time < 10
                  _viewColor[1]
                else if time < 20
                  _viewColor[2]
                else if time < 30
                  _viewColor[3]
                else if time < 50
                  _viewColor[4]
                else
                  _viewColor[5]
            else
              $timechartViewData = $('<div class="timechart-view-data-mode2"></div>')
              left = ((comment.event_time_hour - 10) * 12 + (comment.event_time_min / 5) % 12) * ($(".timechart-view").width() / 60)
              $timechartViewData.css "top", top
              $timechartViewData.css "left", left - 11
              $timechartViewData.css "width", 20
              if comment.event_code is 0
                $timechartViewData.css "background-color", "#2AFF55"
              else if comment.event_code is 2
                $timechartViewData.css "background-color", "#FF2A2A"
              else if comment.event_code is 3
                $timechartViewData.css "background-color", "#FFFF00"

            $timechartViewData.attr "data-circleknowledgecomment-id", comment.id
            $timechartViewData.popover
              html: true
              placement: "top"
              animation: false
              trigger: "hover"
              container: "body"
              content: do (comment) ->
                  $pvco = $("#popover-view-content-original")
                    .clone()
                  $pvco
                    .find ".timechart-pop-view-comment"
                    .text comment.comment
                  if comment.onymous
                    $pvco
                      .find ".timechart-pop-view-thumbnail"
                      .css "display", "inline"
                      .children "img"
                      .attr "src", comment.parent_user__thumbnail__url
                  else
                    $pvco
                      .find ".timechart-pop-view-thumbnail"
                      .css "display", "inline"
                      .children "img"
                      .attr "src", args.static_url + "png/thumbnail_73.png"

                  if comment.event_code is 0
                    $pvco
                      .find ".timechart-pop-view-mode2"
                      .css "display", "inline"
                    hour = comment.event_time_hour
                    min = comment.event_time_min
                    if min < 10
                      min = "0" + min
                    $pvco
                      .find ".timechart-pop-view-event-hour"
                      .text hour
                    $pvco
                      .find ".timechart-pop-view-event-min"
                      .text min
                  else if comment.event_code is 1
                    $pvco
                      .find ".timechart-pop-view-mode1"
                      .css "display", "inline"
                    shour = comment.start_time_hour
                    smin = comment.start_time_min
                    fhour = comment.finish_time_hour
                    fmin = comment.finish_time_min
                    time = fhour * 60 + fmin - shour * 60 - smin
                    if smin < 10
                      smin = "0" + smin
                    if fmin < 10
                      fmin = "0" + fmin
                    $pvco
                      .find ".timechart-pop-view-start-hour"
                      .text shour
                    $pvco
                      .find ".timechart-pop-view-start-min"
                      .text smin
                    $pvco
                      .find ".timechart-pop-view-finish-hour"
                      .text fhour
                    $pvco
                      .find ".timechart-pop-view-finish-min"
                      .text fmin
                    $pvco
                      .find ".timechart-pop-view-time"
                      .text time
                    $pvco
                      .find ".timechart-pop-view-description"
                      .text "並びました"
                  else if comment.event_code is 2
                    $pvco.find ".timechart-pop-view-mode2"
                      .css "display", "inline"
                    hour = comment.event_time_hour
                    min = comment.event_time_min
                    if min < 10
                      min = "0" + min
                    $pvco
                      .find ".timechart-pop-view-event-hour"
                      .text hour
                    $pvco
                      .find ".timechart-pop-view-event-min"
                      .text min
                    $pvco
                      .find ".timechart-pop-view-description"
                      .text "頒布物が売り切れました"
                  else if comment.event_code is 3
                    $pvco
                      .find ".timechart-pop-view-mode2"
                      .css "display", "inline"
                    hour = comment.event_time_hour
                    min = comment.event_time_min
                    if min < 10
                      min = "0" + min
                    $pvco
                      .find ".timechart-pop-view-event-hour"
                      .text hour
                    $pvco
                      .find ".timechart-pop-view-event-min"
                      .text min
                    $pvco
                      .find ".timechart-pop-view-description"
                      .text "限数が変わりました"

                  if comment.onymous
                    $pvco
                      .find ".timechart-pop-view-description"
                      .append "(" + comment.parent_user__username + ")"
                  return $pvco.html()

            $(".timechart-view-wrapper-" + k).append $timechartViewData
      , "circle_knowledge_id": args.circle_knowledge__circle_knowledge_id


  form_cancel = ->
    return


  form_submit = ->
    post = {}
    post["circle_knowledge_id"] = _args.circle_knowledge__circle_knowledge_id;
    post["onymous"] = $("#form-onymous").prop "checked"
    if $("#popover-mode1").hasClass "active"
      post["mode"] = 1
      post["event"] = 1
      post["start-hour"] = Number $("#form-start-hour").val()
      post["start-min"] = Number $("#form-start-min").val()
      post["finish-hour"] = Number $("#form-finish-hour").val()
      post["finish-min"] = Number $("#form-finish-min").val()
      post["comment"] = $("#form-description1").val()
    else if $("#popover-mode2").hasClass "active"
      post["mode"] = 2
      post["event"] = Number $("#form-event").val()
      post["event-hour"] = Number $("#form-event-hour").val()
      post["event-min"] = Number $("#form-event-min").val()
      post["comment"] = $("#form-description2").val()

    Dajaxice.ck.ajax_register_circleknowledgecomment (data) ->

      console.log data
      $alert = $("#alert-form")
      $alert
        .removeClass "alert-success alert-danger"
        .hide()
      $(".timechart-pop")
        .popover "hide"
        .remove()
      for j in [0...60]
        _timechartParent
          .children ".timechart-block-" + j
          .removeClass "timechart-block-selecting"
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
    , "post": post


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
