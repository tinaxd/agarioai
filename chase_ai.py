from ai import AgarioAI
import random


class ChaserAI(AgarioAI):
    def __init__(self, chase_after):
        super().__init__()
        self.chase_after = chase_after
        self.in_random = False
        self.last_random = ()
    
    def get_chase_cord(self):
        for player in self.other_players:
            if player['name'] == self.chase_after:
                return (player['x'], player['y'])
        return None
    
    def random_search(self):
        tX = random.randrange(4000)
        tY = random.randrange(4000)
        return (tX, tY)
    
    def check_random_target_reach(self):
        return abs(self.last_random[0] - self.myX) < 2 \
               and abs(self.last_random[1] - self.myY) < 2
 
    def next_target(self):
        chase = self.get_chase_cord()
        if not chase:
            if self.in_random:
                if self.check_random_target_reach():
                    self.last_random = self.random_search()
            else:
                self.last_random = self.random_search()
                self.in_random = True
            return {
                'x': self.last_random[0]-self.myX,
                'y': self.last_random[1]-self.myY
            }
        else:
            self.in_random = False
            return {
                'x': chase[0] - self.myX,
                'y': chase[1] - self.myY
            }