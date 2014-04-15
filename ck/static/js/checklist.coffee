class window.Checklist
  constructor: (args)->
    $ ->
      $("#navbar-checklist").addClass "active"

      $(".submit_delete_list").click ->
        if confirm $(this).attr("name") + "を削除しますか？"
          Dajaxice.ck.ajax_delete_list callback_delete_list,
            "list_id": $(this).val()

  callback_delete_list = (data)->
    $("tr[id="+data.list_id+"]").fadeOut "slow"

$ ->
  new Checklist