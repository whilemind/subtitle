# Import the AudioSegment class for processing audio and the 
# split_on_silence function for separating out silent chunks.
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_nonsilent
from pydub.playback import play
import pysrt
import math

import time
import os
import scipy.io.wavfile as wavfile
import numpy as np
import speech_recognition as sr
import librosa

# Define a function to normalize a chunk to a target amplitude.
def match_target_amplitude(aChunk, target_dBFS):
    ''' Normalize given audio chunk '''
    change_in_dBFS = target_dBFS - aChunk.dBFS
    return aChunk.apply_gain(change_in_dBFS)

def get_timestamp(duration):
    hr = math.floor(duration / 3600000)
    total_min = duration % 3600000
    
    mins = math.floor(total_min / 60000)
    total_secs = total_min % 60000

    secs = math.floor(total_secs / 1000)
    milisecs = total_min % 1000

    return "{:02d}:{:02d}:{:02d},{:03d}".format(hr, mins, secs, milisecs)

def recognize(wav_filename):
    data, s = librosa.load(wav_filename)
    librosa.output.write_wav('tmp.wav', data, s)
    y = (np.iinfo(np.int32).max * (data/np.abs(data).max())).astype(np.int32)
    wavfile.write('tmp_32.wav', s, y)

    r = sr.Recognizer()
    with sr.AudioFile('tmp_32.wav') as source:
        audio = r.record(source)  

    print('audiofile loaded')

    try:
        result = r.recognize_google(audio, language = 'tr').lower()
    except sr.UnknownValueError:
        print("cannot understand audio")
        result = ''
        os.remove(wav_filename)  
    # with open('result.txt', 'a', encoding='utf-8') as f:
    #     f.write(' {}\n'.format(result))
    return result

srt_file = pysrt.SubRipFile()

# Load your audio.
print("loading wav file...")
# song = AudioSegment.from_mp3("your_audio.mp3")
#song = AudioSegment.from_wav("vocals.wav")
song = AudioSegment.from_file("vocals.wav", format="wav")
# play(song)
dBFS = song.dBFS


# Nonsilence track start and end positions.
nonsilence = detect_nonsilent(
    song,
    min_silence_len = 500,
    silence_thresh = dBFS-16
)
print("array {}\nNonsilence chunk length {}".format(nonsilence, str(len(nonsilence))))

# for [start, end] in nonsilence:
#     print("start: {0} end: {1}".format(get_timestamp(start), get_timestamp(end)))

# Split track where the silence is 2 seconds or more and get chunks using 
# the imported function.
print("Start spliting file...")
chunks = split_on_silence(
    song, 
    min_silence_len = 500,
    silence_thresh = dBFS-16,
    # optional
    keep_silence = 250
)

print("Spliting done..." + str(len(chunks)))
# Process each chunk with your parameters
for i, chunk in enumerate(chunks):
    # Create a silence chunk that's 0.5 seconds (or 500 ms) long for padding.
#    silence_chunk = AudioSegment.silent(duration=500)

    # Add the padding chunk to beginning and end of the entire chunk.
#    audio_chunk = silence_chunk + chunk + silence_chunk
    audio_chunk = chunk

    # Normalize the entire chunk.
    normalized_chunk = match_target_amplitude(audio_chunk, -20.0)

    # Export the audio chunk with new bitrate.
    starttime = nonsilence[i][0]
    endtime = nonsilence[i][1]
    print("Exporting chunk{0}.wav start: {1} end: {2}".format(i, starttime, endtime))

    chunk_file_path = "ertu2/chunk{0}.wav".format(i)
    normalized_chunk.export(
        chunk_file_path,
        bitrate = "192k",
        format = "wav"
    )
    
    time.sleep(2)
    print("Going to generete the dialogs of file {}".format(chunk_file_path))
    dialogs = recognize(chunk_file_path)
    print("{} file dialog is: {}".format(chunk_file_path, dialogs))
    
    start_time = get_timestamp(starttime)
    end_time = get_timestamp(endtime)
    sub = pysrt.SubRipItem((i+1), start=start_time, end=end_time, text="{} {}".format(str(i+1), dialogs))
    srt_file.append(sub)

srt_file.save("vocals.srt")