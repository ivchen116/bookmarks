$(document).ready(function(){
	function isURL(str_url){ 
       var strRegex = "^((https|http)?://)"  
       + "(([0-9]{1,3}\.){3}[0-9]{1,3}" // IP形式的URL- 199.194.52.184  
       + "|" // 允许IP和DOMAIN（域名） 
       + "([0-9a-z_!~*'()-]+\.)*" // 域名- www.  
       + "([0-9a-z][0-9a-z-]{0,61})?[0-9a-z]\." // 二级域名  
       + "[a-z]{2,6})" // first level domain- .com or .museum  
       + "(:[0-9]{1,4})?" // 端口- :80  
       + "((/?)|" // a slash isn't required if there is no file name  
       + "(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$";  
       var re=new RegExp(strRegex);  
       if (re.test(str_url)){ 
           return (true);  
       }else{  
           return (false);  
       } 
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
