import os
import tempfile
import argparse
from subprocess import call

from pdf2image import convert_from_path
from gtts import gTTS


__author__ = ['slideit']


## Sometimes ffmpeg is avconv
# FFMPEG_NAME = 'ffmpeg'
FFMPEG_NAME = 'avconv'


def generate_video_from_images(fps=24, bitrate='5000k'):
    """
    Generates a video from a list of images.

    :param images: List of images to use in the video.
    :type images: list
    :param output_file: Path to the output video file.
    :type output_file: str
    :param fps: Frames per second of the output video.
    :type fps: int
    :param bitrate: Bitrate of the output video.
    :type bitrate: str
    """
    # Create a temporary directory to store the images
    temp_dir = tempfile.mkdtemp()

    # Save the images to the temporary directory
    images = convert_from_path('slidev/slides-export.pdf', output_folder=temp_dir, fmt='png', dpi=300)
    for i, image in enumerate(images):
        image.save(os.path.join(temp_dir, 'image%05d.png' % i))

    # Generate the video from the images
    call([
        FFMPEG_NAME,
        '-y',
        '-r', str(fps),
        '-i', os.path.join(temp_dir, 'image%05d.png'),
        '-vcodec', 'libx264',
        '-crf', '25',
        '-pix_fmt', 'yuv420p',
        '-b', bitrate,
        output_file
    ])

    # Remove the temporary directory
    os.rmdir(temp_dir)