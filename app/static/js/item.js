// Empty JS for your own code to be here

$(document).ready(function(){
	
	$('.page_queue_list').on('click', '.action_archive a', function(e){
		var item = $(this).closest('.item')
		
		$.ajax({    
			url: "/item/archive",    
			dataType: "json", 
			data: { id: item.attr("id"), done: 1 },        
			type: "POST",    
			context: item,
			success: function(data) {
				if (data.status == '1') {
					$(this).remove();
				}
			}, 
			error: function() {        
				
			}
		});	
		
		e.preventDefault();
	});
	
	function load_more_item(offset, count, state, collection) {
		items_is_loading = true;
		$("#btn-loading").attr("disabled","disabled");
		$("#btn-loading").text("加载中...");
		$.ajax({    
			url: "/item/get",    
			dataType: "json", 
			data: { offset: offset, count: count, state: state, collection: collection },        
			type: "POST",    
			success: function(data) {
				if (data.status == '1') {
					$.each(data.lists, function(i, item) {
						var item_template="<div class=\"item item_type_normal\" id=\"{id}\"><div class=\"item_content\"><a class=\"item_link start_articleview\" href=\"{url}\" target=\"_blank\"></a><a class=\"title\" href=\"{url}\">{title}</a><span class=\"thumb\" style=\"background-image: url(/static/image/direct.jpg)\"> </span><ul class=\"sub clearfix\"><li class=\"original_url_container\"><a class=\"original_url\" href=\"{url}\" target=\"_blank\">{netloc}</a></li><li class=\"tags hasTags\"><span class=\"tag_container\"><a class=\"tag\" href=\"/tags/abcd\">标签</a></span></li></ul><ul class=\"clearfix\" style=\"display:none\"><li class=\"author\">{author}</li></ul><div class=\"clear\"></div><ul class=\"buttons\"><li class=\"action_delete\" title=\"删除\"><a href=\"#\"  data-toggle=\"delete-confirmation\">删除</a></li><li class=\"action_tag\" title=\"编辑标记\"><a href=\"#\">编辑标记</a></li><li class=\"action_favorite \" title=\"标记为精华\"><a href=\"#\">标记为精华</a></li></ul></div></div> ";
						var dis_title = item.given_title?item.given_title:item.resolved_title;
						dis_title = dis_title?dis_title:item.given_url;
						var item_html=item_template.format({id:item.itemid, url:item.given_url, title:dis_title, netloc:item.netloc, author: item.author});
						$(".page_queue_list").append(item_html);
					});
					items_have_get += data.lists.length
					if (data.lists.length < items_per_page) {
						items_has_more = false;
						$("#btn-loading").hide();
						
					}
					else {
						$("#btn-loading").text("加载更多...");
						$("#btn-loading").removeAttr("disabled");
					}
				} else {
					console.log('load error...');
				}
				items_is_loading = false;
			}, 
			error: function() {        
				items_is_loading = false;
			}
		});	
	}
	items_per_page = 10;
	items_have_get = 0;
	items_is_loading = false;
	items_has_more = true;
	load_more_item(items_have_get, items_per_page, 'queue', '');
	
	$(window).scroll(function () {
		if ($(window).scrollTop() + $(window).height() == $(document).height()) { 
			if (items_is_loading==false&&items_has_more)
			{
				load_more_item(items_have_get, items_per_page, 'queue', '');
			}
		}
	});
$('body').confirmation({
    rootSelector: '[data-toggle=delete-confirmation]',
    selector: '[data-toggle=delete-confirmation]',
	container: 'body',
	singleton: true,
	popout: true,
	placement: 'bottom',
	title: '确定删除吗？',
	btnOkLabel: '删除',
	btnCancelLabel: '取消',
	onConfirm: function(value) {
		var item = $(this).closest('.item')
		
		$.ajax({    
			url: "/item/delete",    
			dataType: "json", 
			data: { id: item.attr("id") },    
			type: "POST",    
			context: item,
			success: function(data) {
				if (data.status == '1') {
					$(this).remove();
				}
			}, 
			error: function() {        
				
			}
		});
	}
});

$('#addarticle-menu').popover({
	singleton: true,
	container: 'body',
    html: 'true',
	placement: 'bottom',
	content : function() {
    return $('#addarticle-content').html();
}
});

$(document).on('click', function (e) {
    $('[data-toggle="popover"],[data-original-title]').each(function () {
        //the 'is' for buttons that trigger popups
        //the 'has' for icons within a button that triggers a popup
        if (!$(this).is(e.target) && $(this).has(e.target).length === 0 && $('.popover').has(e.target).length === 0) {                
            (($(this).popover('hide').data('bs.popover')||{}).inState||{}).click = false  // fix for BS 3.3.6
        }

    });
});

});