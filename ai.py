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
    
    @staticmethod
    def distance(p1, p2):
        return math.sqrt(math.pow(p1[0]-p2[0], 2) + math.pow(p1[1]-p2[1], 2))
   
    @property
    def velocity(self):
        return (self.previous_target['x']-self.local_player['x'], self.previous_target['y']-self.local_player['y'])

    @property
    def myX(self):
        return self.local_player['x']
    
    @property
    def myY(self):
        return self.local_player['y']

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
            safe_dist = (cell['radius'] - obj['radius'])# TODO
            actual_dist = math.sqrt(math.pow(obj['x']-cell['x'], 2) + math.pow(obj['y']-cell['y'], 2))
            #print('SafeDist: ' + str(safe_dist) + ' ActualDist: ' + str(actual_dist))
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
                print('<AVOIDING OBJ> ' + str(len(self.foods)) + ' foods around. ' + str(vec), end='\r')
                return vec
        if self.foods:
            target_food = self.find_nearest_food()
            target = {'x': target_food['x'], 'y': target_food['y']}
        else:
            target = {'x': 500, 'y': 500}
        
        pX = self.myX
        pY = self.myY
        dist = math.sqrt(math.pow(target['x']-pX, 2) + math.pow(target['y']-pY, 2))
        target.update({
            'x': (target['x'] - pX) ,
            'y': (target['y'] - pY) 
        })

        self.previous_target = target
        print(str(len(self.foods)) + ' foods around. ' + str(target), end='\r')
        return target


class StandardAI(AgarioAI):
    pass


class NaturalAI(AgarioAI):
    def __init__(self):
        self.last_food_target = None
    
    def find_food_with_lock(self):
        if self.last_food_target:
            for cell in self.local_player['cells']:
                if self.distance((cell['x'], cell['y']), self.last_food_target) < cell['radius']:
                    self.last_food_target = None
                    break
        if self.last_food_target:
            return self.last_food_target
        food = self.find_nearest_food()
        self.food_target_lock = True
        self.last_food_target = (food['x'], food['y'])
        return self.last_food_target

    def next_target(self):
        virus_check = self.check_virus()
        for avoid_obj in virus_check:
            need, vec = self.force_avoid_object(avoid_obj)
            if need:
                self.previous_target = vec
                print('<AVOIDING OBJ> ' + str(len(self.foods)) + ' foods around. ' + str(vec), end='\r')
                return vec
        if self.foods:
            target = self.find_food_with_lock()
        else:
            target = {'x': 500, 'y': 500}
        
        pX = self.myX
        pY = self.myY
        target = {
            'x': (target[0] - pX) ,
            'y': (target[1] - pY) 
        }

        self.previous_target = target
        print(str(len(self.foods)) + ' foods around. ' + str(target), end='\r')
        return target