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
	
	JQ("#my-problem-form").submit(function() {
	})
	
	JQ("button[id^='my-button-submit-']").each(function() {
		JQ(this).click(function() {
			prefix = "my-button-submit-";
			formname = this.id.substring(prefix.length);
			JQ("#my-problem-form").submit();
		})
	})
	
	JQ("#my-button-hide-correct").click(function() {
		var formCheckbox = JQ("#my-hide-correct-checkbox");
		if(formCheckbox.is(':checked')) {
			formCheckbox.prop("checked", false);
			JQ("[canhide = 'true']").each(function() {
				JQ(this).css("display", "");
			})
		} else {
			formCheckbox.prop("checked", true);
			JQ("[canhide = 'true']").each(function() {
				JQ(this).css("display", "none");
			})
		}
	})
	
	JQ("#my-problem-form").submit(function() {
		var tmp = JQ("#my-problem-answer");
		if(tmp.css("display") === "none")
			tmp.val("");
	})
	
	JQ("#my-button-problem-type-1").click(function() {
		JQ("#my-problem-answer").css("display", "none");
	})
	
	JQ("#my-button-problem-type-2").click(function() {
		JQ("#my-problem-answer").css("display", "");
	})
	
	JQ('input, textarea').placeholder();
})