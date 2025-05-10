from pygame import mixer
import time
import os

class AudioManager:
    def __init__(self):
        mixer.init()

    def play_alarm(self, sound_path, gradual=False):
        """Play an alarm sound"""
        try:
            # Check if file exists
            if not os.path.exists(sound_path):
                print(f"Sound file not found: {sound_path}")
                sound_path = "default_alarm.wav"  # Fallback to default

            mixer.music.load(sound_path)
            mixer.music.set_volume(0.1 if gradual else 1.0)
            mixer.music.play(-1)
            if gradual:
                for i in range(10, 101, 10):
                    mixer.music.set_volume(i / 100)
                    time.sleep(2)
        except Exception as e:
            print(f"Error playing sound: {e}")
            # Try playing default alarm if custom sound fails
            try:
                mixer.music.load("default_alarm.wav")
                mixer.music.play(-1)
            except:
                print("Could not play default alarm sound")

    def stop_alarm(self):
        """Stop the current alarm sound"""
        mixer.music.stop()

    def quit(self):
        """Clean up audio resources"""
        mixer.quit()