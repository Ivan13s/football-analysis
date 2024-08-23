from utils import read_video, save_video
from trackers import Tracker
import cv2 as cv
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
import numpy as np
from camera_movement_estimator import CameraMovementEstimator

from utils.bounding_box_utils import get_center_of_bounding_box, measure_distance
from view_transformer import ViewTransformer
def main(): 
    # Read video
    video_frames=read_video('input_videos/test_video.mp4')
    
    # Tracker initialization
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/track_stubs.pkl')
    
    # Get object positions
    tracker.add_position_to_tracks(tracks)
    
    # Camera movement estimation
    camera_movement_estimator = CameraMovementEstimator(video_frames[0])
    camera_movement_per_frame = camera_movement_estimator.get_camera_movement(video_frames, read_from_stub=True, stub_path='stubs/camera_movement_stubs.pkl')
    
    camera_movement_estimator.add_adjust_positions_to_tracks(tracks, camera_movement_per_frame)

    #View Transformer
    view_transformer=ViewTransformer()
    view_transformer.add_transformed_position_to_tracks(tracks)
    
    ## Save cropped image of players
    # for track_id, player in tracks['players'][0].items():
    #     bounding_box = player['bounding_box']
    #     frame = video_frames[0]
        
    #     #crop bounding_box from frame
    #     cropped_image = frame[int(bounding_box[1]):int(bounding_box[3]), int(bounding_box[0]):int(bounding_box[2])]
    #     cv.imwrite(f'output_videos/player_cropped_image.jpg', cropped_image)
    #     break
    
    
    # Interpolate Ball Positions
    tracks["ball"]=tracker.interpolate_ball_positions(tracks["ball"])
    
    # Assign players teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
     
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            # bounding_box = track['bounding_box']
            team_id = team_assigner.get_player_team(video_frames[frame_num], track['bounding_box'], player_id)
            tracks['players'][frame_num][player_id]['team_id'] = team_id
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team_id]
            
    # Assign Ball Acquisition
    player_assigner = PlayerBallAssigner()
    team_ball_control = []

    for frame_num, player_track in enumerate(tracks['players']):
        ball_bounding_box = tracks['ball'][frame_num][1]['bounding_box']
        assigned_player = player_assigner.assign_ball_to_player(player_track, ball_bounding_box)
        ball_position = get_center_of_bounding_box(ball_bounding_box)
        
        # debugging//
        
        if(assigned_player!=-1):
            player_bounding_box = player_track[assigned_player]['bounding_box']
            
            player_left_foot_position = (int(player_bounding_box[0]), int(player_bounding_box[3]))
            player_right_foot_position = (int(player_bounding_box[2]), int(player_bounding_box[3]))
            # Draw lines from feet to ball
            cv.line(video_frames[frame_num], player_left_foot_position, ball_position, (255, 165, 0), 2)
            cv.line(video_frames[frame_num], player_right_foot_position, ball_position, (200, 174, 204), 2)

        # //debugging
        
                
        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team_id'])
        else:
            if team_ball_control:  # If the list is not empty
                team_ball_control.append(team_ball_control[-1])
            else:  # If the list is empty
                team_ball_control.append(0)  # default value for when the ball is not assigned to any player at the beginning of the video
            
    team_ball_control = np.array(team_ball_control)
    
    print(team_ball_control)
    
    # Draw output
    ## Draw object Tracks
    output_video_frames = tracker.draw_annotations(video_frames,tracks,team_ball_control)

    ## Draw Camera Movement
    output_video_frames = camera_movement_estimator.draw_camera_movement(output_video_frames, camera_movement_per_frame)
    
    #Save video
    save_video(output_video_frames,'output_videos/output_video.avi')
    
if __name__ == '__main__':
    main()

