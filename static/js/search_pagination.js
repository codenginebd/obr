(function(){
    var Pager = {
		create_pages: function(current_page, total_objects, page_size, display_page_count) {
			if(typeof display_page_count == "undefined") {
				display_page_count = 10;
			}
			var first_page = (current_page - 1) * page_size + 1;
			if(first_page > total_objects) {
				return [];
			}
			var last_page = first_page;
			var pages = [];
			while(last_page < total_objects) {
				last_page += page_size;
			}
			if(last_page > total_objects) {
				last_page = last_page - page_size;
			}
			for(var i = first_page ; i <= last_page ; i ++) {
				var page = Math.floor(i / page_size) + 1;
				Array.prototype.push.apply(pages, page);
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
			var pagination_object {
				pages: pages,
				prev_page_available: is_prev_page_available,
				next_page_available: is_next_page_available
			};
		};
	 }
})();