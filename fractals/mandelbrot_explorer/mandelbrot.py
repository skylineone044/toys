import numpy
from functools import wraps
import time as time_time
import multiprocessing
from matplotlib import cm

import pygame
from pygame import *
from pygame.locals import *

BRIGHTNESS = 255
MAX_Z = 2
MAX_ITERATIONS = 80
WIDTH = 700
HEIGHT = 700

# cmap = cm.get_cmap("gnuplot2")
# cool colors: "YlGnBu", "gnuplot2","inferno","gist_earth","cubehelix",
cmap = cm.get_cmap("gnuplot2")
LUT = []
for i in range(BRIGHTNESS):
    LUT.append(cmap(i / BRIGHTNESS, bytes=True)[:3])
# LUT = LUT[::-1]


def timeit(
    func,
):  # ezt loptam: https://sureshdsk.dev/python-decorator-to-measure-execution-time
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time_time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time_time.perf_counter()
        total_time = end_time - start_time
        print(
            f"Function {func.__name__}{args[:-1]} {kwargs} Took {total_time:.4f} seconds"
        )  # not printing out the numpy array, that is the last arg
        return result

    return timeit_wrapper


# @timeit
def mandelbrot(*args):
    (
        boundary_x_min,  # start of the slice in the complex plane
        boundary_x_max,  # width of the slice in teh complex plane
        boundary_y_min,  # bottom and top of boundary in the complex plane
        boundary_y_max,
        out_array,  # result array
    ) = args

    # print(out_array.shape)
    for i, x in enumerate(
        numpy.linspace(boundary_x_min, boundary_x_max, num=out_array.shape[1])
    ):
        # print(f"{i=}/{out_array.shape[1]}", end="    \r")
        for j, y in enumerate(
            numpy.linspace(boundary_y_min, boundary_y_max, num=out_array.shape[0])
        ):
            z = complex(0, 0)
            c = complex(y, x)
            iterations = 0

            while abs(z) <= MAX_Z and iterations < MAX_ITERATIONS:
                z = z ** 2 + c
                iterations += 1

            out_array[j, i] = min(
                int(((iterations / MAX_ITERATIONS) * BRIGHTNESS)), 254
            )
    return out_array


def mp_handler(*args):
    (
        sum_array,
        threads,
        (res_width, res_height),
        (boundary_y_min, boundary_y_max),
        (boundary_x_min, boundary_x_max),
    ) = args

    c_ranges = numpy.linspace(
        boundary_x_min, boundary_x_max, num=threads, endpoint=False
    )
    range_width = abs(c_ranges[0] - c_ranges[1])

    print("calculating ranges...")
    slice_IDs = []
    for i in range(threads):
        slice_start = i * (res_width // threads)
        slice_width = res_width // threads
        slice_IDs.append(
            (
                c_ranges[i],  # start of the slice in the complex plane
                c_ranges[i] + range_width,  # width of the slice in teh complex plane
                boundary_y_min,  # bottom and top of boundary in the complex plane
                boundary_y_max,
                sum_array[:, slice_start : slice_start + slice_width],  # result array
            )
        )
    # print(slice_IDs)

    print("starting pool...")
    p = multiprocessing.Pool(threads)
    results = p.starmap(mandelbrot, slice_IDs)
    # print(results)
    p.close()
    p.join()

    # minden thread kap egy full 0 mátrixot, és a végén összelegózom
    print("joining arrays...")
    sum_array = numpy.concatenate(results, axis=1)
    return sum_array


def render(center=(-0.5, 0), r=1.2):
    print("rendering...")
    zero_arr = numpy.zeros((HEIGHT, WIDTH))

    frame_array = mp_handler(
        zero_arr,  # starting array
        50,  # thread cound
        (WIDTH, HEIGHT),  # result resolution in pixels
        (center[0] - r, center[0] + r),  # (boundary_y_min, boundary_y_max)
        (center[1] - r, center[1] + r),  # (boundary_x_min, boundary_x_max)
    ).astype(numpy.uint8)
    color_array = numpy.zeros((*frame_array.shape, 3), dtype=numpy.uint8)
    numpy.take(LUT, frame_array, axis=0, out=color_array)

    print("render done")
    surface = pygame.surfarray.make_surface(color_array)
    return surface


def main():
    pygame.init()
    display = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(display)

    center = [-0.5, 0]
    r = 1.2

    surface = render(center, r)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    center[1] -= 0.05 * r
                elif event.key == pygame.K_s:
                    center[1] += 0.05 * r
                elif event.key == pygame.K_a:
                    center[0] -= 0.05 * r
                elif event.key == pygame.K_d:
                    center[0] += 0.05 * r

                elif event.key == pygame.K_KP_PLUS:
                    r *= 0.9
                elif event.key == pygame.K_KP_MINUS:
                    r *= 1.1

                surface = render(center, r)

        screen.blit(surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(10)


if __name__ == "__main__":
    main()
    pass
