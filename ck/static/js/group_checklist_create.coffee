class window.GroupChecklistCreate
  _args = {}

  constructor: (@args)->
    $ ->
      _args = args

      $(".form_first").change ->
        $(".form_list[value=" + $(this).val() + "]")
          .prop "checked", true
        for i in [1..9]
          $target = $(".sorting_color_" + i + ",.select_color_" + i)
          if args.color[$(this).val()][i-1] isnt ""
            $target.css "background-color", args.color[$(this).val()][i-1]
          else
            $target.css "background-color", args.default_color[i-1]

      $(".form_list").click ->
        if not $(this).prop "checked"
          $target = $(".form_first[value=" + $(this).val() + "]")
          if $target.prop "checked"
            $target.prop "checked", false
            for i in [1..9]
              $(".sorting_color_" + i + ",.select_color_" + i)
                .css "background-color", args.default_color[i-1]

      for i in [1..9]
        $(".sorting_color_" + i + ",.select_color_" + i)
          .css "width", "32px"
          .css "height", "32px"
          .css "background-color", args.default_color[i-1]

      $("#sortable-color").sortable
        axis: "x"
        cursor: "move"

      $("#submit").click ->
        $("#color-order")
          .val($("#sortable-color").sortable "toArray")
        $("form")
          .submit()
