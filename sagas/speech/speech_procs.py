from typing import Text, List
import pyttsx3
from pydub import AudioSegment
import collections

class SpeechProcs(object):
    def __init__(self):
        self.engine = pyttsx3.init()
        # voicekind='com.apple.speech.synthesis.voice.kyoko.premium'
        self.voicekind = "com.apple.speech.synthesis.voice.samantha.premium"

    def set_voicekind(self, voice_name):
        """
        $ python -m sagas.speech.speech_procs set_voicekind Tom
        :param voice_name:
        :return:
        """
        voices: collections.Iterable = self.engine.getProperty('voices')
        self.voicekind=next((voice.id for voice in voices if voice.name==voice_name), self.voicekind)
        print(f'.. {voice_name}: {self.voicekind}')
        self.engine.setProperty("voice", self.voicekind)

    def save_file(self, sents, voice_name, outfile):
        """
        $ python -m sagas.speech.speech_procs save_file 'the text I want to save as audio' Tom tts_out
        $ python -m sagas.speech.speech_procs save_file "I'm injured" Tom tts_injured
        $ python -m sagas.speech.speech_procs save_file "I am dead" Tom tts_dead
        $ python -m sagas.speech.speech_procs save_file "私は死んだ" Otoya tts_dead_ja
        $ python -m sagas.speech.speech_procs save_file "けがをした" Otoya tts_injured_ja

        :param sents:
        :param outfile:
        :return:
        """
        self.set_voicekind(voice_name)

        target=f"./out/{outfile}.dat"
        self.engine.save_to_file(sents, target)
        self.engine.runAndWait()
        AudioSegment.from_file(target).export(f"./out/{outfile}.mp3", format="mp3")

    def save_files(self, voice_name, sents:List[Text]=None):
        """
        $ python -m sagas.speech.speech_procs save_files Tom
        :return:
        """
        if sents is None:
            sents={'t1': 'the text I want to save as audio',
                   't2': 'hello world'}

        self.set_voicekind(voice_name)
        for k,v in sents.items():
            print(f".. {k}: {v}")
            # voicekind = "com.apple.speech.synthesis.voice.samantha.premium"
            self.engine.setProperty("voice", self.voicekind)
            target = f"./out/{k}.dat"
            self.engine.save_to_file(v, target)
        self.engine.runAndWait()
        for k, v in sents.items():
            target = f"./out/{k}.dat"
            AudioSegment.from_file(target).export(f"./out/{k}.mp3", format="mp3")

    def speech(self, voice_name, sents):
        """
        $ python -m sagas.speech.speech_procs speech Tom 'you are a good man'
        :param voice_name:
        :param sents:
        :return:
        """
        self.set_voicekind(voice_name)
        self.engine.say(sents)
        self.engine.runAndWait()

if __name__ == '__main__':
    import fire
    fire.Fire(SpeechProcs)


