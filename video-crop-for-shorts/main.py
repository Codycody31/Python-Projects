import moviepy.editor as mpy
from moviepy.video.fx.all import crop
import argparse
import sys
import os
directory = os.path.dirname(__file__) + "\\"


def main():
    parser = argparse.ArgumentParser(
        description=' Crop a video file using moviepy.')
    parser.add_argument('-f', '--file', help='File to crop, ex: test.mp4')
    parser.add_argument(
        '-o', '--output', help='Output file name and type, ex: test.mp4')
    parser.add_argument('-st', '--start', type=int,
                        help='Start time.', default=0)
    parser.add_argument('-et', '--end', type=int, help='End time.', default=60)
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Suppress output to stdout.')
    parser.add_argument('-e', '--error', action='store_true',
                        help='File to write errors to.')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.quiet == True:
        sys.stdout = open(os.devnull, 'w')
    if (args.file is None) or (args.output is None):
        print('File and output file name are required.')
        sys.exit(1)
    if args.end < args.start:
        print('End time must be greater than start time.')
        sys.exit(1)
    if args.start < 0:
        print('Start time must be greater than 0.')
        sys.exit(1)
    if args.end <= 0:
        print('End time must be greater than 0.')
        sys.exit(1)
    if args.end == args.start:
        print('End time must be greater than start time.')
        sys.exit(1)
    clip = mpy.VideoFileClip(args.file)
    clip = clip.subclip(args.start, args.end)
    (w, h) = clip.size

    crop_width = h * 9/16
    # x1,y1 is the top left corner, and x2, y2 is the lower right corner of the cropped area.

    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    cropped_clip = crop(clip, x1=x1, y1=y1, x2=x2, y2=y2)
    # or you can specify center point and cropped width/height
    # cropped_clip = crop(clip, width=crop_width, height=h, x_center=w/2, y_center=h/2)
    cropped_clip.write_videofile(directory + args.output, verbose=False)


main()