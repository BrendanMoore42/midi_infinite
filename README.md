## Midi Infinity

Shuffles a deck of cards then outputs a song generated from the card order.

#### Overview
Cards! to Midi!:

A deck of cards has 52! possible permutations - there are
52 * 51 * 50 ... * 2 * 1 possible orders the deck can have.

52! = 8.1 x 10^67 possible configurations. 

The current estimated age of the universe 
is currently around 4.42 x 10^17, much less than the
possible ordering to a shuffled deck of cards.

Leaving a possible Eight-Septensexagintillion possible
combinations of the generated melody.
    
#### Requirements

Rtmidi @ http://www.music.mcgill.ca/~gary/rtmidi/index.html
   - Python-rtmidi
   - Xcode (if OSx)
   - rtmidi version = 1.1.0
Midi controller
   - M-Audio USB (for output to MIDI devices)
   - Virtual Midi port if supported by target DAW 
Other:
   - 120 bpm default 
   - Conversion chart: https://msu.edu/course/asc/232/song_project/dectalk_pages/note_to_%20ms.html
Suits == type of note: 
  - Hearts = 16th 
  - Spades = 8th
  - Clubs = Half 
  - Diamonds = Dotted Half
