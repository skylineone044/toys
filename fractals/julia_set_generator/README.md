# Julia set generator

generates the [Julia set](https://en.wikipedia.org/wiki/Julia_set) of the [Mandelbrot set](https://en.wikipedia.org/wiki/Mandelbrot_set) at a given point on the complex plane

## Basic Usage

jsut run the script with a decently recent python3: I tested it on 3.10

```shell
python julia.py
```

## Configuration

use the global variables defined at the beginning of the script

- `THREADS`: How many threads should the script use (at least 2)
- `PATH`: The path for the output image file
- `WIDTH`: the horizontal resolution of the output image
- `HEIGHT`: the vertical resolution of the output image
- `C`: the point on the complex plane of the Mandelbrot Set at which this julia set is
- `MAX_Z`: the number at which the algorithm considers the current pixel to be divergent
- `MAX_ITERATIONS`: if the currnt pixel has not diverged by this many iterations, the algorithm considers this pixel to be not divergent
- `BOUNTARY_X`: the horizontal distance from the origin on the complex plane in each direciton to be imaged
- `BOUNTARY_Y`: the vertical distance from the origin on the complex plane in each direciton to be imaged
- `cmap`: a matplotlib LUT, which determines what color each brightness level on the output image should be; I have found  "YlGnBu", "gnuplot2","inferno","gist_earth","cubehelix", "tab20c" to be pretty decent, the example image uses the "tab20c" palette

## Example image

![Example image at C=(-0.8, 0.156)](./example.png)

## Animations

The script can also generate image sequences, by interpolating the C point on the complex plane along a straight line, or around a circle

The sequences are going to be planced in the `./sequence/` directory, you can then use a tool like `ffmpeg` to combine the images into a video file.

### Usage

#### Around a circle

use the function `anim_circle(frame_count, r)`, where:

- `frame_count`: the number of images to be generated
- `r`: the radius of the circle

#### Along a straight line

use the function `anim_ft(frame_count, c_from, c_to)`, where:

- `frame_count`: the number of images to be generated
- `c_from`: the starting point of the line on the complex plane
- `c_to`: the ending point of the line on the complex plane

## Example video

![Example video with a radius of r=0.7885](./example.mp4)
