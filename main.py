import mido
import time
import sys
from glob import glob

# How many ticks between notes before the notes should
# no longer be counted as a chord.
#
# For example if SENSITIVITY = 0.05:
# 2 Notes are 0.02 ticks apart => chord
# 2 Notes are 0.1 ticks apart => seperate (need to be played indiviually)
SENSITIVITY = 0.05


def get_inport():
    """
    Asks the user to select a MIDI port and returns the selected port.
    """

    # Fetch a list of all the available input ports
    port_names = mido.get_input_names()
    port_names.remove("MIDI Maestro")

    # Close the program if no ports are available
    if len(port_names) == 0:
        print("There are no MIDI ports available.")
        sys.exit()

    # Print out the ports with a given number for the user to select from.
    print("\nAvailable MIDI ports:\n")
    for x in range(0, len(port_names)):
        print(f"    [{x+1}] {port_names[x]}")

    # Ask the user to select a port by entering one of the given numbers.
    selected_index = 0
    try:
        selected_index = (
            int(input(f"\nSelect a MIDI input port (1-{len(port_names)}): ")) - 1
        )

        # Default to the first port if the value entered is invalid.
        if selected_index < 0 or selected_index > len(port_names) - 1:
            selected_index = 0
    except ValueError:
        pass

    # Inform the user of their choice and return the selected port.
    print(f"Using MIDI port '{port_names[selected_index]}'\n")
    return mido.open_input(port_names[selected_index])


def get_midi_file():
    """
    Asks the user to select a MIDI file and returns the selected file.
    """

    # Fetch a list of all the available MIDI files.
    file_names = glob("./MIDI/**/*.midi", recursive=True)
    pretty_file_names = []

    # Close the program if no files are available
    if len(file_names) == 0:
        print("There are no MIDI files available.")
        sys.exit()

    # Print out the files with a given number for the user to select from.
    print("\nAvailable pieces:\n")
    for x in range(0, len(file_names)):
        pretty_file_names.append(file_names[x].split("/")[-1].removesuffix(".midi"))
        print(f"    [{x+1}] {pretty_file_names[x]}")

    # Ask the user to select a file by entering one of the given numbers.
    selected_index = 0
    try:
        selected_index = int(input(f"\nSelect a piece (1-{len(file_names)}): ")) - 1

        # Default to the first file if the value entered is invalid.
        if selected_index < 0 or selected_index > len(file_names) - 1:
            selected_index = 0
    except ValueError:
        pass

    # Inform the user of their choice and return the selected file.
    print(f"Using piece '{pretty_file_names[selected_index]}'\n")
    return mido.MidiFile(file_names[selected_index])


def clear_inport(inport):
    """
    Clears the given port of any pending messages.

    • `inport`: the MIDI port to clear
    """
    for msg in inport.iter_pending():
        pass


def validate_msg(msg):
    """
    Returns true if the given message type is NOTE_ON or NOTE_OFF.

    • `msg`: the MIDI message to validate
    """
    return (
        not msg.is_meta
        and (msg.type == "note_on" or msg.type == "note_off")
        and hasattr(msg, "velocity")
    )


def play_next_chord(msgs, msg_index, in_velocity, outport):
    """
    Itentifies the next chord and returns the current position in the list of MIDI messages.

    • `msgs`: the list of MIDI messages from the MIDI file
    • `msg_index`: the current position in the list of MIDI messages
    • `in_velocity`: the velocity with which to play the chord
    • `outport`: the MIDI port to send the messages to
    """

    # This will contain all the messages for a chord.
    msg_buffer = []

    # Loop through the MIDI messages.
    while msg_index < len(msgs):
        # Fetch the latest message.
        msg = msgs[msg_index]

        # Play all the messages in the buffer if this is the last message
        if msg_index == len(msgs) - 1:
            msg_buffer.append(msg)
            for buf_msg in msg_buffer:
                outport.send(buf_msg)

            # This will cause this loop and the loop in play_midi_file to break.
            msg_index += 1

        # Play the messages in the buffer if the message time is > 0.05.
        # Note: msg.time is in ticks not seconds.
        if msg.time > SENSITIVITY and len(msg_buffer) > 0:
            # Calculate the average velocity of the chord.
            total_velocity = 0
            note_on_count = 0

            for buf_msg in msg_buffer:
                if buf_msg.type == "note_on" and buf_msg.velocity > 0:
                    total_velocity += buf_msg.velocity
                    note_on_count += 1

            # Don't play the messages in the buffer if all the message types are NOTE_OFF.
            if note_on_count == 0:
                msg_buffer.append(msg)
                msg_index += 1
                continue

            avg_velocity = total_velocity / note_on_count

            # Play the messages in the buffer.
            for buf_msg in msg_buffer:
                # Raise or lower the velocity to match the velocity of the user
                # while still maintaining the velocity differences in the chord.
                if buf_msg.type == "note_on" and buf_msg.velocity > 0:
                    newVelocity = int(buf_msg.velocity + (in_velocity - avg_velocity))
                    if newVelocity < 0:
                        newVelocity = 0
                    elif newVelocity > 127:
                        newVelocity = 127
                    buf_msg.velocity = newVelocity

                # Play the msg from the buffer.
                outport.send(buf_msg)
            break

        # Add the message to the buffer if the message time is <= 0.05.
        msg_buffer.append(msg)
        msg_index += 1

    return msg_index


def play_midi_file(midi_file, outport):
    """
    Iterates through the chords in the given MIDI files when the user plays a chord.

    • `midi_file`: the MIDI file to play
    • `outport`: the MIDI port to send the messages to
    """

    # Load the messages from the MIDI file.
    msgs = [msg for msg in midi_file if validate_msg(msg)]

    # Reset the index of the current message from the MIDI file.
    msg_index = 0

    # Clear the inport of any pending messages.
    clear_inport(inport)

    # Inform the user that we're ready.
    print("\nStart playing... (CTRL+C to cancel)\n")

    # Loop through all the messages from the MIDI file.
    while msg_index < len(msgs):
        try:
            # Wait for a message from the inport.
            in_msg = inport.receive()

            # Return to the start of the loop if the message is not valid.
            if (
                not validate_msg(in_msg)
                or in_msg.type == "note_off"
                or in_msg.velocity == 0
            ):
                continue

            # Play the next chord from the MIDI file.
            msg_index = play_next_chord(msgs, msg_index, in_msg.velocity, outport)

            # Clear the inport of any additional messages that occur when the user plays a chord.
            time.sleep(0.05)
            clear_inport(inport)

        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    print(
        """

    
       ################     ####   ##############     ####
       ##################   ####   ################   ####
       ####   ####   ####   ####               ####   ####
       ####   ####   ####   ####   ####        ####   ####
       ####   ####   ####   ####   ####        ####   ####
       ####   ####   ####   ####   ####        ####   ####
       ####   ####   ####   ####   ################   ####
       ####   ####   ####   ####   ###############    ####

    #########   #####   ######  ######  ######  #####   #####
    ##  ##  ##  ##  ##  ##      ##        ##    ##  ##  ##  ##
    ##  ##  ##  ######  ####    ######    ##    #####   ##  ##
    ##  ##  ##  ##  ##  ##          ##    ##    ##  ##  ##  ##
    ##  ##  ##  ##  ##  ######  ######    ##    ##  ##  ######


    """
    )

    # Create a virtual outport
    outport = mido.open_output("MIDI Maestro", virtual=True)
    print("Opened a virtual MIDI port called 'MIDI Maestro'.")
    print("Set the input of your VST instrument to this port.\n")

    try:
        # Fetch the inport
        inport = get_inport()

        while True:
            # Fetch and play a MIDI file.
            play_midi_file(get_midi_file(), outport)

    except KeyboardInterrupt:
        # Close the ports
        outport.close()
        try:
            inport.close()
        except:
            pass
        print("\n\nClosed the virtual MIDI port.")
