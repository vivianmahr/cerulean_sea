"""
rough outline of what it should do for the moment
load/initiate emotional state
list of actions

Possible ways of input to make it do things:
django site
email server #not yet

actually not sure if django was such a great idea since it can't actually
receive emails, but I will play with it for a while, at least for generating
tagged corpuses

Right now the only action it can take is to start a chat. 
"""

import emotion
import time
import threading
#from actions import chat #spacy took too long to load for now


class C_Sea():
    def __init__(self):
        # try loading first when option exists
        self.emotion = emotion.Emotional_State()

        self.is_sleeping = False
        self._start_date = time.time()
        self._last_check = self._start_date;
        
        self._start_sleeping_time = 0
        self._sleep_for = 0
        self._shutting_down = False
        self.actions = [] #put all threads here later

    def update(self):
        new_time = time.time()
        dt = new_time - self._last_check
        self._last_check = time.time()
        print(dt)
        if not self.is_sleeping:
            #self.emotion.update(dt)
            pass
        else:
            if time.time() - self._start_sleeping_time >= self._sleep_for:
                self.is_sleeping = False
        threading.Timer(.25, self.update).start()
        self.display_status()
            
    def sleep(self, hours):
        self._start_sleeping_time = time.time()
        self._sleep_for = hours * 60 * 60
        self.is_sleeping = True

    def start(self):
        self.update()

    def display_status(self):
        print(self.is_sleeping)

    def shutdown(self):
        # save states
        # wait for all threads/actions to die
        # return
        self._shutting_down = True
        
        
if __name__ == "__main__":
    c = C_Sea()
    c.sleep(1/(60*60))
    c.start()
