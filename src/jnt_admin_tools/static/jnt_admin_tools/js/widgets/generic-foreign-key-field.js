(function($) {
    overrideDjangoSelect2();

    function overrideDjangoSelect2() {
      function getIds(targetTag) {
        return $(targetTag).data('gfk-Models').split(",");
      }

      var init = function($element, options) {
        var settings = $.extend({
          ajax: {
            data: function(params) {
              return {
                term: params.term,
                page: params.page,
                ids: getIds(this),
              };
            }
          },

          dataAdapter: $.fn.select2.amd.require('select2/data/extended-ajax'),

        }, options);
      $element.select2(settings);
      };

      $.fn.djangoAdminSelect2 = function(options) {
        var settings = $.extend({}, options);
        $.each(this, function(i, element) {
            var $element = $(element);
            init($element, settings);
        });
        return this;
      };

      var baseApply = $.fn.select2.amd.define;

      $.fn.select2.amd.define('select2/data/extended-ajax',['./ajax','../utils','jquery'], function(AjaxAdapter, Utils, $){

        function ExtendedAjaxAdapter ($element, options) {
          this.minimumInputLength = options.get('minimumInputLength');
          this.defaultResults     = options.get('defaultResults');
          ExtendedAjaxAdapter.__super__.constructor.call(this,$element,options);
        }

        Utils.Extend(ExtendedAjaxAdapter, AjaxAdapter);

        var originalOption = ExtendedAjaxAdapter.prototype.option;

        ExtendedAjaxAdapter.prototype.option = function(data){
          result = originalOption.call(this, data);
          if (result) {
            if (data.autocomplete_url) {
              result.data("autocompleteUrl", data.autocomplete_url);
            };
            if (data.data_app) {
              result.data("app", data.data_app);
            };
            if (data.data_model) {
              result.data("model", data.data_model);
            };
            if (data.data_change_url) {
              result.data("change-url", data.data_change_url);
            };
          };
          return result;
        }
        return ExtendedAjaxAdapter;
      });

    }

}(django.jQuery));

(function($) {
    $(document).ready(function() {
      var GFK_SELECTOR = ".generic-foreign-key-field";

      $(GFK_SELECTOR).on('change', function(e){
        select2Handle(e.target);
      });

      wrapGFKClass();
      updateGFKLabels();
      initSelect2();

      function select2Handle(target) {
        addForeignField(target);
      };

      function initSelect2(){
        var fields = $(GFK_SELECTOR);

        for (var i = 0; i < fields.length; i++) {
          var $field = $(fields[i]);
          var inlineParams = getInlineParams($field);

          if (inlineParams.isHidden) {
            continue;
          }

          var prefixId = 'id_';

          if (inlineParams.isInline) {
            prefixId = inlineParams.prefix;
          }

          var fkFieldId = prefixId + $field.data('fk-Field');
          var ctFieldId = prefixId + $field.data('ct-Field');
          var gfFieldId = prefixId + $field.data('gf-Name');

          var fkValue = $('#' + fkFieldId).val();
          var ctValue = $('#' + ctFieldId).val();
          var gfValue = $('#' + fkFieldId).data('present');

          if (ctValue || fkValue) {
            var data = undefined;

            if (fkValue && gfValue) {
              data = {'id': fkValue, 'text': gfValue};
            }

            addForeignField($field, data);
          }

        }
      };

      function updateGFKLabels() {
        var fields = $(GFK_SELECTOR);
        for (var i = 0; i < fields.length; i++) {
          var $field = $(fields[i]);
          var name = $field.data('gf-Name');
          name = name.substr(0, 1).toUpperCase() + name.substr(1);
          var ctField = $field.data('ct-Field');
          $('div.form-row.field-' + ctField + ' label').text(name + ':');

          if ($field.closest("div.tabular.inline-related").length) {
            var $currentCell = $field.closest("td");
            var cellIndex = $currentCell.closest("tr").find("td").index($currentCell);
            $($currentCell.closest("table").find("thead th")[cellIndex]).text(name);
          }
        };
      };

      function wrapGFKClass(){
        var fields = $(GFK_SELECTOR);

        for (var i = 0; i < fields.length; i++) {
          $(fields[i]).closest("div.related-widget-wrapper").addClass("gfk-related-widget-wrapper");
        };
      };

      function getInlineParams($field){
        var inlineFormset = $field.closest('div.inline-group');
        var params = {
          'isInline': false,
          'isHidden': false,
          'prefix': '',
          'inlineType': undefined,
        }

        if (inlineFormset.length) {
          var data = inlineFormset.data();
          var prefix = $field.attr('id').replace($field.data('ct-Field'), '');

          params['isInline'] = true;
          params['isHidden'] = prefix.indexOf('__prefix__') !== -1;
          params['prefix'] = prefix;
          params['inlineType'] = data.inlineType;
        }

        return params;
      }

      function addForeignField(target, data) {
        var fkFieldPlaceSelector = ".generic-foreign-key-fk-field";
        var selectClass = 'updated-foreign-field';
        var selectForeignField = $(target).parent().find('.' + selectClass).first();

        if (selectForeignField) {
          $(selectForeignField).select2('destroy');
          $(selectForeignField).remove();
        }

        var inlineParams = getInlineParams($(target));

        if (inlineParams.isHidden) {
          return;
        }

        var prefixId = 'id_';

        if (inlineParams.isInline) {
          prefixId = inlineParams.prefix;
        }


        var selected = $(target).find(':selected').first();
        var hiddenForeignField = $('#' + prefixId + $(target).data('fk-Field'));

        if (selected == undefined || !selected.val()){
          hiddenForeignField.val('');
          return;
        }
        else if (!data) {
           hiddenForeignField.val('');
        };

        var $sel = $('<select>');

        if (data){
          $sel.append($('<option>', {'value': data.id}).text(data.text));
        }

        var settings = {
          ajax: {
            url: selected.data('autocompleteUrl'),
            dataType: 'json',
            delay: 250,
            data: function (params) {
              return {
                term: params.term,
                page: params.page
              };
            },

            processResults: function (data, params) {
              params.page = params.page || 1;

              return {
                results: data.results,
                pagination: {
                    more: (params.page * 30) < data.total_count
                }
              };
            },
            cache: true,
          },
          minimumInputLength: 0,
          placeholder: 'Select the ' + selected.text(),
          width: 'auto',
        };

        $sel.addClass(selectClass);
        $sel.appendTo($(target).parent().find(fkFieldPlaceSelector));
        $sel.data('fk-Field', $(target).data('fk-Field'));
        $sel.select2(settings);
        $sel.parent().find('.select2-container').addClass('select2-container--admin-autocomplete');

        $sel.on('change', function(e){
          var newValue = $(e.target).find(':selected').first();
          var fkField = $(e.target).data('fk-Field');
          $('#' + prefixId + fkField).val(newValue.val());
        });
      };

      $("a.clear-generic-field").on("click", function(event) {
          event.preventDefault();
          $(event.target).closest(".gfk-related-widget-wrapper").find("select").first().val(null).trigger("change");
      });

      $("a.generic-foreign-field-wrapper-href").on("click", function (event) {
        event.preventDefault();

        var $target = $(event.target);
        var editId = $target.closest(".gfk-related-widget-wrapper").find(".generic-foreign-key-fk-field select").val();
        var changeUrlTemplate = $target.closest(".gfk-related-widget-wrapper").find(".generic-foreign-key-field").find("option:selected").data("change-url");
        if (!changeUrlTemplate) {
          return;
        };
        var changeUrl = changeUrlTemplate.replace("{id}", editId);
        changeUrl = changeUrl + "?_to_field=id&_popup=1";
        $("a.generic-foreign-field-wrapper-href").attr({"href": changeUrl});
      });
    });
}(django.jQuery));
