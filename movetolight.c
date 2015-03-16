#include <kilolib.h>

#define LEFT 0
#define RIGHT 1

// declare constants
// The more the kilobot faces away from the light source, the less
// higher the value returned by the analog-to-digital converter will be. 
static const uint16_t THRESH_HI = 600;
static const uint16_t THRESH_LO = 300;

// declare variables
uint8_t cur_direction;
int16_t cur_light = 0;

// To reduce noise we take the average of 300 samples, discarding
// samples where the ADC sensor failed (returned -1).
void sample_light() {
    int16_t numsamples = 0;
    long average = 0;

    while (numsamples < 300) {
        int16_t sample = get_ambientlight();
        if (sample != -1) {
            average += sample; // average numerator
            numsamples++;
        }
    }

    cur_light = average / 300; // average calculation
}

void turn_left() {
    spinup_motors();
    set_motors(kilo_turn_left, 0);
    set_color(RGB(2,0,0));
}

void turn_right() {
    spinup_motors();
    set_motors(0, kilo_turn_right);
    set_color(RGB(0,2,0));
}


void setup() {
    cur_direction = LEFT;
    turn_left();
}

void loop() {
    sample_light(); // get the average ambient light value
    switch(cur_direction) {
        case LEFT:
            if (cur_light < THRESH_LO) { // kilobot facing away from the light source
                cur_direction = RIGHT;
                turn_right();
            }
            break;
        case RIGHT:
            if (cur_light > THRESH_HI) { // kilobot facing directly at the light source
                cur_direction = LEFT;
                turn_left();
            }
            break;
    }
}

int main() {
    kilo_init();
    kilo_start(setup, loop);

    return 0;
}
