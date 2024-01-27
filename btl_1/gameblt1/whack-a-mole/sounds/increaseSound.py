from pydub import AudioSegment

def increase_volume(input_file, output_file, gain_in_db):
    # Load the audio file
    audio = AudioSegment.from_file(input_file)

    # Increase the volume (gain) by the specified amount in decibels
    louder_audio = audio + gain_in_db

    # Export the louder audio to a new file
    louder_audio.export(output_file, format="wav")

# Example usage:
input_file = "hurt.wav"
output_file = "hurt1.wav"
gain_in_db = -10  # Adjust this value to increase or decrease the volume

increase_volume(input_file, output_file, gain_in_db)
