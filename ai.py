import sys
import math
import numpy as np


class AgarioAI:
    def __init__(self):
        self.local_player = {'x': 0, 'y': 0}
        self.other_players = {}
        self.foods = []
        self.virus = {}
        self.previous_target = {'x': 0, 'y': 0}
   
    @property
    def velocity(self):
        return (self.previous_target['x']-self.local_player['x'], self.previous_target['y']-self.local_player['y'])

    def find_nearest_food(self):
        pX = self.local_player['x']
        pY = self.local_player['y']
        minDist = sys.maxsize
        minFood = None
        for food in self.foods:
            dist = math.sqrt(math.pow(food['x']-pX, 2) + math.pow(food['y']-pY, 2))

            if dist < minDist:
                minDist = dist
                minFood = food
        return food

    def find_food_natural(self):
        """
        Find the food in the same direction  as velocity
        """
        velocity = np.array(self.velocity)
        minRad = sys.maxsize
        minFood= None
        for food in self.foods:
            target_vec = np.array([food['x']-self.local_player['x'], food['y']-self.local_player['y']])
            prod = np.dot(target_vec, velocity)
            rad  = prod / (np.linalg.norm(velocity) * np.linalg.norm(target_vec))
            if rad < minRad:
                minRad = rad
                minFood = food
        return food

    def check_virus(self):
        should_avoid = []
        for virus in self.virus:
            for cell in self.local_player['cells']:
                if cell['radius'] >= virus['radius']:
                    should_avoid.append(virus)
            continue
        return should_avoid

    def force_avoid_object(self, obj):
        avoid_vec = np.array([0.0,0.0])
        need_avoid = False
        for cell in self.local_player['cells']:
            safe_dist = (obj['radius'] + cell['radius']) * 2 # TODO
            actual_dist = math.sqrt(math.pow(obj['x']-cell['x'], 2) + math.pow(obj['y']-cell['y'], 2))
            print('SafeDist: ' + str(safe_dist) + ' ActualDist: ' + str(actual_dist))
            if actual_dist < safe_dist:
                need_avoid = True
                avoid_vec += np.array([cell['x']-obj['x'], cell['y']-obj['y']])
        return need_avoid, {'x': avoid_vec[0], 'y': avoid_vec[1]}

    def next_target(self):
        virus_check = self.check_virus()
        for avoid_obj in virus_check:
            need, vec = self.force_avoid_object(avoid_obj)
            if need:
                self.previous_target = vec
                print('<AVOIDING OBJ> ' + str(len(self.foods)) + ' foods around. ' + str(target), end='\r')
                return vec
        if self.foods:
            target_food = self.find_food_natural()
            target = {'x': target_food['x'], 'y': target_food['y']}
        else:
            target = {'x': 0, 'y': 0}
        
        pX = self.local_player['x']
        pY = self.local_player['y']
        dist = math.sqrt(math.pow(target['x']-pX, 2) + math.pow(target['y']-pY, 2))
        target.update({
            'x': (target['x'] - pX) ,
            'y': (target['y'] - pY) 
        })

        self.previous_target = target
        print(str(len(self.foods)) + ' foods around. ' + str(target), end='\r')
        return target
