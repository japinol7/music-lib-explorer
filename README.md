## Music Library Metadata Explorer
This is a simple Music Library Metadata Explorer.
Its purpose is to be used as a Flask + SQLAlchemy example. 

About the demo data: All the MusicLME demo metadata has been entered <br>
manually over the years as a hobby by the author of MusicLME. 

Starting with version 1.0.3, MusicLME includes a Spotify integration with <br> 
the Spotify REST API that the user can use to get movie data from Spotify.
* Regarding the Spotify integration:
  * This product uses the Spotify API but is not endorsed or certified by Spotify
  * You will need to get a Spotify API access token to use this integration: <br>
    https://developer.spotify.com/documentation/
<br> <br>


### The program 

	Objective: Make a very simple Music Library Metadata Explorer using flask and SQLAlchemy.
    Title: Music Library Metadata Explorer
	program: music-lib-explorer
	version: 1.0.9
	author: Joan A. Pinol
	author_nickname: japinol
	author_gitHub: japinol7
	author_twitter: @japinol
	Python requires: 3.13 or greater.


## Screenshots

<img src="screenshots/screenshot01.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot02.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot03.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot04.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot05.png" alt=""> <br/> <br/>

#### Starting with version 1.0.2 you can export the Music data to Excel

#### Starting with version 1.0.3 you can activate the Spotify integration

When activated, a "Spotify" button will appear in the song and album lists. <br>
This button will open a view with some information about the album and the artist <br>
and links to the album and the artist on Spotify.

<img src="screenshots/screenshot06.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot07.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot08.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot09.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot10.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot11.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot12.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot13.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot14.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot15.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot16.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot17.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot18.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot19.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot20.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot21.png" alt=""> <br/> <br/>
<img src="screenshots/screenshot22.png" alt=""> <br/> <br/>
<br>


**To make this web server app to work in your local environment**

	Do this:
	    1. Clone this repository in your local system.
	    2. Go to its folder in your system.
	    3. $ pip install -r requirements.txt
	    4. $ flask run
	    5. Open the website indicated in the console in your browser.
	       Example: http://127.0.0.1:5000/
	    6. To have some demo data, the first time 
	       you must import the music data into the database:
	       6. 1. Press the [Songs] button
	       6. 2. Press the [Show/Hide Import Form] button
	       6. 3. Press the [Import data] button
	       6. 4. Note: Once the music data is loaded into the database,
	             you do not have to import it again.
 