from utils import read_video, save_video
from trackers import Tracker
import cv2 as cv
from team_assigner import TeamAssigner


def main(): 
    # Read video
    video_frames=read_video('input_videos/test_video.mp4')
    
    
    tracker = Tracker('models/best.pt')
    tracks = tracker.get_object_tracks(video_frames, read_from_stub=True, stub_path='stubs/track_stubs.pkl')
    
    # # Save video
    # save_video(video_frames,'output_videos/output_video.avi')
    
    # # Save cropped image of players
    # for track_id, player in tracks['players'][0].items():
    #     bounding_box = player['bounding_box']
    #     frame = video_frames[0]
        
    #     #crop bounding_box from frame
    #     cropped_image = frame[int(bounding_box[1]):int(bounding_box[3]), int(bounding_box[0]):int(bounding_box[2])]
    #     cv.imwrite(f'output_videos/player_cropped_image.jpg', cropped_image)
    #     break
    
    
    # Assign players teams
    team_assigner = TeamAssigner()
    team_assigner.assign_team_color(video_frames[0], tracks['players'][0])
    
    for frame_num, player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            # bounding_box = track['bounding_box']
            team_id = team_assigner.get_player_team(video_frames[frame_num], track['bounding_box'], player_id)
            tracks['players'][frame_num][player_id]['team_id'] = team_id
            tracks['players'][frame_num][player_id]['team_color'] = team_assigner.team_colors[team_id]
            
            
            
    # Draw output
    ## Draw object Tracks
    output_video_frames=tracker.draw_annotations(video_frames,tracks)

    save_video(output_video_frames, 'output_videos/output_video.avi')

if __name__ == '__main__':
    main()

