# Transcribe

Transcribe video and add subtitles using Whisper AI.

## Features

- Split videos longer than 20 minutes into segments.
- Extract audio from video files.
- Transcribe audio using Whisper AI.
- Generate and burn subtitles into videos.
- Handle various video formats, including `.mkv` conversion to `.mp4`.

## Requirements

See `requirements.txt` for a list of dependencies.

- `torch`
- `torch-audiomentations`
- `torch-pitch-shift`
- `torchaudio`
- `torchmetrics`
- `torchvision`
- `openai-whisper`
- `colorama`
- `ffutils`
- `ffmpeg`

## Installation

To install the package, clone the repository and install using `pip`:

```bash
git clone https://github.com/yourusername/transcribe.git
cd transcribe
pip install .
```

## Usage

To use the CLI tool, run the following command:

```bash
transcribe -i /path/to/video.mp4 --model small
```

## Arguments

- `-i, --input`: Path to the input video file. (required)
- `--model`: Whisper model size to use (`tiny`, `base`, `small`, `medium`, `large`). Default is `small`.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Steps to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the transcription model.
- [FFmpeg](https://ffmpeg.org/) for video processing.
- [Colorama](https://pypi.org/project/colorama/) for colored terminal output.
- [Torch](https://pytorch.org/) for the deep learning framework.
- [ffutils](https://github.com/slhck/ffmpeg-normalize) for FFmpeg utilities.
