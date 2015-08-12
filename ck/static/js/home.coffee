class window.Home
  constructor: ->
    $ ->
      for i in [1..5]
        if bi >= tumblr_api_read["posts-total"]
          break
        $tumblr = $('<a class="list-group-item"></a>')
        $tumblr.addClass "list-group-item"
        $tumblr.attr "href", tumblr_api_read["posts"][i]["url-with-slug"]
        $tumblrHeading = $('<h5 class="list-group-item-heading"></h5>')
        $tumblrHeading.text tumblr_api_read["posts"][i]["regular-title"]
        $tumblr.append $tumblrHeading
        $tumblrText = $('<small class="list-group-item-text"></small>')
        $tumblrText.text ->
          if $(tumblr_api_read["posts"][i]["regular-body"]).text().length > 80
            $(tumblr_api_read["posts"][i]["regular-body"]).text().substr(0, 80) + "…"
          else
            $(tumblr_api_read["posts"][i]["regular-body"]).text()
        $tumblr.append $tumblrText
        $("#list-tumblr").append $tumblr