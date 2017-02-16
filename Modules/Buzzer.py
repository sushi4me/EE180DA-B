#------------------------
# Imported Modules
#------------------------
import time
import pyupm_buzzer as upmBuzzer
import mraa as m

#------------------------
#  Buzzer Class
#------------------------
class Buzzer:
    #------------------------
    # Member Variables
    #------------------------
    # Time tick = 1/32 s;  1000000 = 1s
    tick = 31250 
    # Time between notes
    sleeptime = 0.01

    #------------------------
    #  Connected Sound
    #------------------------
    sound_connected = [ 2, 1, 0, 4 ]
    beat_connected = [ 4, 2, 2, 4 ]
    
    #------------------------
    #  Disconnected Sound
    #------------------------
    sound_disconnected = [ 5, 6, 7, 2, 1, 0 ]
    beat_disconnected = [ 3, 4, 5, 6, 7, 7 ]
   
    #------------------------
    #  Shoot
    #------------------------
    sound_shoot = [ 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    beat_shoot = [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ]
    
    #------------------------
    #  Hit
    #------------------------
    sound_hit = [ 8, 0 ]
    beat_hit = [ 12, 8 ]
   
    #------------------------
    # Cloak
    #------------------------
    sound_cloak = [ 0, 8, 0, 7, 0, 6, 0, 5, 0, 4, 0, 3, 0, 2, 0, 1, 0, 0 ]
    beat_cloak = [ 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5 ]

    #------------------------
    # Power Up
    #------------------------
    sound_powerUp = [ 1, 1, 1, 4, 8 ] 
    beat_powerup = [ 4, 4, 4, 32, 16 ] 

    
    def __init__(self):
        self.buzzer = upmBuzzer.Buzzer(0)
        self.chords = [upmBuzzer.DO, upmBuzzer.RE, upmBuzzer.MI, upmBuzzer.FA,
                        upmBuzzer.SOL, upmBuzzer.LA, upmBuzzer.SI, upmBuzzer.DO,
                        upmBuzzer.SI, 4000, 6000];
        self.buzzer.stopSound()
        self.buzzer.setVolume(0.01)

    # Print sensor name
    def getName(self):
        print self.buzzer.name()

    # Play sound
    def play(self, sound, beat):
        for i in range (0, len(sound)):
            print self.buzzer.playSound(self.chords[sound[i]], 
                    beat[i] * self.tick)
            time.sleep(self.sleeptime)

    # Play Connected Sound
    def connected(self):
        self.play(self.sound_connected, self.beat_connected)

    # Play Disconnected Sound
    def disconnected(self):
        self.play(self.sound_disconnected, self.beat_disconnected)
    
    # Play Shoot
    def shoot(self):
        self.play(self.sound_shoot, self.beat_shoot)

    # Play Hit
    def hit(self):
        self.play(self.sound_hit, self.beat_hit)
    
    # Play Cloak
    def cloak(self):
        self.play(self.sound_cloak, self.beat_cloak)

    # Play Power up
    def powerUp(self):
        self.play(self.sound_powerUp, self.beat_powerup)

    def __del__(self):
        del self.buzzer

