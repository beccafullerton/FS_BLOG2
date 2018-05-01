function ajaxCall(url, type, data, processData, contentType, successFunction) {
	var data_string;
	var csrftoken = getCookie('csrftoken');
	$.ajax({
		beforeSend: function(xhr, settings) {
			if (!this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		url: url,
		type: type,
		data: data,
		processData: processData,
		contentType: contentType,
		success: successFunction
	})
	
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
};

function sizeTitleEqualizerSpace(data, div){
	generatePosts(data, div, function() {
		// get height of each post title and set equalizer equal to its height
		$(".post_title").each(function() {
			var id = $(this).attr("id");
			var postTitleDivHeight = $('#' + id).outerHeight();
			var eqID = "#eq" + id;
			$(eqID).css({"height": postTitleDivHeight +"px"});
		});
	})
}

function generatePosts(data, div, _callback) {
	$(div).append(data)
	_callback();
}

