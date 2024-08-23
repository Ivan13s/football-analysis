import sys
sys.path.append('../')
from utils import get_center_of_bounding_box, measure_distance
import numpy as np
import cv2 as cv

#TODO: Implement hysterisis for ball assignment

class PlayerBallAssigner():
    def __init__(self):
        self.max_player_ball_distance = 69
        
    def assign_ball_to_player(self, players, ball_bounding_box):
        ball_position = get_center_of_bounding_box(ball_bounding_box)
        minimum_distance = float('inf')
        assigned_player = -1

        for player_id, player in players.items():
            player_bounding_box = player['bounding_box']            
            player_left_foot_position = (int(player_bounding_box[0]), int(player_bounding_box[3]))
            player_right_foot_position = (int(player_bounding_box[2]), int(player_bounding_box[3]))
            
            distance_pl_left = measure_distance(player_left_foot_position, ball_position)
            distance_pl_right = measure_distance( player_right_foot_position, ball_position)
            distance = min(distance_pl_left, distance_pl_right)           
            
            if distance < self.max_player_ball_distance:
                if distance < minimum_distance:
                    minimum_distance = distance
                    assigned_player = player_id
    
        return assigned_player


