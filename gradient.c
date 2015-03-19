#include <kilolib.h>

uint32_t last_changed = 0;
uint16_t gradient_value = UINT16_MAX; //largest value an uint16_t can hold.
uint16_t recvd_gradient = 0;
uint8_t new_message = 0;
message_t msg;

void message_rx(message_t *m, distance_measurement_t *d) {
    new_message = 1;
    // unpack two 8-bit integers into one 16-bit integer
    // <<8 shifts the data[1] by 8 bit to left 
    recvd_gradient = m->data[0]  | (m->data[1]<<8);
}

message_t *message_tx() {
    if (gradient_value != UINT16_MAX) // I'm not the max gradient holder
        return &msg;
    else
        return '\0'; 
}

void update_message() {
    // pack one 16-bit integer into two 8-bit integers
    // &0xFF = 0...011111111
    msg.data[0] = gradient_value & 0xFF;
    msg.data[1] = (gradient_value>>8) & 0xFF;
    msg.crc = message_crc(&msg);
}

void setup() {

    if (kilo_uid == 1000){ // I'm the root kilobot
        set_color(RGB(1,1,1));
        gradient_value = 0;
    }
    update_message();

}

void loop() {
    if (new_message) {
        
        if (gradient_value > recvd_gradient+1) {
            gradient_value = recvd_gradient+1;
            update_message();
        }
        /*else if (gradient_value < recvd_gradient - 1){
            gradient_value = recvd_gradient -1;
            update_message();
        }*/

        new_message = 0;
        switch(gradient_value%3) {
            case 0:
                set_color(RGB(1,0,0));
                break;
            case 1:
                set_color(RGB(0,1,0));
                break;
            case 2:
                set_color(RGB(0,0,1));
                break;
        }

        /*if (kilo_ticks >= last_changed + 96)
            last_changed = kilo_ticks;
            if (gradient_value < recvd_gradient -1){
                gradient_value = recvd_gradient - 1;
                update_message();
            }
        switch(gradient_value%3) {
            case 0:
                set_color(RGB(1,0,0));
                break;
            case 1:
                set_color(RGB(0,1,0));
                break;
            case 2:
                set_color(RGB(0,0,1));
                break;
        }*/
        
    }
}

int main() {
    // initialize hardware
    kilo_init();
    // register message callbacks
    kilo_message_rx = message_rx;
    kilo_message_tx = message_tx;
    // register your program
    kilo_start(setup, loop);

    return 0;
}
