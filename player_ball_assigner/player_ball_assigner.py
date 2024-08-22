import sys
sys.path.append('../')
from utils import get_center_of_bounding_box, measure_distance
import numpy as np
import cv2 as cv

#TODO: Implemente hysterisis for ball assignment

class PlayerBallAssigner():
    def __init__(self):
        self.max_player_ball_distance = 117
        
    def assign_ball_to_player(self, players, ball_bounding_box):
        ball_position = get_center_of_bounding_box(ball_bounding_box)
        minimum_distance = float('inf')
        assigned_player = -1

        for player_id, player in players.items():
            player_bounding_box = player['bounding_box']
            player_center = get_center_of_bounding_box(player_bounding_box)
            
            distance = measure_distance(player_center, ball_position)
            distance_pl_left = measure_distance([player_bounding_box[0], player_bounding_box[-1]], ball_position)
            distance_pl_right = measure_distance([player_bounding_box[2], player_bounding_box[-1]], ball_position)
            # distance = min(distance_pl_left, distance_pl_right)           
            
            print(f"Player {player_id} center: {player_center}, Center_d: {distance} Left_d: {distance_pl_left} Right_d: {distance_pl_right}")
            
            if distance < self.max_player_ball_distance:
                if distance < minimum_distance:
                    minimum_distance = distance
                    assigned_player = player_id

        if assigned_player != -1:
            print(f"Ball assigned to player {assigned_player} at distance {minimum_distance} Left_d: {distance_pl_left} Right_d: {distance_pl_right}")
        else:
            print("Ball not assigned to any player")

        return assigned_player


