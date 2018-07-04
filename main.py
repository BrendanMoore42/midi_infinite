import time
import rtmidi
import random

from card import *

"""
rtmidi version = 1.1.0

Cards! to Midi!:

A deck of cards has 52! possible permutations, as to say there are
52 * 51 * 50 ... * 2 * 1 possible orders the deck can have.

About 8.1 x 10^67 possible configurations. 

Which is more than the current estimated age of the universe 
thought to be around 4.42 x 10^17!

So how cool would it be to have each unique shuffled deck play it's own 
unique melody...blasting out something like 8 Septensexagintillion 
possible combinations?

Requirements:
- Rtmidi @ http://www.music.mcgill.ca/~gary/rtmidi/index.html
    -Python-rtmidi
    -Xcode (if OSx)
- Midi controller
    - M-Audio USB (for output to MIDI devices)
    - Virtual Midi port if supported by target DAW  
    
Other:
- 120 bpm default 
    - Conversion chart: https://msu.edu/course/asc/232/song_project/dectalk_pages/note_to_%20ms.html
- Suits type of note, Hearts = 16th, Spades = 8th, Clubs = Half, Diamonds = Dotted Half

"""

def create_deck():
    cards = [(v, s) for s in ['H', 'S', 'C', 'D']
             for v in [int(i) for i in range(1, 14)]]
    random.shuffle(cards)
    return list(cards)


def create_midi_input(deck):
    """
    Returns a list of notes in the format taken by rtmidi:
        [channel, note, velocity]

    Note - card values can be shifted +/- to bring notes within more
    pleasant listening ranges. +40 is a good middle balance.
    """
    song_list = []
    ch = 0x90
    print(f"Shuffled deck: {deck}")

    for card, suit in deck:
        song_list.extend([[ch, card+40, 100]])

    print(f'Midi out: {song_list}')
    return song_list


def midi_off_deck(deck):
    """
    Midi must be depressed after pressed, or note will hold. This fn
    takes the same note from the current card deck and turns the velocity
    to 0 and close the channel.
    """
    song_list_off = []
    closed_ch = 0x80
    vel = 0

    for card, suit in deck:
        song_list_off.extend([[closed_ch, card+40, vel]])

    return song_list_off


def add_rests(deck):
    """
    Takes the suit and converts that to a beat:
    Hearts = 16th, Spades = 8th, Clubs = Half, Diamonds = Dotted Half
    """
    rest_time = []
    #h=16th, s=8th, c=1/2, d=d1/2 @ 120bpm
    h, s, c, d = 0.125, 0.250, 1, 1.5

    for suit in deck:
        if suit[1] == 'H':
            rest_time.append(h)
        if suit[1] == 'S':
            rest_time.append(s)
        if suit[1] == 'C':
            rest_time.append(c)
        if suit[1] == 'D':
            rest_time.append(d)

    return rest_time


def main():
    """
    Main fn, creates deck, assigns values, rests and midi points
    """

    # note_on = [0x90, 14, 112] # channel 1, middle C, velocity 112
    # note_off = [0x80, 14, 0]

    deck = create_deck()

    deck_midi_out = list(create_midi_input(deck))
    rest_to_add = add_rests(deck)
    rest_times = [i for i in rest_to_add]

    off_deck = list(midi_off_deck(deck))

    user_input = input(('Play track? (y/n)?'))

    if user_input == 'y':

        midiout = rtmidi.MidiOut()
        available_ports = midiout.get_ports()

        """Looks for active midi, if none found opens virtual port...
        Set up of a virtual port for garageband through Audio Midi Setup
        """
        if available_ports:
            midiout.open_port(0)
        else:
            midiout.open_virtual_port("My virtual output")

        for note, rest, note_off in zip(deck_midi_out, rest_times, off_deck):
            midiout.send_message(note)
            time.sleep(rest)
            midiout.send_message(note_off)
            print(note)
            print(rest)

        play_again = input('Play again? (y/n)?')
        if play_again == 'y':
            main()
        if play_again == 'n':
            print('Maybe next time.')
        del midiout

    if user_input == 'n':
        print('Suit yourself.')

if __name__ == '__main__':
    main()

