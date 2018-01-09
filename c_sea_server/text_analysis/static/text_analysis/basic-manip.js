current_sentence = null;
selected_word = null;
$(document).ready(function() {

	function reset_inputs() {
		$("#penn-tags").val("none");
		$("#upos-tags").val("none");
	}
	$('input[type=checkbox]').each(function() { this.checked = false; }); 
	$("#dialogue-tag").val("none");
	reset_inputs();


	function to_AJAX(sentence_to_save) {
		var result = {
			url: "/text_analysis/send_JSON",
        	dataType: 'json',

        	data: {
        		"text": $("#text-input").val(),
        		"to_save": JSON.stringify(current_sentence)
        	},
        	
			success: function(data){
				current_sentence = data.current_sentence_info;

				$("#reply-div").html(data.reply);
				$("#text-input").val('');

				refresh_sentence(current_sentence);
			}
		};
		console.log(JSON.stringify(current_sentence));
		return result;
	}
	function refresh_sentence(sent) {
		$("#dialogue-tag").val("none");
		$('input[type=checkbox]').each(function() { this.checked = false; }); 
		reset_inputs();

		var wordDiv = $("#word-div");
		wordDiv.html("");
		for (var i=0; i<sent.tokens.length; i++){
			wordDiv.append("<span class='word clickable', id='word-" + i.toString() + "''>" + sent.tokens[i] + "</span>");
		};

		$(".word").click(function(){
			$(".selected").removeClass("selected");
			$(this).addClass("selected");

			var num = Number($(this).attr('id').slice(-1));
			$("#penn-tags").val(current_sentence["pbank_tags"][num]);
			$("#upos-tags").val(current_sentence["upos_tags"][num]);
			selected_word = [$(this).html(), $(this).attr('id').slice(-1)];
		})
		$("#text-input").val('');
	}

	$("#save").click(function(){
		if (selected_word !== null) {
			var i = Number(selected_word[1])
			current_sentence["pbank_tags"][i] = [selected_word[0], $("#penn-tags").val()];
			current_sentence["upos_tags"][i] = [selected_word[0], $("#upos-tags").val()];
			var checks = $('input[type="checkbox"]');
			var modifiers = "";
			checks.each(function(i, el){
				if ($(el).is(':checked')) {
					modifiers += $(el).val();
				}
			})
			selected_word = null;
		}
		current_sentence["dialogue_tag"] = $("#dialogue-tag").val() + modifiers;
		$(".selected").removeClass("selected");
		reset_inputs();
	});

	var txt = $("#text-input");
	var reply = $("#reply-div");
	txt.on("keydown", function(e) {
		if (e.which === 13) { 
			var to_send = to_AJAX(current_sentence)
			$.ajax(to_send);
		};
	});
});
/*
Example JSON and what everything does (and all the label things I gotta program in)
{
    "conversation_id" : 0
	"sentence_id" : 0
	"speaker_id" : 0,
	"speaker_name": "vivian"
	"text" : "This is a sample sentence.",
	"tokens" : ['This', 'is', 'a', 'sample', 'sentence', '.'],
	"pbank_tags	" : [('This', ''), ('is', ''), ('a', ''), ('sample', ''), ('sentence', ''), ('.', '')],
	"upos_tags" : [('This', ''), ('is', ''), ('a', ''), ('sample', ''), ('sentence', ''), ('.', '')],
	"dialogue_tag" : "",
	"truthfulness" : .5, 
	"is_sarcasm" : 0,
	"sentiment" : "",
}

conversation_id: group all conversations together, I will need that when figuring out how to reply to messages
sentence_id = id of the sentence and its place in the converastion. use convo and sentence id to specify a sentence. 
speaker_id = id of speaker, for future use
speaker_id = name of speaker, for future use

text = recorded text
tokens = tokenized texts
pbank_tags = penn pos tags
upos_tags = universal pos tags
dialogue_tag = SWBD/DAMSL tags

truthfulness = 0 to 1, saving in case it's useful later
is_sarcasm = 0 or 1, saving in case it's useful later
sentiment = -1 to 1, for sentiment analysis
*/