# eee

Convert C/C++ source code to eee using preprocessor macros

## Usage
```shell
python eee.py inputfile outputfile
```

it should work with any fairly recent python, I tested it with python 3.10

## Examples

see `./fizzbuzz.c.cpp` --> `./fizzbuzz_eee.c.cpp`:

```c
#include <stdio.h>

int main(void)
{
    int i;
    for(i=1; i<=100; ++i)
    {
        if (i % 3 == 0)
            printf("Fizz");
        if (i % 5 == 0)
            printf("Buzz");
        if ((i % 3 != 0) && (i % 5 != 0))
            printf("number=%d", i);
        printf("\n");
    }

    return 0;
}
```

becomes:

```c
#define e "Fizz"
#define ee "Buzz"
#define eee "number=%d"
#define eeee "\n"
#define eeeee (
#define eeeeee )
#define eeeeeee {
#define eeeeeeee ;
#define eeeeeeeee =
#define eeeeeeeeee <=
#define eeeeeeeeeee ++
#define eeeeeeeeeeee %
#define eeeeeeeeeeeee ==
#define eeeeeeeeeeeeee !=
#define eeeeeeeeeeeeeee &&
#define eeeeeeeeeeeeeeee ,
#define eeeeeeeeeeeeeeeee }
#define eeeeeeeeeeeeeeeeee int
#define eeeeeeeeeeeeeeeeeee main
#define eeeeeeeeeeeeeeeeeeee void
#define eeeeeeeeeeeeeeeeeeeee i
#define eeeeeeeeeeeeeeeeeeeeee for
#define eeeeeeeeeeeeeeeeeeeeeee 1
#define eeeeeeeeeeeeeeeeeeeeeeee 100
#define eeeeeeeeeeeeeeeeeeeeeeeee if
#define eeeeeeeeeeeeeeeeeeeeeeeeee 3
#define eeeeeeeeeeeeeeeeeeeeeeeeeee 0
#define eeeeeeeeeeeeeeeeeeeeeeeeeeee printf
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeee 5
#define eeeeeeeeeeeeeeeeeeeeeeeeeeeeee return
#include <stdio.h>

 eeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeee eeeeee
 eeeeeee
     eeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeee eeeeeeee
     eeeeeeeeeeeeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeee eeeeeeeee eeeeeeeeeeeeeeeeeeeeeee eeeeeeee eeeeeeeeeeeeeeeeeeeee eeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeee eeeeeeee eeeeeeeeeee eeeeeeeeeeeeeeeeeeeee eeeeee
     eeeeeee
         eeeeeeeeeeeeeeeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeee eeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eeeeee
             eeeeeeeeeeeeeeeeeeeeeeeeeeee eeeee e eeeeee eeeeeeee
         eeeeeeeeeeeeeeeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeee eeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eeeeee
             eeeeeeeeeeeeeeeeeeeeeeeeeeee eeeee ee eeeeee eeeeeeee
         eeeeeeeeeeeeeeeeeeeeeeeee eeeee eeeee eeeeeeeeeeeeeeeeeeeee eeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eeeeee eeeeeeeeeeeeeee eeeee eeeeeeeeeeeeeeeeeeeee eeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eeeeee eeeeee
             eeeeeeeeeeeeeeeeeeeeeeeeeeee eeeee eee eeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeee eeeeee eeeeeeee
         eeeeeeeeeeeeeeeeeeeeeeeeeeee eeeee eeee eeeeee eeeeeeee
     eeeeeeeeeeeeeeeee

     eeeeeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeeeeeeeeeeeeeeeeeeeeee eeeeeeee
 eeeeeeeeeeeeeeeee
```

and also see `./example.cpp` --> `example_eee.cpp`
