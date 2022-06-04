import numpy
import pathlib
from functools import wraps
import time
import multiprocessing
from PIL import Image
from matplotlib import cm

# hello
# ez a csoda képes a julia set egy slice-át legenerálni
# de nem csak ugy siman, hanem multithreading-el, hogy ha pl egy 20k*15k méretű
# kép kell neked, akkor az is megy, és az újab optimalizálásaimmal már nem pakol
# tele 45GB ramot, hanem anak csak tizedét

# az output az egy pgm kép, ami azért, mert a python-os képkészítős modulok nem
# akarták az igazat, és pgm-et könnyű manuálisan csinálni, viszont nagy képek esetén
# a 2 mély for loopban res += szam túl sokáig tartana, úgyhogy az is multithreaded

# ha meg akarok egy képet tartani, akkor imageMagic-el png-vé konvertálom és sokkal
# kisebb lesz, tökre jó

# a lentebb látható nagybetűs opciókkal lehet configolni a dolgot:
#   THREADS: mennyi szálat használjon, én 50-el toltam neki, nehogy pihenjen már a laptopom 12 szála
#   WIDTH & HEIGHT: az output PGM kép mérete
#   BOUNTARY_X & BOUNTARY_Y: a complex plane-en számított elhelyezkedése a "kamerának" (origó a középpont, a legszélső pozitív irányú pont megadható)
#   c: a julia set complex paramétere
# a többi nagyjából magátór értetődő

THREADS = (
    50  # minimum 2 kell hogy legyen, a sliceok szelessegenek korrekt kiszamitasahoz
)
PATH = str(pathlib.Path(__file__).parent.resolve()) + "/julia.pgm"


# WIDTH = 50000
# HEIGHT = 32352
WIDTH = 1920
HEIGHT = 1080
C = complex(-0.8, 0.156)

MAX_Z = 5
MAX_ITERATIONS = 255

BOUNTARY_X = 1.7
BOUNTARY_Y = 1.1

BRIGHTNESS = 255

# cmap = cm.get_cmap("gnuplot2")
# cool colors: "YlGnBu", "gnuplot2","inferno","gist_earth","cubehelix", "tab20c"
cmap = cm.get_cmap("tab20c")
LUT = []
for i in range(BRIGHTNESS):
    LUT.append(cmap(i / BRIGHTNESS, bytes=True)[:3])
# LUT = LUT[::-1]


def timeit(
    func,
):  # ezt loptam: https://sureshdsk.dev/python-decorator-to-measure-execution-time
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(
            f"Function {func.__name__}{args[:-1]} {kwargs} Took {total_time:.4f} seconds"
        )  # not printing out the numpy array, that is the last arg
        return result

    return timeit_wrapper


@timeit
def julia(*args):
    # print(args)
    (
        part_width,
        boundary_min,
        boundary_max,
        c,
        array,
    ) = args
    # a képet függőlegesen vágott oszlopokból legózom össze, minden thread egy oszlopon dolgozik
    for i, x in enumerate(numpy.linspace(boundary_min, boundary_max, num=part_width)):
        print(f"{i=}/{part_width}", end="    \r")
        for j, y in enumerate(numpy.linspace(-BOUNTARY_Y, BOUNTARY_Y, num=HEIGHT)):
            z = complex(x, y)

            # print(f"making: {i=}, {j=}, {x=}, {y=}", end="")
            itertations = 0
            while abs(z) <= MAX_Z and itertations < MAX_ITERATIONS:
                z = z ** 2 + c
                itertations += 1

            color = itertations / MAX_ITERATIONS  # mert a grayscale az egyszerű
            array[j, i] = min(int(color * BRIGHTNESS), 254)
            # print(f" {color=}")
    return array


def array_to_string(
    *args,
):  # a numpy array egy vízszintes szeletét alakítja egy hosszó string-gé
    array = args
    res = ""
    for i, row in enumerate(array):
        res += " ".join([str(int(num)) for j, num in enumerate(array[i])])
        res += "\n"
    return res


@timeit
def wrtire_to_pgm(array):
    print("creating image...")
    header = f"P2\n{WIDTH} {HEIGHT}\n{BRIGHTNESS}\n"

    slices = [
        (array[i * HEIGHT // THREADS : (i + 1) * HEIGHT // THREADS, :])
        for i in range(THREADS)
    ]
    # print(slices)

    # a pgm kép készítése is multithreaded, hogy gyorsabban meglegyen, mert nagy
    # képekném már ez is nagyon sokáig tartott
    p = multiprocessing.Pool(THREADS)
    results = p.starmap(array_to_string, slices)
    # print(results)
    p.close()
    p.join()

    res = "".join(results)

    print(f"writing {PATH}...", end="\r")
    with open(PATH, "w") as outFile:
        outFile.write(header)
        outFile.write(res)
    print(f"{PATH} written")


def mp_handler(sum_array, c):
    # mindegyik thread kap egy oszlopt, amin végigmegy
    c_ranges = numpy.linspace(-BOUNTARY_X, BOUNTARY_X, THREADS, endpoint=False)
    range_width = abs(c_ranges[0] - c_ranges[1])
    slice_IDs = []
    for i in range(THREADS):
        slice_start = i * (WIDTH // THREADS)
        slice_width = WIDTH // THREADS
        slice_IDs.append(
            (
                slice_width,
                c_ranges[i],
                c_ranges[i] + range_width,
                c,
                # mostmár nem kap minden thread meg egy teljes méretű aarray-t,
                # hanem csak egy akkorát amibe az ő eredményeit kell pakolnia,
                # ezzel a memórihasználat rengeteget csökkent
                sum_array[:, slice_start : slice_start + slice_width],
            )
        )
    # print(slice_IDs)

    p = multiprocessing.Pool(THREADS + 1)
    results = p.starmap(julia, slice_IDs)
    # print(results)
    p.close()
    p.join()

    # minden thread kap egy full 0 mátrixot, és a végén összelegózom
    print("joining arrays...")
    sum_array = numpy.concatenate(results, axis=1)
    return sum_array


# a c paramétert 2 complex szám között, egy egyenes mentén animálja, és exportál frame_count számú png képet
def anim_ft(frame_count, c_from, c_to):
    for i, c in enumerate(numpy.linspace(c_from, c_to, num=frame_count)):
        print(f"frame {i}...")
        ARRAY = mp_handler(numpy.zeros((HEIGHT, WIDTH)), c).astype(numpy.uint8)
        color_array = numpy.zeros((*ARRAY.shape, 3), dtype=numpy.uint8)
        numpy.take(LUT, ARRAY, axis=0, out=color_array)
        image = Image.fromarray(color_array.astype(numpy.uint8), mode="RGB").save(
            f"sequence/julia_{i:05}.png"
        )


# egy r sugarú körön animálja végig a c paramétert, és frame_count számú képkockát exportál
def anim_circle(frame_count, r):
    for i, a in enumerate(numpy.linspace(0, 2 * numpy.pi, num=frame_count)):
        print(f"frame {i}...")
        c = complex(r * numpy.cos(a), r * numpy.sin(a))
        ARRAY = mp_handler(numpy.zeros((HEIGHT, WIDTH)), c).astype(numpy.uint8)
        color_array = numpy.zeros((*ARRAY.shape, 3), dtype=numpy.uint8)
        numpy.take(LUT, ARRAY, axis=0, out=color_array)
        image = Image.fromarray(color_array.astype(numpy.uint8), mode="RGB").save(
            f"sequence/julia_{i:05}.png"
        )


# csak egy kép a file tetején lévő c paraméterrel
def single_image():
    ARRAY = mp_handler(numpy.zeros((HEIGHT, WIDTH)), C).astype(numpy.uint8)
    color_array = numpy.zeros((*ARRAY.shape, 3), dtype=numpy.uint8)
    numpy.take(LUT, ARRAY, axis=0, out=color_array)
    print("saving to png...")
    image = Image.fromarray(color_array.astype(numpy.uint8), mode="RGB").save(
        "julia.png"
    )


if __name__ == "__main__":
    pass
    # make it go
    single_image()
    # anim_ft(240, complex(0, -0.8), complex(-0.8, 0.156))
    # anim_circle(1024, 0.75)
    # anim_circle(1024, 0.7885)

#       ████████
#     ██▒▒▒▒▒▒▒▒▒▒██
#   ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
# ██▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒██
# ██▒▒▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒██
# ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████
# ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
# ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
# ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#   ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#     ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#     ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#       ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#           ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#               ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
#                   ████████████████
#           this is the bean
