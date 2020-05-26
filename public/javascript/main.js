
$(document).ready(function() {


  var isAdvancedUpload = function() {
    var div = document.createElement('div');
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
  }();

  var $form = $('.box');
  var $input = $form.find('input[type="file"]')
  var $errorMsg = $form.find('span.error__message');

  function submitForm(e) {
    if ($form.hasClass('is-uploading')) {
      console.log("is uploading so returned false");
      return false;
    }

    $form.addClass('is-uploading').removeClass('is-error');

    if (isAdvancedUpload) {
      modernAjaxSend(e);
    } else {
      legacyAjaxSend(e);
    }
  }

  function modernAjaxSend(e) {
    e.preventDefault();

    var ajaxData = new FormData();

    if (droppedFiles) {
      $.each( droppedFiles, function(i, file) {
        ajaxData.append( $input.attr('name')+i, file );
        console.log("file is : ");
        console.log(file);
      });
    }

    $.ajax({
      url: $form.attr('action'),
      type: $form.attr('method'),
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
        if (!data.success) $errorMsg.text(data.error);
      },
      error: function() {
        console.log(data.error);
      }
    });
  }

  function legacyAjaxSend(e) {
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

  } else {
    $input.on('change', function(e) { // when drag & drop is NOT supported
      $form.trigger('submit');
    });
  }

  $form.on('submit', function(e) {
    submitForm(e);
  });



});