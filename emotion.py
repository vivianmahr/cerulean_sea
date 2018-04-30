"""
The painful class that means I will probably have to write everything from scratch.
Emotional_State should influence everything that the AI does.

unused atm
"""

import math, random

class Emotional_State():
    def __init__(self):
        # This is incredibly inefficient, but right now I need readability as
        # I have no idea how half of this will possibly work
        # Each variable has a list of things it influences
        # The implementation of the effects are not in this class 

        self.social_fulfillment = 0;
        # -1 is loneliness, 0 is neutral, 1 is well-satisfied
        # Learning rate                  [ ] - decreases too if too low
        # Likelihood to initiate contact [ ] - increases if too low 
        
    def update(self, time_ms):
        """Gradual decay or increase in certain emotions"""
        self._update_social_implementation(time_ms)
        
    def ms_to_days(self, ms):
        """Converts ms to days"""
        return ms / 8640000
    
    def ms_to_hours(self, ms):
        """Converts ms to hours"""
        return ms / 360000

    def ms_to_minutes(self, ms):
        """Converts ms to minutes"""
        return ms / 6000

    def ms_to_seconds(self, ms):
        """Converts ms to seconds"""
        return ms / 1000

    def _social_sigmoid(self, x):
        """Reference sigmoid for social fulfillment"""
        return 2/(1+math.e**(-x))-1
    
    def _der_social_sigmoid(self):
        """Reference derivative sigmoid for social fulfillment"""
        return 2 * self._social_sigmoid(x) * (2 - self._social_sigmoid(x))
    
    def _update_social_implementation(self, dt):
        # basic sigmoid function - 14ish days to hit high levels of isolation from peak
        # /10 is for scaling
        dt = self.ms_to_days(dt) / 10
        
        # nudges it up so this can be used
        # the function's range is 0-2 but we want -1 to 1 so bump it up hre
        y = self.social_fulfillment + 1

        # dy should always be negative
        # things get more lonely over time without intervention
        dy = 2 * y * (2 - y) * dt
        self.social_fulfillment -= dy
        
        # This should only kick in if there's a monstrous amount of lagging and it can't update for a while
        # Mathematically, derivative changes will just be completely off if dt is too large 
        if self.social_fulfillment <= -1:
            self.social_fulfillment = -.999
        if self.social_fulfillment >= 1:
            self.social_fulfillment = .999
        
    def get_matrix(self):
        """The part of the emotional matrix other functions use
           Returns a 1d matrix, that for a long while, will be only one thing
        """
        return [social_fulfillment]


if __name__ == "__main__":
    day = 8640000
    hour = 360000
    minute = 6000
    second = 1000

    # social fulfillment tests
    def print_x_days(days):
        e = Emotional_State()
        e.social_fulfillment = 0.9
        step = 100
        for i in range(0, day*days, step):
            e.update(step)
            if i%(hour) == 0:
                print("Hour: {:2}, {}".format(int(i/hour), e.social_fulfillment))
                
