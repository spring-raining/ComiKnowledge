class window.ChecklistEdit
  _args = {}

  constructor: (@args)->
    $ ->
      _args = args

      $(".color-cell").css "background-color", ->
        index = Number($(this).attr "data-color-number") - 1
        if args.color[index] isnt "" then args.color[index] else args.default_color[index]

      $(".header-cell").click ->
        if $(this).attr "data-href"
          document.location = $(this).attr("data-href")

      $(".submit_delete_listcircle").click ->
        if confirm $(this).attr("name") + "を削除しますか？"
            Dajaxice.ck.ajax_delete_listcircle callback_delete_listcircle,
              "listcircle_id": $(this).val()


  callback_delete_listcircle = (data)->
    $("tr[id=" + data.id + "]").fadeOut "slow"
