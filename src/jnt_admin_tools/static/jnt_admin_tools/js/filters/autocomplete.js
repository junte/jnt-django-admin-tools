"use strict";

(function ($) {
  $(document).ready(function () {
    const LIST_FILTER = "is-list-filter";
    const PARAMETER = "parameter";

    initUI();
    initHandlers();

    function initUI() {
      $("select[" + LIST_FILTER + "]")
        .next("span.select2.select2-container")
        .css("width", "100%");
    }

    function initHandlers() {
      $("select[" + LIST_FILTER + "]").on("change", function (e) {
        let $target = $(e.target);

        const value = $target.val();
        const parameter = $target.data(PARAMETER);

        setFilter(parameter, value);
      });
    }

    function setFilter(parameter, value) {
      window.location.search = updateSearch(
        window.location.search,
        parameter,
        value,
      );
    }

    function updateSearch(search, parameter, value) {
      const searchParams = new URLSearchParams(search);
      searchParams.delete(parameter);

      if (!value) {
        return searchParams.toString();
      }

      if (!Array.isArray(value)) {
        value = [value];
      }

      for (let i in value) {
        searchParams.append(parameter, value[i]);
      }

      return searchParams.toString();
    }
  });
})(django.jQuery);
