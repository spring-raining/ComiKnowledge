// Generated by CoffeeScript 1.9.3
(function() {
  window.GroupChecklistCreate = (function() {
    var _args;

    _args = {};

    function GroupChecklistCreate(args1) {
      this.args = args1;
      $(function() {
        var i, j;
        _args = args;
        $(".form_first").change(function() {
          var $target, i, j, results;
          $(".form_list[value=" + $(this).val() + "]").prop("checked", true);
          results = [];
          for (i = j = 1; j <= 9; i = ++j) {
            $target = $(".sorting_color_" + i + ",.select_color_" + i);
            if (args.color[$(this).val()][i - 1] !== "") {
              results.push($target.css("background-color", args.color[$(this).val()][i - 1]));
            } else {
              results.push($target.css("background-color", args.default_color[i - 1]));
            }
          }
          return results;
        });
        $(".form_list").click(function() {
          var $target, i, j, results;
          if (!$(this).prop("checked")) {
            $target = $(".form_first[value=" + $(this).val() + "]");
            if ($target.prop("checked")) {
              $target.prop("checked", false);
              results = [];
              for (i = j = 1; j <= 9; i = ++j) {
                results.push($(".sorting_color_" + i + ",.select_color_" + i).css("background-color", args.default_color[i - 1]));
              }
              return results;
            }
          }
        });
        for (i = j = 1; j <= 9; i = ++j) {
          $(".sorting_color_" + i + ",.select_color_" + i).css("width", "32px").css("height", "32px").css("background-color", args.default_color[i - 1]);
        }
        $("#sortable-color").sortable({
          axis: "x",
          cursor: "move"
        });
        return $("#submit").click(function() {
          $("#color-order").val($("#sortable-color").sortable("toArray"));
          return $("form").submit();
        });
      });
    }

    return GroupChecklistCreate;

  })();

}).call(this);