#include <kilolib.h>

// declare constants
static const uint8_t TOOCLOSE_DISTANCE = 45; // 40 mm
static const uint8_t DESIRED_DISTANCE = 65; // 60 mm

// declare motion variable type
typedef enum {
    STOP,
    FORWARD,
    LEFT,
    RIGHT
} motion_t;

// declare state variable type
typedef enum {
    ORBIT_TOOCLOSE,
    ORBIT_NORMAL,
} orbit_state_t;

uint16_t gradient_value = UINT16_MAX;
uint16_t recvd_gradient = 0;
uint8_t new_message = 0;
message_t msg;

uint8_t message_sent = 0;

// orbit
// declare variables
motion_t cur_motion = STOP;
orbit_state_t orbit_state = ORBIT_NORMAL;
uint8_t cur_distance = 0;
distance_measurement_t dist;

/*                      Partie orbit                             */
// function to set new motion
void set_motion(motion_t new_motion) {
    if (cur_motion != new_motion) {
        cur_motion = new_motion;
        switch(cur_motion) {
            case STOP:
                set_motors(0,0);
                break;
            case FORWARD:
                spinup_motors();
                set_motors(kilo_straight_left, kilo_straight_right);
                break;
            case LEFT:
                spinup_motors();
                set_motors(kilo_turn_left, 0); 
                break;
            case RIGHT:
                spinup_motors();
                set_motors(0, kilo_turn_right); 
                break;
        }
    }
}

void orbit_normal() {
    if (cur_distance < TOOCLOSE_DISTANCE) {
        orbit_state = ORBIT_TOOCLOSE;
    } else {
        if (cur_distance < DESIRED_DISTANCE)
            set_motion(LEFT);
        else
            set_motion(RIGHT);
    }
}

void orbit_tooclose() {
    if (cur_distance >= DESIRED_DISTANCE)
        orbit_state = ORBIT_NORMAL;
    else
        set_motion(FORWARD);
}
/*                       Fin partie orbit                        */


void message_rx(message_t *m, distance_measurement_t *d) {
    new_message = 1;
    // unpack two 8-bit integers into one 16-bit integer
    recvd_gradient = m->data[0]  | (m->data[1]<<8);
    dist = *d;
}

message_t *message_tx() {
    if (gradient_value != UINT16_MAX)
        return &msg;
    else
        return '\0';
}

void update_message() {
    // pack one 16-bit integer into two 8-bit integers
    msg.data[0] = gradient_value&0xFF;
    msg.data[1] = (gradient_value>>8)&0xFF;
    msg.crc = message_crc(&msg);
}

void setup() {
    if (kilo_uid == 1000)
        gradient_value = 0;
    update_message();

    if (kilo_uid == 2000){
        set_color(RGB(1,1,1));
        delay(20);
        set_color(RGB(0,0,0));
    }
}

void loop() {
    if (new_message && kilo_uid != 2000) {
        if (gradient_value > recvd_gradient+1) {
            gradient_value = recvd_gradient+1;
            update_message();
        }
        new_message = 0;
        switch(gradient_value%6) {
            case 0:
                set_color(RGB(1,0,0));
                break;
            case 1:
                set_color(RGB(0,1,0));
                break;
            case 2:
                set_color(RGB(0,1,1));
                break;
            case 3:
                set_color(RGB(0,0,1));
                break;
            case 4:
                set_color(RGB(1,0,1));
                break;
            case 5:
                set_color(RGB(1,1,0));
                break;
        }
    }

    if (kilo_uid == 2000){
        if (new_message && recvd_gradient == 0) {
            new_message = 0;
            cur_distance = estimate_distance(&dist);
        } 
        else (cur_distance == 0) // skip state machine if no distance measurement available
            return;

    // Orbit state machine
        switch(orbit_state) {
            case ORBIT_NORMAL:
                orbit_normal();
                break;
            case ORBIT_TOOCLOSE:
                orbit_tooclose();
                break;
        }
        if (gradient value < recvd_gradient){ // si je reçois un grad superieur
            gradient_value = recvd_gradient; // je prends cette valeur de grad
            
        }
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

/*
Revoir les titres
sdoit donner le nom du contexte 
sinon mettre seulement "the context"
revoir le titre : c'est trop vague
revoir abstract, faire plutot un resume du sujet, resumer le contenu
du projet, qd je lis l abstract je dois etre attiré par le sujet et
savoir ce que je vais lire

faut faire des choix, on detaille plus un des algos 

Faire un rapport technique qu'on rendra a travers par algo. 


DONE revenir sur l'exemple du code et dire qu il y a des propriétés globales 
observes. 

essayer de citer des articles 

mettre en avant la problématique - dire ce qu'on a dû faire - 

DONE Visidia c'est plus general.

DONE dire le nom du simulateur sur matlab 

DONE essayer par exemple de faire plusieurs categories de simulateurs 
(du general au moins general) et dire pourquoi ils sont eliminés 

preciser le fait que ces algos existent deja et qu'on les remanie. 

*/
