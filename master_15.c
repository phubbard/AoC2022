

#include "stdio.h"
#include "stdlib.h"

struct sensor_t {
    int location_x;
    int location_y;
    int distance;
};

#include "massaged_sensor_15.c"

int main()
{
    const int sensor_extent = sizeof(sensors) / sizeof(sensors[0]);
    printf("Starting with %d elements...\n", sensor_extent);
    int x;
    int y;
    int s;
    for (x = 0; x < search_extent; x++)
    {
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

