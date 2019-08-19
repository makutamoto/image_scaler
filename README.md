Image Scaler
=====
Scales a bunch of images at once.

Usage Examples
-----
#### Scale all images in your working directory to 200px width

`imscale.py ./*.png -w 200 -p "scaled-"`

To overwrite original images, use this:

`imscale.py ./*.png -w 200 -f`

#### Grayscale all images in your working directory

`imscale.py ./*.png -g -p "grayscaled-"`

License
-----
Image Scaler is released under MIT License.
