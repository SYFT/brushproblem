var JQ = $.noConflict();
JQ(document).ready(function() {
	JQ("#my-button-toTop").click(function() {
		JQ(document.body).animate({scrollTop : 0}, 500);
		JQ(window).scrollTo = (0, 0);
	})
	
	JQ("#my-button-toBottom").click(function() {
		JQ(document.body).animate(
			{scrollTop : JQ(document).height() - JQ(window).height()}, 
			500);
		JQ(window).scrollTo = (0, JQ(document).height() - JQ(window).height());
	})
	
	JQ("button[id^='my-button-submit-']").each(function() {
		JQ(this).click(function() {
			prefix = "my-button-submit-";
			formname = this.id.substring(prefix.length);
			JQ("#my-show-problem-form").submit();
		})
	})
	
	var myCheckboxToggle = function(formCheckbox) {
		// alert(formCheckbox);
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
	}
	
	JQ("#my-button-hide-correct").click(function() {
		// var formCheckbox = JQ("#my-hide-correct-checkbox");
		myCheckboxToggle(JQ("#my-hide-correct-checkbox"));
		// if(formCheckbox.is(':checked')) {
			// formCheckbox.prop("checked", false);
			// JQ("[canhide = 'true']").each(function() {
				// JQ(this).css("display", "");
			// })
		// } else {
			// formCheckbox.prop("checked", true);
			// JQ("[canhide = 'true']").each(function() {
				// JQ(this).css("display", "none");
			// })
		// }
	})
	
	
	JQ("#my-hide-correct-checkbox").click(function() {
		myCheckboxToggle(JQ(this));
		myCheckboxToggle(JQ(this));
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
	
	JQ("#my-button-login").click(function() {
		setMaxDigits(512);
		var key = new RSAKeyPair("0x10001", "", "0x813b99a2e3028f253b83f2e2e592eb5aa1d43bc4c03de707608ecd999cae7c8d17c56989b9ef714245012c4a95914e092376217ad0a5279d579c11e8c0f5e56b");
		alert(key.e);
		var pwd = encryptedString(key, JQ("#my-input-password").val());
		JQ("#my-input-password").val(pwd)
		// alert(pwd);
		// return false;
	})
	
	JQ('input, textarea').placeholder();
})