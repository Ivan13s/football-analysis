from sklearn.cluster import KMeans

class TeamAssigner:
    def __init__(self):
        self.team_colors = {}
        self.player_team_dict = {}
    
    def get_clustering_model(self, image):
        image_2d = image.reshape(-1,3)
        
        kmeans = KMeans(n_clusters=2, init='k-means++', n_init=1)
        kmeans.fit(image_2d)
        return kmeans
    
    def get_player_color(self, frame, bounding_box):
        image = frame [int(bounding_box[1]):int(bounding_box[3]), int(bounding_box[0]):int(bounding_box[2])]
        top_half = image[0:int(image.shape[0]/2), :]
        kmeans = self.get_clustering_model(top_half)
        
        # Get the cluster labels for each of the pixels
        labels = kmeans.labels_
        
        # Reshape the labels to the image shape
        clustered_image = labels.reshape(top_half.shape[0], top_half.shape[1])

        # Get player cluster
        corner_clusters = [clustered_image[0,0], clustered_image[0,-1], clustered_image[-1,0], clustered_image[-1,-1]]
        non_player_cluster = max(set(corner_clusters), key=corner_clusters.count)
        player_cluster = 1 - non_player_cluster
        
        player_color = kmeans.cluster_centers_[player_cluster]
        
        return player_color
        
        
    
    def assign_team_color(self,frame,player_detections):
        player_colors = []
        for _, player_detections in player_detections.items():
            bounding_box = player_detections['bounding_box']
            player_color= self.get_player_color(frame,bounding_box)
            player_colors.append(player_color)
        
        kmeans = KMeans(n_clusters=2, init='k-means++', n_init=10)
        kmeans.fit(player_colors)
        
        self.kmeans = kmeans
        
        self.team_colors[1] = kmeans.cluster_centers_[0]
        self.team_colors[2] = kmeans.cluster_centers_[1]    
            
    
    def get_player_team(self, frame, player_bounding_box, player_id):
        if (player_id) in self.player_team_dict:
            return self.player_team_dict[player_id]
        
        player_color = self.get_player_color(frame, player_bounding_box)
        team_id = self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id += 1
        
        if player_id==91:
            team_id=1
        self.player_team_dict[player_id] = team_id
        
        return team_id
         