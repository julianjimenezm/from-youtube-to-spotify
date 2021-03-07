
import json
import os
import requests
import urllib.parse  # utilise with urllib.parse chunk

#Google APIs libraries
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import youtube_dl

# Spotify Personal id and token authorization by request
from keys import spotify_user_id, spotify_token



class FromYoutubeToSpotify:

    def __init__(self):
        
        ''' initializing personal info'''
        
        self.youtube = self.main_client()
        self.user_id = spotify_user_id
        self.token = spotify_token
        self.my_dict = {}
        
        
    def main_client(self):
        """ Log Into Youtube client, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        # # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube Main client  
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube

    def fav_videos(self):
        """getting our favorite videos info into a dictionary"""
        
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            maxResults = 30
            myRating="like"
        )
        response = request.execute()

        # getting youtube videos information.
        for item in response["items"]:
            video_title = item["snippet"]["title"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])

            # Youtube_dl connection
            video = youtube_dl.YoutubeDL({"nocheckcertificate" : True}).extract_info(
                youtube_url, download=False)
            song_name = video["track"]
            artist = video["artist"]

            self.my_dict[video_title] = {
                "youtube_url": youtube_url,
                "song_name": song_name,
                "artist": artist,
                "spotify_uri": self.search_songs(song_name, artist)

            }
            
 # Request body implementation from Spotify console and url end-point
    def playlist(self):
        """Creating a Spotify playlist"""
        request_body = json.dumps({
            "name": "My Youtube Liked Videos",
            "description": "julianjimenezm favorites videos",
            "public": True
        })

        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = requests.post(
            
            url,
            data=request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response_json = response.json()

        # playlist id
        return response_json["id"]

 # Searching and matching songs by song_name & artist 
    def search_songs(self, song_name, artist):
        """Spotify search for an item end-point"""
       
        url = f"https://api.spotify.com/v1/search?q={song_name}%20{artist}&type=track%2Cartist&market=US&limit=10&offset=5"
        
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )
        response_json = response.json()
        
        song_id = response_json["tracks"]["items"]
        
        song_uri = song_id[0]["uri"]
        
        return song_uri
######################### urllib.parse code chunck #############################################
    '''
    def search_songs(self,song_name, artist):
        
        query = urllib.parse.quote(f'{song_name} {artist}')
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        
        response = requests.get(
            url,
            headers = {
                
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
                
            }
        )
        
        response_json = response.json()
        
        return  response_json["tracks"]["items"][0]["uri"]
        '''
  #######################################################################################
    
    def add_songs(self):
        """Add our favorites songs into the new spotify playlist """
        self.fav_videos()
        
        # Getting URIs (Spotify Uniform Resources Identifiers)
        URIs = []
        for song, info in self.my_dict.items():
        URIs.append(info["spotify_uri"])
               
        playlist_id = self.playlist()

        # Add all songs into the new playlist
        request_data = json.dumps(URIs)

        url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
            
        response = requests.post(
            url,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
        )

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = FromYoutubeToSpotify()
    cp.add_songs()
