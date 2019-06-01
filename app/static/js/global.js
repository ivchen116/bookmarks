$(document).ready(function(){
	function isURL(str){
		return !!str.match(/(((^https?:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-_]*)?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)$/g);
	}
	$('#addarticle-menu').popover({
		container: 'body',
		html: 'true',
		placement: 'bottom',
		content : function() {
		return $('#addarticle-content').html();
	}
	}).on('shown.bs.popover', function (eventShown) {
		var $popup = $('#' + $(eventShown.target).attr('aria-describedby'));
		$popup.find('input.url').keypress(function(e){
			if(event.keyCode == "13")    
			{
				$popup.find('button.save').trigger("click",e);
				e.preventDefault();
			}
		});

		$popup.find('button.save').click(function (e) {
			article_url = $popup.find('input.url').val();
			$popup.find('div.form-group').removeClass('has-error');
			if(!isURL(article_url)) {
				$popup.find('div.form-group').addClass('has-error');
				return;
			}
			$.ajax({    
				url: "/item/add",    
				dataType: "json", 
				data: { url:  article_url},    
				type: "POST",    
				success: function(data) {
					if (data.status == '1') {
						$popup.popover('hide');
					} else {
						$popup.find('div.form-group').addClass('has-error');
					}
				}, 
				error: function(data) {        
					$popup.find('div.form-group').addClass('has-error');
				}
			});
			
		});
	});
});