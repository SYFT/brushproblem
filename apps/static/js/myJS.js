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
		JQ.getJSON($SCRIPT_ROOT + '_return_public', {
			now: new Date()
		}, function(data) {
			// alert(data.publicKey);
			tmp = data.publicKey.split(" ");
			exponent = tmp[0];
			mod = tmp[1];
			// alert(exponent);
			// alert(mod);
			// alert(exponent);
			// alert(mod);
			pwd = JQ("#my-input-password").val();
			if(pwd.length > 6) pwd = pwd.substring(0, 6);
			// alert(pwd);
			setMaxDigits(1024);
			message = biFromDecimal(pwd);
			tmp = biToString(message, 10);
			// alert(tmp);
			exponent = biFromDecimal(exponent);
			mod = biFromDecimal(mod);
			pwd = biPowMod(message, exponent, mod);
			pwd = biToString(pwd, 10);
			// alert('pwd:'+ pwd);
			JQ("#my-input-password").val(pwd);
			// return false;
			// alert('new pwd:' + JQ("#my-input-password").val());
			JQ("#my-form-login").submit();
		})
		return false;
	})
	
	JQ('input, textarea').placeholder();
})