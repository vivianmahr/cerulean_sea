from actions.text_processing.token_taggers import tokenizer, tagger

DIMENSIONS = ["task"]

class Dialogue_Tagger():
    def __init__(self):
        self._decision_tree = {
            "auto_feedback" : ["auto_positive", "auto_negative"],
            "allo_feedback" : ["allo_positive", "allo_negative", "feedback_elicitation"],
            "turn_management" : ["turn_take", "turn_grab", "turn_accept", "turn_release", "turn_assign", "turn_keep"],
            "time_management" : ["stall", "pause"],
            "discourse_structuring" : ["topic_shift", "opening", "interaction_structuring"],
            "own_communication_management" : ["repair", "retraction"],
            "partner_communication_management": ["completion", "correct_misspeaking"],
            "social_obligations_manager" : ["initial_greeting", "return_greeting", "apology", "accept_apology", "initial_self_introduction", "return_self_introduction", "thanking", "accept_thanking", "initial_goodbye", "return_goodbye", "congratulations", "accept_congratulations", "condolence", "accept_condolence", "compliment", "accept_compliment"],
            "task": {
                "question" : {
                    "propositional_question" : ["check_question"],          
                    "choice_question" : [],
                    "set_question": []
                    },
                "inform" : {
                    "answer" : ["confirm", "disconfirm"],
                    "agreement" : [],
                    "disagreement" : ["correction"]
                    },
                "offer" : {
                    "promise" : {
                            "address_request" : ["accept_request", "decline_request"],
                        }
                },
                "request" : {
                    "instruct" : {
                            "address_offer" : ["accept_offer", "decline_offer"],
                        }
                }
                
            }
        }
        
        def tag_sentence(self, previous_sentence_tag, sentence):
            pass
            """
                NN location should be a concatenation of all the branches
                result is one of its outcomes, or 0 for "hey stay here, it can't get any more specific"
                
            """
            

"""
things damsl includes that don't seem to be clearly expressed in Diaml
open-ended and rhetorical questions and answers

tangents/unrelated responses
"""

class Dialogue_Act():
    def __init__(self, text, speaker, addressee):
        """For now, a dialogue act is a sentence - I'm not sure how to handle the idea of dialogue 
            acts that encompass more than one sentence, or sentences with dialogue acts b/c I'm not 
            that good at dialogue act division."""
        self.text = ""
        self.tokens = []
        self._tagged_tokens = False
        self._structure = []
        # For now, assuming one on one conversations
        self.speaker = speaker 
        self.addressee = addressee
        self.dimensions = [] # where the tags are
        
        
        