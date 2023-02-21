import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

load_dotenv()

speech_key = os.getenv('SPEECH_KEY')
service_region = os.getenv('SERVICE_REGION')

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

audio_loc = 'output/audio'
speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

def generate_audio_from_text(text, audio_path):
    result = speech_synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Saves the audio data to a WAV file
        with open(audio_path, "wb") as wav_file:
            wav_file.write(result.audio_data)
        print("Speech synthesized to wave file successfully")
    else:
        print("Error synthesizing speech: {}".format(result.reason))

def generate_for_home(document):
    speaker_notes = document["title"] + ' the author of the article is:' + document["author"][0]
    generate_audio_from_text(speaker_notes, os.path.join(audio_loc, 'frame_1.wav'))
    speaker_notes = 'This is the image representing the ' + document["title"] + 'article'
    generate_audio_from_text(speaker_notes, os.path.join(audio_loc, 'frame_2.wav'))

def synthesize_audio(document):
    os.mkdir(audio_loc)
    generate_for_home(document)                             
    for i, (topic, contents) in enumerate(document['slides'].items()):
        for num, sentences in contents.items():
            speaker_notes = ''.join(sentences)
            audio_path = os.path.join(audio_loc, 'frame_{}.wav'.format(i+2))
            generate_audio_from_text(speaker_notes, audio_path)
