import os
from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    ImageClip,
    CompositeAudioClip,
    CompositeVideoClip,
)
from random import choice

# Get background video files
base_videos = os.listdir('videos/bases/')

# This should change according to your background video resolution
RESIZE_FACTOR = 0.7

def make_video(filename):
    times = []

    # Create final audio track by joining every audio
    audioclips = []
    cur_time = 0

    files = os.listdir("audio")
    files.sort()
    for file in files:
        audioclip = AudioFileClip(f"audio/{file}")
        audioclip = audioclip.set_start(cur_time)
        audioclip = audioclip.set_end(cur_time + audioclip.duration)

        cur_time = cur_time + audioclip.duration + 1

        times.append(cur_time)
        audioclips.append(audioclip)

    audioclips = audioclips[::-1]
    final_audioclip = CompositeAudioClip(audioclips).set_fps(44100)

    # Create Image Tracks according to the corresponding audio duration
    time_index = 0
    image_clips = []
    files = os.listdir("screenshots")
    files.sort()
    for file in files:
        imageclip = ImageClip(f"screenshots/{file}")

        if time_index != 0:
            imageclip = imageclip.set_start(times[time_index - 1])
        else:
            imageclip = imageclip.set_start(0)

        imageclip = imageclip.set_end(times[time_index])

        image_clips.append(imageclip)
        time_index += 1

    imageclip = CompositeVideoClip(image_clips)
    imageclip = imageclip.set_position("center")
    imageclip = imageclip.resize(RESIZE_FACTOR)
    imageclip.set_duration(audioclip.duration)

    videoclip = VideoFileClip(f"videos/bases/{choice(base_videos)}")
    videoclip = videoclip.subclip(0, final_audioclip.duration)
    videoclip.audio = final_audioclip

    final = CompositeVideoClip([videoclip, imageclip])
    final.set_duration(final_audioclip.duration)
    final.write_videofile(f"videos/{filename}.mp4", threads=3)
