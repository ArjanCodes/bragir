# Bragir
![Authors](https://kajabi-storefronts-production.kajabi-cdn.com/kajabi-storefronts-production/file-uploads/themes/2149113237/settings_images/4adb13d-824c-454-a5c-72b2c6f06e1_Arjan_Codes_-_FInal_Files.png)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Description

The bragir CLI is a command-line application built using Click. Its primary purpose is to facilitate the translation of SubRip Subtitle (SRT) files using the OpenAI GPT-based language model, ChatGPT.

## Features

- **Translation:** Translate the content of SRT files from one language to another using the power of ChatGPT.
- **Batch Processing:** Process a single SRT file, multiple files, or an entire directory, providing flexibility and efficiency.
- **Easy-to-Use Interface:** Utilize a user-friendly command-line interface powered by Click, making translation tasks straightforward.

## Table of Contents

- [bragir](#bragir)
  - [Description](#description)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Provide step-by-step instructions on how to install your project. Include any dependencies and how to resolve them.

```bash
pip install bragir
```

# Usage

Translate a single file to one language:

```
bragir --file input.srt --language fr 
```

Translate multiple files to multiple languages:

```
bragir --file input_1.srt --file input_2.srt --language French --language German 
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







