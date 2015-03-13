#include <kilolib.h>
/*Broadcast a message continuously.*/

// declare variables
message_t transmit_msg;
//flag that anounces the sending of a message
uint8_t message_sent = 0;



void setup() {
    // setup code, to be run only once
    transmit_msg.type = NORMAL;
    transmit_msg.crc = message_crc(&transmit_msg);
}

void loop() {
    // main code, to be run repeatedly
    if (message_sent == 1){
        message_sent = 0;
        set_color(RGB(1,0,1));
        delay(20);
        set_color(RGB(0,0,0));
    }
}

message_t *message_tx(){
    return &transmit_msg;
}

void message_tx_success(){
    message_sent=1;
}

int main() {
    // initialize hardware
    kilo_init();
    kilo_message_tx = message_tx;
    kilo_message_tx_success = message_tx_success;
    // start program
    kilo_start(setup, loop);

    return 0;
}
