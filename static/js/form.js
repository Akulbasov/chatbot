$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				text : $('#textInput').val()
			},
			type : 'POST',
			url : '/execute'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').html(data.result).show();
				$('#successAlert2').html(data.result2).show();
				$('#successAlert3').html(data.result3).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

});
