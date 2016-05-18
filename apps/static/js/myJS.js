var JQ = $.noConflict();
JQ(document).ready(function() {
	JQ("#my-button-toTop").click(function() {
		JQ(document.body).animate({scrollTop : 0}, 500);
	})
	
	JQ("#my-button-toBottom").click(function() {
		JQ(document.body).animate(
			{scrollTop : JQ(document).height() - JQ(window).height()}, 
			500);
	})
	
	JQ("button[id^='my-button-submit-']").each(function() {
		JQ(this).click(function() {
			prefix = "my-submit-";
			formname = this.id.substring(prefix.length);
			JQ("#my-problem-form").submit();
		})
	})
	
	JQ("#my-button-hide-correct").click(function() {
		var formCheckbox = JQ("#my-hide-correct-checkbox");
		if(formCheckbox.is(':checked')) {
			formCheckbox.prop("checked", false);
			JQ("[canhide = 'true']").each(function() {
				this.style.display = "";
			})
		} else {
			formCheckbox.prop("checked", true);
			JQ("[canhide = 'true']").each(function() {
				this.style.display = "none";
			})
		}
	})
	
	JQ('input, textarea').placeholder();
})