from typing import Text, List
import pyttsx3
from pydub import AudioSegment

class SpeechProcs(object):
    def __init__(self):
        self.engine = pyttsx3.init()

    def save_file(self, sents, outfile):
        """
        $ python -m sagas.speech.speech_procs save_file 'the text I want to save as audio' tts_out
        :param sents:
        :param outfile:
        :return:
        """
        # voicekind='com.apple.speech.synthesis.voice.kyoko.premium'
        voicekind="com.apple.speech.synthesis.voice.samantha.premium"
        self.engine.setProperty("voice", voicekind)
        target=f"./out/{outfile}.dat"
        self.engine.save_to_file(sents, target)
        self.engine.runAndWait()
        AudioSegment.from_file(target).export(f"./out/{outfile}.mp3", format="mp3")

    def save_files(self, sents:List[Text]=None):
        """
        $ python -m sagas.speech.speech_procs save_files
        :return:
        """
        if sents is None:
            sents={'t1': 'the text I want to save as audio',
                   't2': 'hello world'}
        for k,v in sents.items():
            print(f".. {k}: {v}")
            voicekind = "com.apple.speech.synthesis.voice.samantha.premium"
            self.engine.setProperty("voice", voicekind)
            target = f"./out/{k}.dat"
            self.engine.save_to_file(v, target)
        self.engine.runAndWait()
        for k, v in sents.items():
            target = f"./out/{k}.dat"
            AudioSegment.from_file(target).export(f"./out/{k}.mp3", format="mp3")

if __name__ == '__main__':
    import fire
    fire.Fire(SpeechProcs)


