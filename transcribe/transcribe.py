import os
import whisper
import torch
from ffutils import ffprog
from pathlib import Path
from tempfile import mktemp
from colorama import Fore, init
import argparse
import subprocess
import shutil

def parse_arguments():
    parser = argparse.ArgumentParser(description='Transcribe video and add subtitles.')
    parser.add_argument('-i', '--input', type=str, help='Input video file path', required=True)
    parser.add_argument('--model', type=str, choices=['tiny', 'base', 'small', 'medium', 'large'], default='small', help='Whisper model size (tiny, base, small, medium, large)')
    return parser.parse_args()

def seconds_to_srt_time_format(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def get_video_duration(video_path):
    ffprobe_command = [
        'ffprobe',
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(ffprobe_command, capture_output=True, text=True)
    duration = float(result.stdout)
    return duration

def has_audio_stream(video_path):
    ffprobe_command = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'a',
        '-show_entries', 'stream=codec_type',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        video_path
    ]
    result = subprocess.run(ffprobe_command, capture_output=True, text=True)
    return 'audio' in result.stdout

def split_video(src):
    src_filename = Path(src).stem
    output_dir = Path.cwd() / 'cuts'
    output_dir.mkdir(exist_ok=True)
    print(Fore.CYAN + 'Splitting videos. Please wait...')
    ffmpeg_command = [
        'ffmpeg',
        '-hide_banner',
        '-i', src,
        '-threads', '3',
        '-vcodec', 'copy',
        '-f', 'segment',
        '-segment_time', '1200',
        '-reset_timestamps', '1',
        str(output_dir / f'{src_filename}_%02d.mp4')
    ]
    subprocess.run(ffmpeg_command, check=True)

def transcribe_and_subtitle(video_in, model_size):
    torch_device = "cuda" if torch.cuda.is_available() else "cpu"
    if not video_in.exists():
        print(Fore.RED + f"File {video_in} does not exist")
        exit()

    output_dir = Path.cwd() / 'output'
    output_dir.mkdir(exist_ok=True)

    video_out = output_dir / f"{video_in.stem}_subtitled_en.mp4"

    if not has_audio_stream(video_in):
        print(Fore.RED + f"No audio stream found in {video_in}. Skipping this file.")
        try:
            new_name = video_in.with_name(video_in.stem + "_no_audio" + video_in.suffix)
            os.rename(video_in, new_name)
            print(Fore.GREEN + f"Renamed {video_in} to {new_name}.")
        except Exception as e:
            print(Fore.RED + f"Error renaming {video_in}: {e}")
        return

    cwd = Path(os.getcwd())
    audio_file = mktemp(suffix=".aac", dir=cwd)
    try:
        ffprog(["ffmpeg", "-y", "-i", str(video_in), "-vn", "-c:a", "aac", audio_file], desc=Fore.CYAN + 'Extracting audio from video')
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Failed to extract audio from {video_in}: {e.stderr.decode()}")
        return

    if not os.path.exists(audio_file) or os.path.getsize(audio_file) == 0:
        print(Fore.RED + f"Extracted audio file {audio_file} is empty or does not exist. Skipping this file.")
        return

    model_dir = cwd / "models"
    model_files = list(model_dir.glob(f"{model_size}.pt"))
    if model_files:
        print(Fore.CYAN + f"Model for '{model_size}' found in cache directory.")
        print(Fore.CYAN + "Loading model...")
    else:
        print(Fore.CYAN + f"Model for '{model_size}' not found in cache directory.")
        print(Fore.CYAN + "Downloading model...")
    model = whisper.load_model(model_size, download_root="models", device=torch_device)

    print(Fore.CYAN + "Transcribing...")
    try:
        results = model.transcribe(audio_file, language="en", task="translate", no_speech_threshold=0.3, condition_on_previous_text=False, verbose=False)
    except Exception as e:
        print(Fore.RED + f"Error during transcription: {e}")
        return

    os.remove(audio_file)

    subtitle_file = mktemp(suffix=".srt", dir=cwd)
    print(Fore.GREEN + f"Writing subtitle to {subtitle_file}...")
    with open(subtitle_file, "w", encoding="utf-8") as f:
        index = 1
        for segment in results['segments']:
            start_time = segment['start']
            end_time = segment['end']
            text = segment['text']
            f.write(f"{index}\n")
            f.write(f"{seconds_to_srt_time_format(start_time)} --> {seconds_to_srt_time_format(end_time)}\n{text}\n\n")
            index += 1

    ffprog(
        ["ffmpeg", "-y", "-i", str(video_in), "-vf", f"subtitles={str(Path(subtitle_file).name)}:force_style='Fontname=Arial,Fontsize=16,OutlineColour=&H80000000,BorderStyle=4,BackColour=&H80000000,Outline=0,Shadow=0,MarginV=10,Alignment=2,Bold=-1'",
         str(video_out)],
        cwd=str(Path(subtitle_file).parent),
        desc=Fore.GREEN + f"Burning subtitles into {video_out}",
    )

    subtitle_file_renamed = cwd / f"{video_in.stem}_subs_en.srt"
    try:
        os.rename(subtitle_file, subtitle_file_renamed)
    except FileExistsError:
        print(Fore.RED + f"File '{subtitle_file_renamed}' already exists. Deleting the existing file.")
        os.remove(subtitle_file_renamed)
        os.rename(subtitle_file, subtitle_file_renamed)

    move_subtitle_to_srt_folder(subtitle_file_renamed)
    delete_processed_video(video_in)

def delete_processed_video(video_file):
    try:
        os.remove(video_file)
        print(Fore.GREEN + f"Deleted {video_file} from 'cuts' folder.")
    except Exception as e:
        print(Fore.RED + f"Error deleting {video_file} from 'cuts' folder: {e}")

def move_subtitle_to_srt_folder(subtitle_file):
    srt_folder = Path.cwd() / 'srt'
    srt_folder.mkdir(exist_ok=True)
    try:
        shutil.move(subtitle_file, srt_folder)
        print(Fore.YELLOW + f"Moved {subtitle_file} to {srt_folder}")
    except Exception as e:
        print(Fore.RED + f"Error moving {subtitle_file} to {srt_folder}: {e}")

def process_cuts():
    cwd = Path(os.getcwd())
    cuts_dir = cwd / 'cuts'
    for video_file in cuts_dir.glob('*.mp4'):
        print(Fore.YELLOW + f"Processing {video_file}...")
        transcribe_and_subtitle(video_file, args.model)

def remove_converted(converted_video):
    os.remove(converted_video)
    print(Fore.YELLOW + f"Removed {converted_video}...")

def Pipeline():
    video_path = Path(args.input)
    converted_video = None
    if video_path.suffix.lower() == '.mkv':
        output_dir = Path.cwd() / 'converted'
        output_dir.mkdir(exist_ok=True)
        converted_video = output_dir / f"{video_path.stem}.mp4"
        ffmpeg_command = [
            'ffmpeg',
            '-i', str(video_path),
            '-codec', 'copy',
            str(converted_video)
        ]
        subprocess.run(ffmpeg_command, check=True)
        print(Fore.YELLOW + f"Converted {video_path} to {converted_video}")

    video_duration = get_video_duration(converted_video if converted_video else args.input)
    if video_duration > 1200:
        if converted_video:
            split_video(converted_video)
            process_cuts()
            remove_converted(converted_video)
        else:
            split_video(args.input)
            process_cuts()
    else:
        print(Fore.YELLOW + "Video duration is less than or equal to 20 minutes. Proceeding to transcribe and subtitle.")
        transcribe_and_subtitle(Path(converted_video) if converted_video else Path(args.input), args.model)

def main():
    init(autoreset=True)
    global args
    args = parse_arguments()
    Pipeline()

if __name__ == "__main__":
    main()