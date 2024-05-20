from setuptools import setup, find_packages

def read_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name='transcribe',
    version='0.1.0',
    description='Transcribe video and add subtitles using Whisper AI.',
    author='Jerome A. Arellano',
    author_email='jerome.a.arellano@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=read_requirements(),
    dependency_links=[
        'https://download.pytorch.org/whl/cu121/torch-2.3.0%2Bcu121-cp312-cp312-win_amd64.whl',
        'https://download.pytorch.org/whl/cu121/torchaudio-2.3.0%2Bcu121-cp312-cp312-win_amd64.whl',
        'https://download.pytorch.org/whl/cu121/torchvision-0.18.0%2Bcu121-cp312-cp312-win_amd64.whl',
        'https://download.pytorch.org/whl/torchmetrics-1.0.3-py3-none-any.whl'
    ],
    entry_points={
        'console_scripts': [
            'transcribe=transcribe.transcribe:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
