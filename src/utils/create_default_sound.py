import wave
import math
import struct

def create_beep_sound(filename, duration=1.0, frequency=440.0, amplitude=0.5, sample_rate=44100):
    """Create a simple beep sound"""
    num_samples = int(duration * sample_rate)
    audio_data = []
    
    for i in range(num_samples):
        t = float(i) / sample_rate
        value = amplitude * math.sin(2.0 * math.pi * frequency * t)
        packed_value = struct.pack('h', int(value * 32767.0))
        audio_data.append(packed_value)

    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b''.join(audio_data))

if __name__ == "__main__":
    # Create a 1-second beep sound
    create_beep_sound("../../sounds/default_alarm.wav", duration=1.0, frequency=880.0) 