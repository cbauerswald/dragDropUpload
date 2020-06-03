//SOURCE: https://css-tricks.com/drag-and-drop-file-uploading/

$(document).ready(function() {

  // Detects whether or not modern drag/drop is supported.
  var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
  }();

  var $form = $('.box');
  var $input = $form.find('input[type="file"]');
  var $typeInput = $('.file_type_input').find('select');
  var $errorMsg = $form.find('span.error__message');

  // set up drag drop events and submit form on DROP

  if (isAdvancedUpload) {
    $form.addClass('has-advanced-upload');

    var droppedFiles = false;

    $form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
    })
    .on('dragover dragenter', function() {
      $form.addClass('is-dragover');
    })
    .on('dragleave dragend drop', function() {
      $form.removeClass('is-dragover');
    })
    .on('drop', function(e) { // when drag & drop is supported
      droppedFiles = e.originalEvent.dataTransfer.files;
      $form.trigger('submit');
    });

  }
  
  $input.on('change', function(e) { // when user does traditional file upload
    droppedFiles = this.files;
    $form.trigger('submit');
  });
  

  function submitForm(e) {
    //prevent results from being uploaded with null test type
    if ($typeInput.val() === null ) {
      alert("You must choose a test type.");
      return false;
    }
    //prevent multiple uploads
    if ($form.hasClass('is-uploading')) {
      return false;
    }

    //upadate html to show we are uploading and alert future calls that upload is aleady in progress
    $form.addClass('is-uploading').removeClass('is-error');

    //same parameter works to check if ajax file upload can be used
    if (isAdvancedUpload) { 
      modernAjaxSend(e);
    } else {
      legacyAjaxSend(e);
    }
  }

  function modernAjaxSend(e) {
    e.preventDefault();

    var ajaxData = new FormData();

    //add all files to ajaxData to be sent to server
    if (droppedFiles) {
      $.each( droppedFiles, function(i, file) {
        ajaxData.append( $input.attr('name'), file );
      });
      ajaxData.append($typeInput.attr('name'), $typeInput.val());
    }

    $.ajax({
      url:'/fileupload',
      type: 'POST',
      data: ajaxData,
      dataType: 'json',
      cache: false,
      contentType: false,
      processData: false,
      complete: function() {
        $form.removeClass('is-uploading');
      },
      success: function(data) {
        $form.addClass( data.success == true ? 'is-success' : 'is-error' );
        $form.find('.box__success .fileCount').html(data.fileCount + " "); 
        // if there is an error, display it to the user
        if (!data.success) $errorMsg.text(data.error);
      },
      error: function() {
        console.log(data.error);
      }
    });
  }

  function legacyAjaxSend(e) {
    //untested, for use in older browsers (IE9 and below) where modern ajax not supported
    var iframeName  = 'uploadiframe' + new Date().getTime();
      $iframe   = $('<iframe name="' + iframeName + '" style="display: none;"></iframe>');

    $('body').append($iframe);
    $form.attr('target', iframeName);

    $iframe.one('load', function() {
      var data = JSON.parse($iframe.contents().find('body' ).text());
      $form
        .removeClass('is-uploading')
        .addClass(data.success == true ? 'is-success' : 'is-error')
        .removeAttr('target');
      if (!data.success) $errorMsg.text(data.error);
      $form.removeAttr('target');
      $iframe.remove();
    });
  }

  $form.on('submit', function(e) {
    submitForm(e);
  });
});