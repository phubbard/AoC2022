const struct sensor_t sensors = {
    {.location_x=2, .location_y=18, .distance=7}
    {.location_x=9, .location_y=16, .distance=1}
    {.location_x=13, .location_y=2, .distance=3}
    {.location_x=12, .location_y=14, .distance=4}
    {.location_x=10, .location_y=20, .distance=4}
    {.location_x=14, .location_y=17, .distance=5}
    {.location_x=8, .location_y=7, .distance=9}
    {.location_x=2, .location_y=0, .distance=10}
    {.location_x=0, .location_y=11, .distance=3}
    {.location_x=20, .location_y=14, .distance=8}
    {.location_x=17, .location_y=20, .distance=6}
    {.location_x=16, .location_y=7, .distance=5}
    {.location_x=14, .location_y=3, .distance=1}
    {.location_x=20, .location_y=1, .distance=7}
};

const int search_extent = 20;

const int expected_answer = 56000011;

const int frequency_x_scalar = 4000000;