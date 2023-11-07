# Speech Enhancement

## Table of contents

- [Introduction](#introduction)
- [How to install](#how-to-install)
- [Demo](#demo)
- [Training](#training)
- [References](#references)
- [Contact](#contact)

## Introduction

This project is built with the purpose of eliminating noise and interference in real-world environments, making voices clearer.

## How to run

Run command

```bash
cd speech-enhancement
docker-compose up -d --build --scale app=$NUMSERVER
```

Example:
```bash
cd speech-enhancement
docker-compose up -d --build --scale app=3
```

## Demo
After the installation is complete, we will have a web interface as follows

<p align="center">
  <img src="assets/homepage.png" width="512" title="Home Page">
</p>

- Upload file and choose ``Bắt Đầu`` button, we have the result follow

<p align="center">
  <img src="assets/outputpage.png" width="512" alt="Output Page">
</p>

- After completion, you can listen to the audio samples before and after processing, and also download the results.

## Training

- To train the model, you can refer to the assets code available here: [MP-SENet: A Speech Enhancement Model with Parallel Denoising of Magnitude and Phase Spectra](https://github.com/yxlu-0102/MP-SENet)

<p align="center">
  <img src="assets/model_short_version.png" width="70%" alt="Architecture">
</p>

### Data preparation

The project utilizes two main datasets:
- [VoiceBank+DEMAND](https://paperswithcode.com/dataset/voice-bank-demand)
- Synthesis data

With synthsis data:
- Clean Audio: We leverage clean audio data from the [FPT Open Speech Dataset (FOSD) - Vietnamese](https://data.mendeley.com/datasets/k9sxg2twv4/4)

- The environmental noise were gathered from [ESC-50 dataset](https://github.com/karolpiczak/ESC-50). However, we only focus on 20 classes which we believe are the most relevant to daily environmental noise. These classes are:

|                 |   |             |   |                  |   |
|-----------------|---|-------------|---|------------------|---|
| vacuum cleaner  | <img src="assets/vaccum-cleaner.jpg" height="100"/>  | engine      |  <img src="assets/engine.jpg" height="100"/> | keyboard typing  | <img src="assets/keyboard.jpg" height="100"/> |
| fireworks       | <img src="assets/firework.jpg" height="100"/>  | mouse click | <img src="assets/mouse-click.png" height="100"/>  | footsteps        | <img src="assets/footsteps.jpg" height="100"/>  |
| clapping        | <img src="assets/clapping.jpg" height="100"/> | clock alarm | <img src="assets/clock-alarm.jpg" height="100"/>  | car horn         | <img src="assets/car-horn.jpg" height="100"/>  |
| door wood knock | <img src="assets/knock.jpg" height="100"/>  | wind        | <img src="assets/wind.jpg" height="100"/>  | drinking sipping | <img src="assets/drinking-sipping.jpg" height="100"/>  |
| washing machine | <img src="assets/washing-machine.jpeg" height="100"/> | rain        | <img src="assets/rain.png" height="100"/>  | rooster          | <img src="assets/rooster.jpg" height="100"/>  |
| snoring         | <img src="assets/snoring.jpg" width="100"/> | breathing   | <img src="assets/breathing.jpg" height="100"/>  | toilet flush     | <img src="assets/toilet-flush.jpg" height="100"/>  |
| clock tick      | <img src="assets/clock-tick.jpg" height="100"/>  | laughing    | <img src="assets/laughing.jpg" height="100"/>  |                  |   |

- Noises have been blended to clean voices with a randomization of the noise level (between 30% and 85%)


## References

- [MP-SENet: A Speech Enhancement Model with Parallel Denoising of Magnitude and Phase Spectra](https://github.com/yxlu-0102/MP-SENet)
- [FPT Open Speech Dataset (FOSD) - Vietnamese](https://data.mendeley.com/datasets/k9sxg2twv4/4)
- [VoiceBank+DEMAND](https://paperswithcode.com/dataset/voice-bank-demand)
- [ESC-50 dataset](https://github.com/karolpiczak/ESC-50)

## Contact
- [Nguyen Y Hop](nguyenyhop1999@gmail.com)
