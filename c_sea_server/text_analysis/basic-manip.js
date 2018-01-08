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