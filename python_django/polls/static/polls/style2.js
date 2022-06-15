;(function($, document, window, undefined) {

  'use strict';
  
  var maxCharWarning2 = 

    $.fn.maxCharWarning2 = function() {

        return this.each(function() {
          var el                 = $(this),
              maxLength             = el.data('max-length'),
              warningContainerClass   = el.data('max-length-warning-container'),
              warningContainer  = $('.'+warningContainerClass),
              maxLengthMessage      = el.data('max-length-warning')
          ;
          el.keyup(function() {
            var length = el.val().length;      
            if (length >= maxLength & warningContainer.is(':empty')){
              warningContainer.html(maxLengthMessage);
              el.addClass('input-error');
            }
            else if (length < maxLength & !(warningContainer.is(':empty'))) {
              warningContainer.html('');
              el.removeClass('input-error');
            }
         });
     });
  };
})(window.jQuery || window.$, document, window);


/**
 * Export as a CommonJS module
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = maxCharWarning2;
}

 $(document).ready(function(){
        $('.js-max-char-warning2').maxCharWarning2();
    });