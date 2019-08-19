#!/usr/bin/env python3
import os
import re
import sys
from optparse import OptionParser
from PIL import Image


if __name__ == '__main__':
    parser = OptionParser(usage="%prog [options] [files]")
    parser.add_option('-w', '--width', help="specify the width of scaled images.")
    parser.add_option('-t', '--height', help="specify the height of scaled images.")
    parser.add_option('-p', '--prefix', help="specify the prefix of output file names.", default='')
    parser.add_option('-s', '--suffix', help="specify the suffix of output file names.", default='')
    parser.add_option('-f', '--force', action='store_true', default=False, help="allow to overwrite existing files.")
    parser.add_option('-g', '--grayscale', action='store_true', default=False, help="grayscale output images.")
    parser.add_option('-r', '--rgb', action='store_true', default=False, help="convert to rgb mode.")
    options, args = parser.parse_args()
    if options.grayscale and options.rgb:
        sys.stderr.write("'grayscale' and 'rgb' options are exclusive.")

    REGEX_NAME = re.compile(r"\.?([^/\.\n]+)[^/\n]*?$")
    scaled = 0
    for filename in args:
        try:
            with Image.open(filename) as im:
                if options.width is None and options.height is None:
                    width = im.size[0]
                    height = im.size[1]
                else:
                    aspect = im.size[0] / im.size[1]
                    if options.width is None:
                        width = int(float(options.height) * aspect)
                    else:
                        width = int(options.width)
                    if options.height is None:
                        height = int(float(options.width) / aspect)
                    else:
                        height = int(options.height)
                new_image = im.resize((width, height))
                if options.grayscale:
                    new_image = new_image.convert('L')
                elif options.rgb:
                    new_image = new_image.convert('RGB')

                match = REGEX_NAME.search(filename)
                parent = filename[:match.start(1)]
                extension = filename[match.end(1):]
                new_name = parent + options.prefix + match.group(1) + options.suffix + extension

                if options.force or not os.path.isfile(new_name):
                    try:
                        new_image.save(new_name)
                        scaled += 1
                        if options.grayscale:
                            print('Scaled(grayscale):', filename, '->', new_name)
                        elif options.rgb:
                            print('Scaled(RGB):', filename, '->', new_name)
                        else:
                            print('Scaled:', filename, '->', new_name)
                    except IOError:
                        print("Permission denied:", filename)
                else:
                    print("Already exists (--force):", new_name)
        except IOError:
            print("Couldn't be opened:", filename)
    print('Scaled', scaled, 'of', len(args), 'images.')
