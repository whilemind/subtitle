# SubTitle

## Require packages

### To split the background music and voice from a single voice file.
$ pip install spleeter

### To detect the speech.
$ pip install SpeechRecognition

### Google api client
$ pip install google-api-python-client

### FFMPEG for MacOS
$ brew install ffmpeg

## Necessary Commands
### separate voice file from video file
$ ffmpeg -i input.mp4 output.mp3

### split music file.
$ spleeter separate -i current.wav -p spleeter:2stems -o output

## Run the program.
$ python

## Process to generate the subtitles.
1. source *.mp4 video file.
2. separate voice *.wav file from *.mp4.
3. separate the background music and voice into two different file from *.wav file.
4. slice the *.wav voice file by detecting silence.
5. now use the google vocie to text engine to translate sliced voice file to text file.

We will need a movie *.mp4 file which subtitle will be generated automatically. At first the sound file need to be seperated from the video file for that we will use the following command:
$ python recognizer.py -video ../Ertuğrul/Ertugrul-147.mp4
