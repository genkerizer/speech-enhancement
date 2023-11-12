
import os
import json
import torch
import librosa
import soundfile as sf
import time

from torch.utils.mobile_optimizer import optimize_for_mobile

from .src.utils import AttrDict
from .src.generate import MPNet
from .src.data_process import mag_pha_stft, mag_pha_istft

class SpeechEnhancement:

    def __init__(self, **kwargs):
        self.relative_path = os.path.dirname(os.path.realpath(__file__))
        cfg_path = os.path.join(self.relative_path, 'configs/cfg.json')
        assert os.path.exists(cfg_path), 'cannot find config path'

        self.cfg = json.load(open(cfg_path))
        self.global_cfg = self.cfg['Global']
        self.h = AttrDict(self.cfg['Model'])

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        if True:
            self.model = MPNet(self.h).to(self.device)
            # total_params = sum(p.numel() for p in self.model.parameters())
            # print(f"Number of parameters: {total_params}")
            state_dict = self.load_weight()
            self.model.load_state_dict(state_dict['generator'])
            self.model.eval()
        else:
            self.model = None

    def optimizier4mobile(self):
        example = torch.rand(1, 201, 100)
        traced_script_module = torch.jit.trace(self.model, (example, example))
        traced_script_module_optimized = optimize_for_mobile(traced_script_module)
        traced_script_module_optimized._save_for_lite_interpreter("infer/models/mobile/model.ptl")
        
    def convert2onnx(self):
        print("Convert to onnx...")
        dims = 11
        input1 = torch.randn(1, 201, dims, requires_grad=False)
        input2 = torch.randn(1, 201, dims, requires_grad=False)
        output = self.model(input1, input2)
        torch.onnx.export(self.model,               # model being run
                  (input1, input2),                         # model input (or a tuple for multiple inputs)
                  "infer/models/onnx/speech_enhance.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=10,          # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  input_names = ['input1', 'input2'],   # the model's input names
                  output_names = ['output1', 'output2', 'output3'], # the model's output names
                  dynamic_axes={'input1' : {2 : 'dims'},
                                'input2' : {2 : 'dims'},   # variable length axes
                                'output1' : {2 : 'dims'},
                                'output2' : {2 : 'dims'},
                                'output3' : {2 : 'dims'}})
        print("Done")


    def load_weight(self):
        weight_path = os.path.join(self.relative_path, self.global_cfg['weight'])
        assert os.path.isfile(weight_path)
        print("Loading '{}'".format(weight_path))
        state_dict = torch.load(weight_path, map_location=self.device)
        print("Complete.")
        return state_dict
    

    def split_audio(self, signal, duration, sampling_rate=16000, max_duration_per_process=1.0):
        if duration < max_duration_per_process:
            return [signal]
        num_split = int(duration // max_duration_per_process)
        split_signal_list = []
        for i in range(0, num_split):
            tmp_split_signal = signal[i * sampling_rate:(i+1)*sampling_rate]
            split_signal_list.append(tmp_split_signal)
        if num_split * max_duration_per_process < duration - 100:
            split_signal_list.append(signal[num_split*sampling_rate:])
        return split_signal_list





    def predict(self, audio_path, output_dir="app/speech_enhan/outputs"):
        assert self.model is not None
        assert os.path.exists(audio_path)
        name = audio_path.split('/')[-1]
        with torch.no_grad():
            signal, _ = librosa.load(audio_path, self.h.sampling_rate)
            duration = len(signal) / self.h.sampling_rate
            split_signal = self.split_audio(signal, duration)
            
            output_list = []

            for noisy_wav in split_signal:
                noisy_wav = torch.FloatTensor(noisy_wav).to(self.device)
                norm_factor = torch.sqrt(len(noisy_wav) / torch.sum(noisy_wav ** 2.0)).to(self.device)
                noisy_wav = (noisy_wav * norm_factor).unsqueeze(0)
                noisy_amp, noisy_pha, noisy_com = mag_pha_stft(noisy_wav, self.h.n_fft, self.h.hop_size, self.h.win_size, self.h.compress_factor)
                amp_g, pha_g, com_g = self.model(noisy_amp, noisy_pha)
                audio_g = mag_pha_istft(amp_g, pha_g, self.h.n_fft, self.h.hop_size, self.h.win_size, self.h.compress_factor)
                audio_g = audio_g / norm_factor
                output_list.append(audio_g)
            output_list = torch.cat(output_list, -1)
            output_file = os.path.join(output_dir, '.'.join(name.split('.')[:-1] + ['wav']))
            print(output_file)

            sf.write(output_file, output_list.squeeze().cpu().numpy(), self.h.sampling_rate, 'PCM_16')
            return output_file, duration

if __name__ == '__main__':
    class_ = SpeechEnhancement()
    class_.predict('speech_enhan/debugs/64.mp3')
   