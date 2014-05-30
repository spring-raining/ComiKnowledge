class window.Timechart
  _args = {}
  _timechartPressing = false;
  _downedBlock = null;
  _selectingBlock = [];
  _timechartParent = null;
  _viewColor = ["#2699BF", "#B5D145", "#F5CC38", "#F1BC39", "#E68840", "#D2495B"];

  constructor: (@args, form_cancel, form_submit)->
    $ ->
      _args = args

      # timechartにBlockを加える
      for i in [0...60]
        $timechartBlock = $('<div class="timechart-block"></div>');
        $timechartBlock.addClass "timechart-block-" + i
        $timechartBlock.attr "data-toggle", "tooltip"

        hour = Math.floor(i/12+10) + ":"
        min = String(i%12*5)
        if min.length is 1
          min = "0" + min
        $timechartBlock.attr "title", hour + min
        if i%12 is 11
          $timechartBlock.addClass "timechart-block-hour"

        $timechartBlock.mousedown ->
            _selectingBlock = []
            $(".timechart-pop")
              .popover "hide"
              .remove()
            _timechartParent = $(this).parent()
            for j in [0...60]
              _timechartParent
                .children ".timechart-block-" + j
                .removeClass "timechart-block-selecting"
            _timechartPressing = true
            for j in [0...60]
              if $(this).hasClass("timechart-block-" + j)
                k = j
            _selectingBlock.push k
            _downedBlock = k
            $(this).addClass "timechart-block-selecting"

        $timechartBlock.hover ->
            if not _timechartPressing
              return
            _selectingBlock = []
            j = 0;
            for k in [0...60]
              if j >= 2
                j++
              if $(this).hasClass("timechart-block-" + k)
                j++
              if k is _downedBlock
                j++
              if j is 1 or j is 2
                _timechartParent
                  .children ".timechart-block-" + k
                  .addClass "timechart-block-selecting"
                _selectingBlock.push k
              else
                _timechartParent
                  .children ".timechart-block-" + k
                  .removeClass "timechart-block-selecting"

        $("*").mouseup ->
            if not _timechartPressing
              return
            time = $(_timechartParent)
              .children ".timechart-block-" + _selectingBlock[0]
              .attr "data-original-title"
              .split ":"
            $("#form-start-hour").attr "value", time[0]
            $("#form-start-min").attr "value", time[1]
            $("#form-event-hour").attr "value", time[0]
            $("#form-event-min").attr "value", time[1]
            time = $(_timechartParent)
              .children ".timechart-block-" + _selectingBlock[_selectingBlock.length-1]
              .attr "data-original-title"
              .split ":"
            $("#form-finish-hour").attr "value", time[0]
            $("#form-finish-min").attr "value", time[1]
            $timechartPop = $('<div class="timechart-pop"></div>')
            j = _selectingBlock[Math.floor(_selectingBlock.length / 2)]
            $(_timechartParent)
              .children ".timechart-block-" + j
              .after $timechartPop
            pos = $(_timechartParent)
              .children ".timechart-block-" + j
              .position()

            $timechartPop
              .css "top", pos.top
              .css "left", pos.left + if _selectingBlock.length % 2 is 1 then $(".timechart-block").width()/2 else 0
              .popover
                html: true,
                placement: "bottom",
                animation: false,
                trigger: "focus",
                content: ->
                  return $("#popover-content-original").html()

            $timechartPop.popover "show"
            $("#form-cancel").click _form_cancel
            $("#form-submit").click _form_submit
            $("#collapse-body").on "hide.bs.collapse", _form_cancel
            _timechartPressing = false
            _selectingBlock = []

        $(".timechart").append $timechartBlock

      # timechart-viewにBlockを加える
      for i in [0...60]
        $timechartViewBlock = $('<div class="timechart-view-block"></div>')
        $timechartViewBlock.addClass "timechart-view-block-" + i
        if i%12 is 11
          $timechartViewBlock.addClass "timechart-view-block-hour"
        $(".timechart-view").append $timechartViewBlock

      $("[data-toggle=tooltip]").tooltip
          placement: "bottom"
          animation: false

      _form_cancel = ->
        $(".timechart-pop")
          .popover "hide"
          .remove()
        for j in [0...60]
          _timechartParent
            .children ".timechart-block-" + j
            .removeClass "timechart-block-selecting"
        do form_cancel

      _form_submit = ->
        do form_submit