// Empty JS for your own code to be here

$(document).ready(function(){
	//just test for delete
	$('.page_queue_list').on('click', '.action_delete', function(e){
		$(this).closest('.item').remove();	//disable #
		e.preventDefault();
	});
	
	//just test for add
	$('.page_queue_list').on('click', '.action_tag', function(e){
		$(".page_queue_list").prepend($(this).closest('.item').prop("outerHTML"));
		e.preventDefault();			//disable #
	});
	
});