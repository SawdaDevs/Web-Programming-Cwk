$(document).ready(() => {
   $('#id_dob').attr('type', 'date');
   //$('#id_end_datetime').attr('type', 'datetime-local');
   $('#id_end_datetime').datetimepicker({
      format:'d/m/Y H:i:s'
   });
   $('#id_start_datetime').datetimepicker({
      format:'d/m/Y H:i:s'
   });
    console.log('loaded!!')
});

function progressHandler(event) {
   var percent = (event.loaded / event.total) * 100;
   $('#progressBar').val(Math.round(percent));
}

function completeHandler(event) {
   $('#progressBar').val(0);
   $('#progressBar').hide();
}

//UPLOADING IMAGE USING AJAX.
$(function () {
$('#img_file').change(function uploadFile() {
	console.log('yooo')
   $('#progressBar').show();
   var formdata = new FormData();
   var file = document.getElementById('img_file').files[0];
   formdata.append('img_file', file);
   formdata.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
   $.ajax({
      xhr: function () {
         var xhr = new window.XMLHttpRequest();
         xhr.upload.addEventListener('progress', progressHandler, false);
         xhr.addEventListener('load', completeHandler, false);
         return xhr;
      },
      type : 'POST',
      url  : '/uploadimage/',
      data : formdata,
      success: function(data) {
         $('#profile-img').attr("src",data);
      },
      processData : false,
      contentType : false,
   });
});
});
