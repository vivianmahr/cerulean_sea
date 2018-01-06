$(document).ready(function() {
	var txt = $("#text-input");
	var reply = $("#reply-div");
	
	txt.on("keydown", function(e) {
		if (e.which === 13) { 
			var text = txt.val();
			var textFragments = text.split(" ");
			var wordDiv = $("#word-div")
			for (var i=0; i<textFragments.length; i++)	{
				wordDiv.append("<span class='word'>" + textFragments[i] + "</span>");
			}
			wordDiv.append("<div class='clearer'></div>");
			txt.val("");
		}	
	});
	reply.append("<p>I haven't figured out what to say yet.</p>")
	var temp = function(f) {
		text = f;
		var textFragments = text.split(" ");
		var wordDiv = $("#word-div")
		for (var i=0; i<textFragments.length; i++)	{
			wordDiv.append("<span class='word'>" + textFragments[i] + "</span>");
		}
	}
	temp("Yet again I plugged up my ears against a repeating, reused song.");
});
