# Bragir
![Authors](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/themes/2149113237/settings_images/4adb13d-824c-454-a5c-72b2c6f06e1_Arjan_Codes_-_FInal_Files.png)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Description

The bragir CLI is a command-line application built using Click. Its primary purpose is to handle and generate SubRip Subtitle (SRT) files using ChatGPT and Whisper from Openai.

## Features

- **Translation:** Translate the content of SRT files from one language to another using ChatGPT.
- **Transcription:** Trancribe the content of video and audio files from one language to another using Whisper.
- **Batch Processing:** Process a single file, multiple files, or an entire directory, providing flexibility and efficiency.
- **Easy-to-Use Interface:** Utilize a user-friendly command-line interface powered by Click, making translation tasks straightforward.

## Table of Contents

- [Bragir](#bragir)
  - [Description](#description)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [FFmpeg](#ffmpeg)
      - [Macos](#macos)
      - [Linux](#linux)
      - [Windows](#windows)
    - [OpenAI](#openai)
    - [Bragir](#bragir-1)
- [Usage](#usage)
    - [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

In order to use the full potential of Bragir, FFmpeg is needed to be installed on the system and you need to obtain an Openai key.

### FFmpeg
#### Macos
**Using brew**
```zsh
brew install ffmpeg
```

#### Linux

Update avaiable linux packages
```bash
 sudo apt update
```
Install ffmpeg
```bash
 sudo apt install ffmpeg
```

#### Windows

Download the .exe from official [ffmpeg-website](https://ffmpeg.org/download.html)

Extract the contents of the zip file and rename the file to FFmpeg.

Move the folder into the main drive (Usually c:/)

Open command prompt as administrator, and add FFmpeg to your system path

```bash
setx /m PATH "C:\ffmpeg\bin;%PATH%"
```

**Verifyting the installation**
In order to see if the installation of FFmpeg is correct, run the following command
```bash
ffmpeg --version 
```

If a version is displayed, then FFmpeg is installed correctly.

### OpenAI

Currently, this tool relise on OpenAIs API. That means that an OpenAI api-key is crucial. See the following resource of [how to get an OpenAI api-key](https://platform.openai.com/docs/quickstart?context=python)

### Bragir
Use pip to install Bragir
```bash
pip install bragir
```

Check if installation is complete

```
bragir --version
```
If a version is displayed, then Bragir is installed correctly.


# Usage

Bragir comes with two commands, transcribe and translate. Transcribe will always generate an file with extension `.srt`. The translate command has only been tested with SRT-files, however other files would work. However, Bragir is not intended to translate other file types  

In order to use either command, a Openai needs to be loaded into the terminal session or as an flag to the command.

Load Openai key as an enviroment variable into current session
```
export OPENAI_KEY=<VALUE>
```

Flag in command:
```
bragir translate ... --api_key <VALUE>
```

### Examples
Translate a single file to one language:

```
bragir translate --file <FILE_PATH> --language fr 
```

Translate multiple files to multiple languages:

```
bragir translate --file <FILE_PATH> --file <FILE_PATH> --language French --language German 
```

Translate files in a directory to multiple languages:

```
bragir translate --directory <DIRECTORY_PATH> --language French --language German --api_key <OPENAI_KEY> 
```

Transcribe file:

```
bragir transcribe --file <FILE_PATH> --api_key <OPENAI_KEY> 
```

Transcribe files in a directory:

```
bragir transcribe --directory <DIRECTORY_PATH> --api_key <OPENAI_KEY> 
```

# Contributing
If you want to contribute to this project, please use the following steps:

1. Fork the project.
2. Create a new branch (git checkout -b feature/awesome-feature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/awesome-feature).
5. Open a pull request.

# License
This project is licensed under the MIT License.







