from gtts import gTTS


def make_audio_files(texts_to_read):
    for text in texts_to_read:
        audio = gTTS(text=text, lang="en", slow=False)

        audio.save(f"audio/audio-{texts_to_read.index(text)}")
