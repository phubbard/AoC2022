

#include "stdio.h"
#include "stdlib.h"

#include "unistd.h"
#include "omp.h"

struct sensor_t {
    int location_x;
    int location_y;
    int distance;
};

#include "massaged_sensor_15_final.c"

int main()
{
    printf("Openmp test...\n");
#pragma omp parallel num_threads(4)
    printf("Hellow from thread %d in process %d.\n",
           omp_get_thread_num(), getpid());

    const int sensor_extent = sizeof(sensors) / sizeof(sensors[0]);
    printf("Starting with %d elements...\n", sensor_extent);

    int x;
#pragma omp parallel for private(x)
    for (x = 0; x < search_extent; x++)
    {
        int y;
        int s;

        if (0 == (x % 100000))
        {
            printf("Startin on row %d\n", x);
        }
        for (y = 0; y < search_extent; y++)
        {
            int is_covered = 0;
            for (s = 0; s < sensor_extent; s++)
            {
                const struct sensor_t* sensor = &sensors[s];

                const int delta_x = abs(sensor->location_x - x);
                const int delta_y = abs(sensor->location_y - y);
                const int manhattan = delta_x + delta_y;
                is_covered = (manhattan <= sensor->distance);
                if (is_covered) break;
            }
            if (!is_covered)
            {
                const int frequency = frequency_x_scalar * x + y;
                printf("For %d, %d -> %d\n", x, y, frequency);
            }
        }
    }
    return 0;
}


/*
$ time ./do_15_winblows.sh
./do_15_winblows.sh: line 2: $'\r': command not found
Generating...
': [Errno 2] No such file or directoryhome/bhyslop/phubbard_AoC2022/15.py
Building...
Running...
Openmp test...
Hellow from thread 1 in process 152.
Hellow from thread 2 in process 152.
Hellow from thread 0 in process 152.
Hellow from thread 3 in process 152.
Starting with 32 elements...
Startin on row 0
Startin on row 2700000
Startin on row 1700000
Startin on row 3700000
Startin on row 2400000
Startin on row 700000
Startin on row 2100000
Startin on row 1400000
Startin on row 3400000
Startin on row 2800000
Startin on row 1800000
Startin on row 400000
Startin on row 2500000
Startin on row 3100000
Startin on row 2200000
Startin on row 1100000
Startin on row 1900000
Startin on row 2600000
Startin on row 2900000
Startin on row 3800000
Startin on row 800000
Startin on row 1500000
Startin on row 2300000
Startin on row 3500000
Startin on row 2000000
Startin on row 3200000
Startin on row 100000
For 2960219, 3211051 -> -345624021
Startin on row 1200000
Startin on row 500000
Startin on row 1600000
Startin on row 3000000
Startin on row 900000
Startin on row 3900000
Startin on row 3600000
Startin on row 1300000
Startin on row 3300000
Startin on row 600000
Startin on row 1000000
Startin on row 200000
Startin on row 300000
Done, no errors.
./do_15_winblows.sh: line 10: $'\r': command not found
./do_15_winblows.sh: line 11: $'\r': command not found
./do_15_winblows.sh: line 12: $'\r': command not found

real    564m25.169s
user    4788m59.247s
sys     3m51.275s
*/

