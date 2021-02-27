# from-youtube-to-spotify

# SETUP

1. Config YouTube data API:

    - Activate YouTube data API (v3) from your google account.
     Google for developpers / API Services > Create a new project 

   - Create your own credentials, for this case we need a request credential (Aouth 2.0 ID client)
     got your app desktop credential > download your own client_secret.json file.
    
2.  Getting your client connection:

     - Go to > use cases and got snippets > resource-videos > method-list > list my_liked_videos > Python Tab.
     - (https://developers.google.com/youtube/v3/code_samples/code_snippets?apix=true) and search Python tab.
       
  
     - Now you got your client connection code.


3.  Spotify Configuration:

     - From your account get your personal user_id.
     - From the spotify developpers console > Search > search for an item > get your end-point and token
     - (https://developer.spotify.com/console/) 
       
     - Save those personals identifiers into the Keys.py file.
 
     - To create our playlist we go to the API Reference > Create a playlist and get the 'end-point' and the 'Request-Body'



4.  The Google data credentials doesn't expires, but Spotify token does it every hour.
