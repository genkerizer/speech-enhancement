
import os
from .speech_enhan.predict_model import SpeechEnhancement

class_ = SpeechEnhancement()

def backend(input_path, output_dir):
    name = input_path.split('/')[-1]
    output_path = class_.predict(input_path, output_dir)
    return output_path