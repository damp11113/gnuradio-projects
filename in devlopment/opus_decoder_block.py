import numpy as np
from gnuradio import gr
from pyogg import OpusDecoder

class blk(gr.sync_block):
    def __init__(self, sample_rate=48000):
        gr.sync_block.__init__(
            self,
            name='Opus Decoder',
            out_sig=[np.complex64],
            in_sig=[np.byte]
        )

        self.opus_decoder = OpusDecoder()
        self.opus_decoder.set_channels(2)
        self.opus_decoder.set_sampling_frequency(sample_rate)

        self.max_output_items = 1024  # Adjust this value according to your needs

    def int16_to_float(self, input_data):
        # Convert int16 to float
        return np.array([float(x) / 32768.0 for x in input_data], dtype=np.float32)

    def work(self, input_items, output_items):
        try:
            opusencoded = memoryview(input_items[0])

            decoded_pcm = self.opus_decoder.decode(opusencoded)

            num_output_items = 0  # Initialize num_output_items
            if len(decoded_pcm) > 0:
                pcm_to_write = np.frombuffer(decoded_pcm, dtype=np.int16)
                output_items[0] = pcm_to_write
            else:
                print("Decoded PCM is empty")

        except Exception as e:
            print("Error:", str(e))
            # Log the error for debugging purposes
            # You can add more specific handling or raise the exception for better debugging

        return len(output_items)  # Return the number of items produced
