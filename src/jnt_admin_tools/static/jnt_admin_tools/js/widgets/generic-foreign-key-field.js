(function($) {
    overrideDjangoSelect2();

    function overrideDjangoSelect2() {
      function getIds(targetTag) {
        return encodeURI($(targetTag).data('gfk-Models'));
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
          if (result && data.autocompleteUrl) {
            result.data('autocompleteUrl', data.autocompleteUrl);
          }
          return result;
        }
        return ExtendedAjaxAdapter;
      });

    }

}(django.jQuery));

(function($) {
    $(document).ready(function() {
      var STACKED_INLINE = 'stacked';
      var TABULAR_INLINE = 'tabular';

      $('.generic-foreign-key-field').on('change', function(e){
        select2Handle(e.target);
      });

      hideFkFields();
      updateGFKLabels();
      initSelect2();

      function select2Handle(target) {
        addForeignField(target);
      };

      function initSelect2(){
        var fields = $('.generic-foreign-key-field');

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

      function hideFkFields() {
        var fields = $('.generic-foreign-key-field');
        for (var i = 0; i < fields.length; i++) {
          $('fieldset.module.aligned div.form-row.field-' + $(fields[i]).data('fk-Field')).hide();
        };
      };

      function updateGFKLabels() {
        var fields = $('.generic-foreign-key-field');
        for (var i = 0; i < fields.length; i++) {
          var $field = $(fields[i]);
          var name = $field.data('gf-Name');
          name = name.substr(0, 1).toUpperCase() + name.substr(1);
          var ctField = $field.data('ct-Field');
          $('div.form-row.field-' + ctField + ' label').text(name + ':');
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
          width: '280px',
        };

        $sel.addClass(selectClass);
        $sel.appendTo($(target).parent());
        $sel.data('fk-Field', $(target).data('fk-Field'));
        $sel.select2(settings);
        $sel.parent().find('.select2-container').addClass('select2-container--admin-autocomplete');

        $sel.on('change', function(e){
          var newValue = $(e.target).find(':selected').first();
          var fkField = $(e.target).data('fk-Field');
          $('#' + prefixId + fkField).val(newValue.val());
        });
      };

    });

}(django.jQuery));
