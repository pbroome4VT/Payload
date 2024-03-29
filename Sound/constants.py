import Sound.helper as h


#frequencies of various notes
NOTE_00 = 1
NOTE_C2 = 65
NOTE_D2 = 73
NOTE_E2 = 82
NOTE_F2 = 87
NOTE_G2 = 98
NOTE_A2 = 110
NOTE_B2 = 123
NOTE_C3 = 131
NOTE_D3 = 147
NOTE_E3 = 165
NOTE_F3 = 175
NOTE_G3 = 196
NOTE_A3 = 220
NOTE_B3 = 247
NOTE_C4 = 261   #middle C
NOTE_D4 = 294
NOTE_E4 = 330
NOTE_F4 = 349
NOTE_G4 = 392
NOTE_A4 = 440
NOTE_B4 = 493
NOTE_C5 = 523
NOTE_D5 = 587
NOTE_E5 = 659
NOTE_F5 = 698
NOTE_G5 = 784
NOTE_A5 = 880
NOTE_B5 = 988
NOTE_C6 = 1045

#note duration in beats
NOTE_32 = 0.125
NOTE_16  = 0.25
NOTE_8 = 0.5
NOTE_4 = 1.0
NOTE_2 = 2.0
NOTE_1 = 4.0
NOTE_N2 = 8.0

HAPPY_BIRTHDAY_NOTES=[
 [NOTE_C4,NOTE_8], [NOTE_C4, NOTE_8],   #b1
 [NOTE_D4, NOTE_4], [NOTE_C4, NOTE_4], [NOTE_F4, NOTE_4],   #b2
 [NOTE_E4, NOTE_2], [NOTE_C4, NOTE_8], [NOTE_C4, NOTE_8],   #b3
 [NOTE_D4, NOTE_4], [NOTE_C4, NOTE_4], [NOTE_G4, NOTE_4],   #b4
 [NOTE_F4, NOTE_2], [NOTE_C4, NOTE_8], [NOTE_C4, NOTE_8],   #b5
 ]
HAPPY_BIRTHDAY_BPM = 95.0

THUNDERSTRUCK_NOTES = [
   [NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16], #b1
   [NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16], #b2
   [NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16], #b3
   [NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16], #b4
   [NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16], #b5
   [NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_D4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_F4,NOTE_16],[NOTE_B3,NOTE_16], #b6
   [NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16], #b7
   [NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_E4,NOTE_16],[NOTE_B3,NOTE_16],[NOTE_G4,NOTE_16],[NOTE_B3,NOTE_16], #b8
   ]
THUNDERSTRUCK_BPM = 150

FINAL_COUNTDOWN_NOTES=[
   [NOTE_F3, NOTE_4],[NOTE_C5, NOTE_16], [NOTE_B5, NOTE_16],[NOTE_C5, NOTE_16],[NOTE_F4, NOTE_4],
   [NOTE_D3, NOTE_4], [NOTE_D5, NOTE_16], [NOTE_C5, NOTE_16],[NOTE_D5, NOTE_8],[NOTE_C5, NOTE_8],[NOTE_B5, NOTE_4],
   [NOTE_B3, NOTE_4],[NOTE_D5,NOTE_16],[NOTE_C5, NOTE_16],[NOTE_D5, NOTE_4],[NOTE_F4, NOTE_4],
   [NOTE_E3, NOTE_4],[NOTE_B4, NOTE_16], [NOTE_A4, NOTE_16],[NOTE_B4, NOTE_8],[NOTE_A4, NOTE_8],[NOTE_G4, NOTE_8], [NOTE_B4, NOTE_8],
   [NOTE_F3, NOTE_4],[NOTE_C5, NOTE_16], [NOTE_B5, NOTE_16],[NOTE_C5, NOTE_16],[NOTE_F4, NOTE_4],
   [NOTE_D3, NOTE_4], [NOTE_D5, NOTE_16], [NOTE_C5, NOTE_16],[NOTE_D5, NOTE_8],[NOTE_C5, NOTE_8],[NOTE_B5, NOTE_4],
   [NOTE_B3, NOTE_4],[NOTE_D5,NOTE_16],[NOTE_C5, NOTE_16],[NOTE_D5, NOTE_4],[NOTE_F4, NOTE_4],
   [NOTE_E3, NOTE_4],[NOTE_B4, NOTE_16], [NOTE_A4, NOTE_16],[NOTE_B4, NOTE_8],[NOTE_A4, NOTE_8],[NOTE_G4, NOTE_8], [NOTE_B4, NOTE_8],
   [NOTE_A4, NOTE_4], [NOTE_G4, NOTE_16], [NOTE_A4, NOTE_16],[NOTE_B4, NOTE_4], [NOTE_A4, NOTE_16],[NOTE_B4, NOTE_16],
   [NOTE_C5, NOTE_16],[NOTE_B4, NOTE_16],[NOTE_A4, NOTE_16],[NOTE_G4,NOTE_16],[NOTE_F4, NOTE_4],[NOTE_D5, NOTE_4],
   [NOTE_C5, NOTE_2],[NOTE_D5, NOTE_16],[NOTE_C5,NOTE_16],[NOTE_B5,NOTE_16],[NOTE_C5, NOTE_16],
   [NOTE_C5, NOTE_2],
   [NOTE_00, NOTE_4]
]
FINAL_COUNTDOWN_BPM = 120


WINDOWS_STARTUP_NOTES=[
   [NOTE_D5, NOTE_16],[NOTE_00, NOTE_16],[NOTE_C5, NOTE_8],[NOTE_G3, NOTE_2],[NOTE_E2, NOTE_32],[NOTE_00,NOTE_32],[NOTE_G2,NOTE_32],[NOTE_00,NOTE_32],[NOTE_D3,NOTE_32],[NOTE_00,NOTE_32],[NOTE_G3,NOTE_16]
]
WINDOWS_STARTUP_BPM = 89

STARTUP_SOUND_NOTES=[
   [NOTE_C6, NOTE_4], [NOTE_C5, NOTE_4], [NOTE_C4,NOTE_4], [NOTE_C3,NOTE_4], [NOTE_C2, NOTE_4]]
STARTUP_SOUND_BPM = 60

BEEP_NOTES = [[NOTE_C3, NOTE_4]]
BEEP_BPM = 60