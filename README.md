# Spotify Ad Blocker
 A simple productivity script to "Block" ads on spotify for Desktop
 
 
 As a student I don't really have the money to purchase spotify premium so I made this script. When the spotify desktop client (Win10) is relaunched, the status of the ad is reset and it goes back to music. There are some cosmetic issues (Like the spotify icon glowing orange in the task bar when reopened) that will I will likely soon fix. 
 
 To download do git clone https://github.com/marvic2409/Spotify-Ad-Blocker in cmd. Then use pip3 install -r requirements.txt in the directory of the script. 
 
 To setup go to https://developer.spotify.com/ and create a developer account. Create a new app and set the callback URI to http://localhost:8080/callback. Put your client id and client secret in the script as well with your spotify username. Upon the first launch the script will open the spotify link to get permissions to view what song is playing (To know when there is an ad) and will then start running. Currently only work when the desktop client on your account is playing. 
