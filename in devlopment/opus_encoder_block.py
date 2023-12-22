import numpy as np
from gnuradio import gr
from pyogg import OpusBufferedEncoder
import time

class blk(gr.sync_block):
    def __init__(self, sample_rate=48000, bitrate=64000, application="audio", bandwidth="fullband", desired_frame_duration=60):
        gr.sync_block.__init__(
            self,
            name='Opus Encoder',
            in_sig=[np.float32, np.float32],
            out_sig=[np.byte]
        )

        self.opus_encoder = OpusBufferedEncoder()
        self.opus_encoder.set_application(application)
        self.opus_encoder.set_sampling_frequency(sample_rate)
        self.opus_encoder.set_channels(2)
        self.opus_encoder.set_bitrates(bitrate)
        self.opus_encoder.set_bandwidth(bandwidth)
        self.opus_encoder.set_frame_size(desired_frame_duration)

    def floats_to_int16(self, float_values):
        scaled_values = (float_values * 32767).astype(np.int16)
        return scaled_values

    def work(self, input_items, output_items):
        pcm = (input_items[0] + input_items[1]) / 2
        pcm_int16 = self.floats_to_int16(pcm)

        # Convert PCM samples to bytes using a writable buffer
        #pcm_bytes = pcm_int16.tobytes()

        # Encode the PCM bytes
        #print("h")
        encoded_packets = self.opus_encoder.buffered_encode(memoryview(bytearray(pcm_int16)))

        # Copy the encoded data to the output array
        for encoded_packet, _, _ in encoded_packets:
            #output_items[0] = np.frombuffer(encoded_packet, dtype=np.uint8).tobytes()
            output_items[0] = encoded_packet.tobytes()
            #time.sleep(1)
            #print(encoded_packet)

        return len(output_items[0])
