from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
import sys
sys.path.insert(0, '../AI/actions/')
import chat

c_manager = chat.Conversation_Manager(convo_dir='../AI/actions/conversations')
current_sentence = 0
sentence_counter = 0
# Create your views here.

def index(request):
    context = {}
    return render(request, 'text_analysis/index.html', context)

def send_JSON(request):
	# Read the sentence sent. There will always be one unless it is QUIT
	text = request.GET.get("text", None)
	global current_sentence, sentence_counter
	# If the conversation hasn't stopped
	if not c_manager.shut_down and text != "QUIT":
		to_fix = json.loads(request.GET.get("to_save", None))

		if to_fix != None:
			current_sentence.dialogue_tag = to_fix['dialogue_tag']
			current_sentence.pbank_tags = [tuple(t) for t in to_fix['pbank_tags']]
			current_sentence.upos_tags = [tuple(t) for t in to_fix['upos_tags']]
			c_manager.add_sentence(current_sentence)
		
		current_sentence = chat.Sentence(text, sentence_counter, 1, c_manager.conversation_id, "vivian", "")
		sentence_counter += 1;
	elif text == "QUIT":
		c_manager.add_sentence(current_sentence)
		c_manager.quit()
		return JsonResponse({"reply" : "Goodbye!"})
	else:
		#c_manager has shut down and I gotta restart the server
		return JsonResponse({"reply" : "Please restart..."})



	data = {
		"current_sentence_info": {
			"conversation_id" : current_sentence.conversation_id,
			"sentence_id" : current_sentence.sentence_id,
			"speaker_id" : 0,
			"speaker_name": "vivian",
			"text" : current_sentence.text,
			"tokens" : current_sentence.tokens,
			"pbank_tags" : current_sentence.pbank_tags,
			"upos_tags" : current_sentence.upos_tags,
			"dialogue_tag" : current_sentence.dialogue_tag
		},
		"reply" : c_manager.generate_output(text)
	}

	return JsonResponse(data)
