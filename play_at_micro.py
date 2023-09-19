import wave
import sys
import time

import pyaudio

class SoundPlayer:
    def __init__(self):
        self.CHUNK = 1024
        self.OUTPUT_DEVICE_INDEX = 6

    def select_audio_output(self):
        p = pyaudio.PyAudio()
        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
        
        self.OUTPUT_DEVICE_INDEX = int(input("Select Audio Output (id): "))
    
    def set_output_device(self, device_id): self.OUTPUT_DEVICE_INDEX = device_id
    def get_output_device(self):     return self.OUTPUT_DEVICE_INDEX

    def stream_filename(self, filename):
        with wave.open(sys.path[0]+"\\"+filename, 'rb') as wf:
            # Instantiate PyAudio and initialize PortAudio system resources (1)
            p = pyaudio.PyAudio()

            # Open stream (2)
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True, 
                            output_device_index=self.OUTPUT_DEVICE_INDEX)
            
            time.sleep(0.08);

            # Play samples from the wave file (3)
            while len(data := wf.readframes(self.CHUNK)):  # Requires Python 3.8+ for :=
                stream.write(data)

            # Close stream (4)
            stream.close()

            # Release PortAudio system resources (5)
            p.terminate()

class AppAudioStreamer:
    pass 