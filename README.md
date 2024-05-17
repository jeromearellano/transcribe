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

**Note:** Additionally, you'll need to install the following external dependencies:

- **FFmpeg**: Download and install FFmpeg separately from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z).

  After downloading, extract the contents of the archive and add the FFmpeg binaries to your system PATH.

- **CUDA Toolkit** (Optional, for users with dedicated GPUs): If you have a dedicated NVIDIA GPU and wish to enable GPU acceleration, you'll need to install the CUDA Toolkit. You can download the CUDA Toolkit from [here](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=11&target_type=exe_local) and follow the installation instructions provided by NVIDIA.

## Setting up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies for this project. Follow these steps to create and activate a virtual environment:

1. Install `virtualenv` if you haven't already:
```bash
pip install virtualenv
```
   
2. Navigate to the project directory:
```bash
cd /path/to/your/directory
```

3. Create a virtual environment:
```bash
python -m virtualenv venv
```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
     
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

Once activated, you can install the project dependencies within the virtual environment without affecting your system-wide Python installation.

## Installation

To install the package, clone the repository and install using `pip`:

```bash
git clone https://github.com/jeromearellano/transcribe.git
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

## License

This project is licensed under the MIT License.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) for the transcription model.
- [FFmpeg](https://ffmpeg.org/) for video processing.
- [Colorama](https://pypi.org/project/colorama/) for colored terminal output.
- [Torch](https://pytorch.org/) for the deep learning framework.
- [ffutils](https://github.com/slhck/ffmpeg-normalize) for FFmpeg utilities.
