## youtubeDownloader

#### Python Flask web app for downloading video/audio-only files
#### 

#### App functions:
- download Youtube videos
- cut and download chosen segments of Youtube videos
- cut and download audio of Youtube videos

Usage: enter Youtube video link in link text field,
use audio-only checkbox and video segment timestamps field to adjust
download preferences.

* timestamps format: 00:00 00:00 for start and end of video segment, minutes:seconds
* multiple timestamps can be entered for the same video at once, separated by ' ' space

App is built with Python and Flask framework, pytube library for connecting to Youtube; 
ffmpeg and pydub for video/audio file handling


#### Installation

Install dependencies
> -m pip install -r requirements.txt

#### Starting the app

> python main.py


**Note:** video and audio cut functions require **ffmpeg** and **ffprobe** installed and available in system PATH


---

This project serves for personal informational purposes and is not affiliated with Youtube  
All video and audio rights belong to video owners/authors.
