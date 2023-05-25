# MIDI Maestro
Turn your ghastly piano playing :musical_keyboard: :man_facepalming: into something beautiful :sparkles: at the press of a button (well almost)!

Simply select a piece and off you go. We'll fix all your mistakes for you as long as you get the rhythm right.

Show off to all your friends an nobody will suspect a thing. :innocent:


## :sparkles: Features
- Connect MIDI Maestro to your favorite VST instrument
- Select an input MIDI port
- Select a piece to play
- Add more pieces of your choice
- Play your interpretation:
    - You control the rhythm
    - You control the dynamics
- Play chords:
    - Detects when you play a chord
    - Detects a chord in the MIDI file
- Dynamic velocity:
    - Matches your input velocity
    - Maintains the differences in velocity within chords


## :rocket: Getting Started
1. First let's install the required python libraries. Open up a terminal and enter these lines:
    ```
    pip3 install mido
    pip3 install python-rtmidi
    ```

2. Now we can start the program:
    ```
    python3 /PATH_TO/MIDI-Maestro/main.py
    ```

    You should see:
    ```
    Started a virtual MIDI port called 'MIDI Maestro'.
    Set the input of your VST instrument to this port.
    ```

3. Open your VST instrument of choice. Set the input of the instrument to "MIDI Maestro".

4. Back in your terminal you should see something like:
    ```
    Available MIDI ports:

        [1] KeyLab mkII 88 MIDI

    Select a MIDI input port (1-1):
    ```
    Type in the number of your keyboard port and hit `ENTER`.

5. Select the piece you wish to play the same way as before:
    ```
    Available pieces:

        [1] Chopin - Prelude No 4

    Select a piece (1-1): 1
    Using piece 'Chopin - Prelude No 4'

    Start playing... (CTRL+C to cancel)
    ```
6. Now just start playing!


## :musical_note: Adding more pieces
You can add more pieces as MIDI files. Simply copy your MIDI file into the `MIDI-Maestro/MIDI` folder.

Pieces that work best:
- Easy rhythm
- Similar rhythm all the way through
- No trills or other ornaments
- Mostly legato (staccato doesn't work unless you play fast)

You can of course use any piece you like.

Depending on the way the MIDI file is formatted it might not work as expected (MIDI files from MuseScore are known to have issues). You can try importing the MIDI file into your DAW and exporting it again. MIDI files of type 0 with a high resolution work best.

If you find that some notes are played together instead of individually or vice versa, you can try tuning the `SENSITIVITY` at the top of `main.py`.


## :heavy_plus_sign: Contributing
### Contributing MIDI files
Let everyone join in the fun! Please feel free to contribute MIDI files by opening a pull-request!

But please remember...
- TEST the MIDI file before trying to contribute.
- DO NOT try to contribute songs/pieces that are subject to copyright (most modern songs).
- DO NOT try to contribute arrangements of songs that are subject to copyright.
- DO NOT try to contribute MIDI files that are subject to copyright.
- If the MIDI file is open source please upload the license as well as the MIDI file in a subfolder.
- By contributing a MIDI file that you created yourself you are making that file open source with no copyright. If you wish to be credited please upload the MIDI file with an open-source LICENSE in a subfolder.

### Contributing to the code
Issues? Bugs? Feature requests? Just open an issue.

Know a way of improving the code? Go ahead and open a pull-request.