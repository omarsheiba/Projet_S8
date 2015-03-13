#include <kilolib.h>

/*
This function mixes communication and motion. Whenever a message is received, the bot moves in different ways.
It has 3 possibilities: - 50% chances to moving forward
                        - 25% chances to turn left
                        - 25% chances to turn right
*/

// declare constants
#define STOP 0
#define FORWARD 1
#define LEFT 2
#define RIGHT 3

// declare variables
uint8_t cur_motion = STOP;
uint8_t new_message=0;
message_t msg;

//function to set new motion
void set_motion(uint8_t new_motion){
    if(cur_motion!=new_motion){
        
        cur_motion=new_motion;
        
        switch(cur_motion){
            
            case STOP:
                set_motors(0,0);
                break;
            
            case FORWARD:
                spinup_motors();
                set_motors(kilo_straight_left,kilo_straight_right);
                break;
            
            case LEFT:
                spinup_motors();
                set_motors(kilo_turn_left,0);
                break;
            
            case RIGHT:
                spinup_motors();
                set_motors(0,kilo_turn_right);
                break;
        }
    }
}

void setup() {
// initialize empty message
msg.type = NORMAL;
msg.crc = message_crc(&msg);
}

void loop() {
    if(new_message){
        //generate a random 8-bit number and extract a random 2-bit-number
        const uint8_t twobit_mask = 0b00000011;
        uint8_t rand_direction = rand_soft()&twobit_mask;
        
        if(rand_direction == 0 || rand_direction == 1){
            set_color(RGB(1,0,0));
            set_motion(FORWARD);
        }
        else if (rand_direction == 2){
            set_color(RGB(0,1,0));
            set_motion(LEFT);
        }
        else if (rand_direction == 3){
            set_color(RGB(0,0,1));
            set_motion(RIGHT);
        }
        delay(100);
        set_motion(STOP);
        new_message = 0;
    }
   
}

void message_rx(message_t *m, distance_measurement_t *d){
    new_message = 1;
}

message_t *message_tx(){
    return &msg;
}

int main() {
    kilo_init();
    kilo_message_rx = message_rx;
    kilo_message_tx = message_tx;
    kilo_start(setup, loop);

    return 0;
}
