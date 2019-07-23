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
          //we need explicitly process minimumInputLength value
          //to decide should we use AjaxAdapter or return defaultResults,
          //so it is impossible to use MinimumLength decorator here
          this.minimumInputLength = options.get('minimumInputLength');
          this.defaultResults     = options.get('defaultResults');

          ExtendedAjaxAdapter.__super__.constructor.call(this,$element,options);
        }

        Utils.Extend(ExtendedAjaxAdapter,AjaxAdapter);

        //override original query function to support default results
        var originQuery = AjaxAdapter.prototype.query;

        ExtendedAjaxAdapter.prototype.option = function (data) {
          var option;

          if (data.children) {
            option = document.createElement('optgroup');
            option.label = data.text;
          } else {
            option = document.createElement('option');

            if (option.textContent !== undefined) {
              option.textContent = data.text;
            } else {
              option.innerText = data.text;
            }
          }

          if (data.id) {
            option.value = data.id;
          }

          if (data.disabled) {
            option.disabled = true;
          }

          if (data.selected) {
            option.selected = true;
          }

          if (data.title) {
            option.title = data.title;
          }

          var $option = $(option);

          if (data.dataAutocompleteUrl) {
            $option.attr('data-autocompleteUrl', data.dataAutocompleteUrl);
          }

          var normalizedData = this._normalizeItem(data);
          normalizedData.element = option;

          // Override the option's data with the combined data
          $.data(option, 'data', normalizedData);

          return $option;
        }

        ExtendedAjaxAdapter.prototype.query = function (params, callback) {
          var defaultResults = (typeof this.defaultResults == 'function') ? this.defaultResults.call(this) : this.defaultResults;
          if (defaultResults && defaultResults.length && (!params.term || params.term.length < this.minimumInputLength)){
            var processedResults = this.processResults(defaultResults,params.term);
            callback(processedResults);
          }
          else {
            originQuery.call(this, params, callback);
          }
        };

        return ExtendedAjaxAdapter;
      });

    }

}(django.jQuery));

(function($) {
    $(document).ready(function() {
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
          var fkValue = $('#id_' + $field.data('fk-Field')).val();
          var ctValue = $('#id_' + $field.data('ct-Field')).val();

          if (ctValue || fkValue) {
            var data;
            var fkPresent = $('#id_' + $field.data('gf-Name')).val();

            if (fkValue && fkPresent) {
              data = {'id': fkValue, 'text': fkPresent};
            }

            addForeignField($field, data);
          }

        }
      };

      function hideFkFields() {
        var fields = $('.generic-foreign-key-field');
        for (var i = 0; i < fields.length; i++) {
          $('div.form-row.field-' + $(fields[i]).data('fk-Field')).hide();
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

    });

    function addForeignField(target, data) {
      var selectClass = 'updated-foreign-field';
      var selectForeignField = $(target).parent().find('.'+selectClass).first();

      if (selectForeignField) {
        $(selectForeignField).select2('destroy');
        $(selectForeignField).remove();
      }

      var selected = $(target).find(':selected').first();

      if (selected == undefined || !selected.val()){
        $('#id_' + $(target).data('fk-Field')).val('');
        return;
      };

      var $sel = $('<select>');

      if (data){
        $sel.append($('<option>', {'value': data.id}).text(data.text));
      }

      var settings = {
        ajax: {
          url: selected.data('autocompleteurl'),
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
        $('#id_' + fkField).val(newValue.val());

      });
    }

}(django.jQuery));
