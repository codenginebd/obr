var Pager = {
	create_pages: function(current_page, total_objects, page_size, display_page_count) {
		if(typeof display_page_count == "undefined") {
			display_page_count = 10;
		}
		else {
			display_page_count = parseInt(display_page_count);
		}
		var first_page_start = (current_page - 1) * page_size + 1;
		if(first_page_start > total_objects) {
			return [];
		}
		var last_page_start = first_page_start;
		var pages = [];
		while(last_page_start < total_objects) {
			last_page_start += page_size;
		}
		if(last_page_start > total_objects) {
			last_page_start = last_page_start - page_size;
		}
		var pcount = 0;
		for(var i = first_page_start ; i <= last_page_start ; i += page_size) {
			var page = Math.floor(i / page_size) + 1;
			pages.push(page);
			pcount += 1
			if(pcount >= display_page_count) {
				break;
			}
		}
		return pages;
	 },
	next_page_available: function(page_size, total_objects, current_page) {
		var page_start = (current_page - 1) * page_size + 1;
		var next_page_start = page_start + page_size;
		if(next_page_start <= total_objects) {
			return true;
		}
		return false;
	 },
	prev_page_available: function(page_size, total_objects, current_page) {
		var page_start = (current_page - 1) * page_size + 1;
		var prev_page_start = page_start - page_size;
		if(prev_page_start < 1) {
			return true;
		}
		return false;
	 },
	create_pagination_object: function(total_objects, page_size, current_page, display_page_count) {
		var pages = this.create_pages(current_page, total_objects, page_size, display_page_count);
		var is_next_page_available = this.next_page_available(page_size, total_objects, current_page);
		var is_prev_page_available = this.prev_page_available(page_size, total_objects, current_page);
		var pagination_object = {
			pages: pages,
			prev_page_available: is_prev_page_available,
			next_page_available: is_next_page_available
		}
		return pagination_object;
	}
};