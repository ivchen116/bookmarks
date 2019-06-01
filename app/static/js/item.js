var items_per_page = 10;
var items_have_get = 0;
var items_is_loading = false;
var items_has_more = true;
var items_load_fiter = 'queue'
var items_load_collection = []

function itemLoadPara(filter, collection) {
	items_load_fiter = filter;
	items_load_collection = collection;
}
function itemLoadMore() {
	itemLoadSpec(items_have_get, items_per_page, 'queue', '')
}
function itemBuildNew(item) {
	var html_template = '<div class="item item_type_normal"><div class="item_content"><a class="item_link start_articleview" href="#" target="_blank"/><a class="title" href="#"> </a><span class="thumb"> </span><ul class="sub clearfix"><li class="original_url_container"><a class="original_url" href="#" target="_blank"> </a></li></ul><div class="clear"/><ul class="buttons"></ul></div></div>';
	var $item = $(html_template)
	$item.attr('id', item.itemid);
	$item.find('.item_link').attr("href", item.given_url);

	var dis_title = item.given_title?item.given_title:item.resolved_title;
	dis_title = dis_title?dis_title:item.given_url;
	$item.find('.title').text(dis_title).attr("href", item.given_url);
	$item.find('.thumb').css("background-image","url(/static/image/direct.jpg)");
	$item.find('.original_url').text(item.netloc).attr("href", item.given_url);
	
	var $buttons = $item.find('.buttons')
	if (item.archived) {
		$buttons.append(
				$('<li><a href="#">标记为未读</a></li>')
					.addClass('action_mark action_mark_archived')
					.attr('title', '标记为未读'));
	} else {
		$buttons.append(
			$('<li><a href="#">已读</a></li>')
				.addClass('action_mark')
				.attr('title', '已读'));
	}
	$buttons.append(
			$('<li><a href="#" data-toggle="delete-confirmation">删除</a></li>')
				.addClass('action_delete')
				.attr('title', '删除'));
	$buttons.append(
			$('<li><a href="#">添加收藏夹</a></li>')
				.addClass('action_tag')
				.attr('title', '添加收藏夹'));
	$buttons.append(
			$('<li><a href="#">标记为精华</a></li>')
				.addClass(item.favorite?'action_favorite selected':'action_favorite')
				.attr('title', '标记为精华'));

	return $item;
}
function itemLoadSpec(offset, count, state, collection) {
	items_is_loading = true;
	$("#btn-loading").attr("disabled","disabled");
	$("#btn-loading").text("加载中...");
	$.ajax({    
		url: "/item/get",    
		dataType: "json", 
		data: { offset: offset, count: count, state: items_load_fiter, collection: items_load_collection },        
		type: "POST",    
		success: function(data) {
			if (data.status == '1') {
				$.each(data.lists, function(i, item) {
					$(".page_queue_list").append(itemBuildNew(item));
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

$(document).ready(function(){
	
	$('.page_queue_list').on('click', '.action_mark a', function(e){
		var item = $(this).closest('.item')
		var archive = $(this).parent('.action_mark_archived').length>0?0:1;
		
		$.ajax({    
			url: "/item/archive",    
			dataType: "json", 
			data: { id: item.attr("id"), done: archive },        
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
	
	$('.page_queue_list').on('click', '.action_favorite a', function(e){
		var item = $(this).closest('.item')
		var favorite = $(this).parent('.selected').length>0?0:1;
		
		$.ajax({    
			url: "/item/favorite",    
			dataType: "json", 
			data: { id: item.attr("id"), favorite: favorite },        
			type: "POST",    
			context: item,
			success: function(data) {
				if (data.status == '1') {
					$(this).find('.action_favorite').toggleClass('selected');
					if (items_load_fiter == 'favorite' && !$(this).find('.action_favorite').hasClass('selected')) {
						$(this).remove();
					}
				}
			}, 
			error: function() {        
				
			}
		});	
		
		e.preventDefault();
	});
	
	$(window).scroll(function () {
		if ($(window).scrollTop() + $(window).height() == $(document).height()) { 
			if (items_is_loading==false&&items_has_more)
			{
				itemLoadMore();
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





});