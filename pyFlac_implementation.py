import sys
import queue
import numpy as np
import soundfile as sf
import pyflac


"""
    class FlacCodec- creates the encoder and decoder using pyFlac library
        Functions:
            constructor: takes in args input_file and output_name
                         initialises encoder/decoder using StreamEncoder pyFlac function
            encode/decode: runs the process function of pyFlac
            encoder_callback: adds encoded data to a queue for later processing
            decoder_callback: asserts no data loss
                              write audio data to .wav file using soundfile
    
    Issues with Code:
     * after encoding doesn't write encoded data into a .bin file  
                       
                     
"""



class FlacCodec:


    def __init__(self, input_file, output_name): # initialises encoder/decoder using StreamEncoder pyFlac function
        #initialise info for audio processing
        self.index=0
        self.all_bytes=0
        self.queue=queue.SimpleQueue()
        self.output_name=output_name

        #checks number of bits per sample of input_file
        input_info=sf.info(str(input_file))
        if input_info.subtype=="PCM_16":
            dtype="int16"
        elif input_info.subtype=="PCM_32":
            dtype="int32"

        #gets audio data and sample rate using soundfile
        self.data, self.sample_rate =sf.read(input_file, dtype=dtype, always_2d=True)

        #initialises encoder using enoder_callback function, samplerate, and blocksize
        #default compression level is 5
        self.encoder=pyflac.StreamEncoder(
            write_callback=self.encoder_callback,
            sample_rate=self.sample_rate,
            blocksize=0
        )

        ##initialises decoder using decoder_callback function
        self.decoder=pyflac.StreamDecoder(
            write_callback=self.decoder_callback
        )


    def encode(self): #encodes audio data
            #pyFlac process method ensures:
                #samples are continguous in memory
                #pases a pointer to the numpy array to FLAC encoder to process
            self.encoder.process(self.data)
            self.encoder.finish()

    def decode(self): #decodes audio data
        #checks if encoded queue is empty or not
        #processes audio data if not
        while not self.queue.empty():
            self.decoder.process(self.queue.get())
        self.decoder.finish()


    # function to add encoded bytes into a queue
    def encoder_callback(self,
                         buffer: bytes,
                         num_bytes: int,
                         num_samples: int,
                         current_frame:int):
        self.all_bytes += num_bytes
        self.queue.put(buffer)


    #function to write encoded audio_data into a .wav file
    def decoder_callback(self,
                         data:np.ndarray,
                         sample_rate: int,
                         num_channels: int,
                         num_samples:int):
        #checks that no data has been lost
        assert self.sample_rate==sample_rate
        assert np.array_equal(data, self.data[self.index:self.index+num_samples])

        #changes the bit being worked on
        self.index += num_samples

        #writes audio data into .wav file
        output_file = sf.SoundFile(self.output_name, mode="w",
                                   channels=num_channels, samplerate=self.sample_rate)
        output_file.write(self.data)





#main function
if __name__=='__main__':
    #checks if libraries are all there
    print("All libraries are there", file=sys.stderr)

    #initialises FLAC codec
    codec=FlacCodec("dataset/input.wav", "output.wav")

    #encodes and decodes
    codec.encode()
    codec.decode()

    #calculates compression rate
    compression_rate=codec.all_bytes/codec.data.nbytes*100

    #prints that Codec works and what the compression rate is
    print("Codec Works", file=sys.stderr)
    print(f"Compression rate={compression_rate:.2f}%")
