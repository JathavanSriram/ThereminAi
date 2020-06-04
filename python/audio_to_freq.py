import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.io.wavfile import read,write
import socket
import threading
import sys
import queue

#Variables for holding information about connections
connections = []
total_connections = 0

#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
    
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Client " + str(self.address) + " has disconnected")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                for client in connections:
                    if client.id != self.id:
                        data2 = q.get_nowait()
                        data3 = str(data2.decode("utf-8"))
                        print(data3)
                        client.socket.sendall(data3)


#Wait for new connections
def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1


def update_plot(frame, *fargs):

    # x = np.linspace(0, 4, 1000)
    # ys = np.sin(2 * np.pi * (x - 0.01 * frame))
   
    fargs[0].clear()
    shift = len(fargs[1])
    fargs[0].plot(np.roll(fargs[1],-shift, axis=0))

    # plt.xlabel('Date')
    # plt.ylabel('Price')
    # plt.title('Live graph with matplotlib')	

def recording_callback(indata, frames, time, status):
    clipped_data = indata[500:1500]
    print(clipped_data.shape)
    plot_data(clipped_data,0,900)
    # dominant_frequency(clipped_data)
    # 1/f * sampling rate = sample length of one wave x
    # 1/f * 44100 = x
    # 1/f = x / 44100
    # 1 = x / 44100 * f
    # 1 / (x / 44100) = f
    # 44100 / x = f

    return 0


def record_audio():
    duration = 0.4 # seconds
    fs = 44100
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1,dtype='int16',blocking=True)
    clip_data = myrecording[5000:88000]
    # plot_data(clip_data,0,1000)
    #### Jesus Christ ... it wrote a 2D Array ... vs. 1D Array for 1 channel what it should have been
    ### Using np.ravel to convert to 1-D Array
    current_freq = dominant_frequency(np.ravel(clip_data))
    # print("The fucking data type of the recorded stream array is",clip_data.dtype)
    # write("/home/drmanhattan/04_projects/ThereminAi/sound/testfile.wav",44100,clip_data)

    return current_freq


def record_audio_stream():
    print("Calling Record Audio - Stream Recording")
    while True:
        with sd.InputStream(device=0, channels=1, callback=recording_callback,blocksize=2000,samplerate=44100,dtype='int16'):
            print("Still Streaming Input")


def open_wav_file(filepath):
    input_data = read(filepath)
    audiodata = input_data[1]
    print("The fucking data type of the opened file is",audiodata.dtype)
    return audiodata



def dominant_frequency(inputdata):
    # print("Shape of Input Array is:", inputdata)
    w = np.fft.fft(inputdata)
    # print("Lenght of FFT Output", w.shape)
    # print(w)
    freqs = np.fft.fftfreq(len(w))
    # print("Lenght of FFT FREQ Output", freqs.shape)
    
    # print(freqs.min(), freqs.max())
    # (-0.5, 0.499975)

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    # print("This is idx,",idx)
    freq = freqs[idx]
    freq_in_hertz = np.around(abs(freq * 44100))
    print("Current Frequency is: --->, ", freq_in_hertz)
    # 439.8975

    return freq_in_hertz

def plot_data(data,samplestart,sampleend):

    plt.plot(data[samplestart:sampleend])
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    # set the title  
    plt.title("Sample Wav")
    # display the plot
    plt.show(block=True)
    return 0 



def sine_wave_function(frequency,samplerate):
    sine_wave = [np.sin(2 * np.pi * frequency * x/samplerate) for x in range(samplerate)]
    return np.asarray(sine_wave)

def main():
    print("Running the main function")

    # sw = sine_wave_function(600,600)
    #print(sw.shape, "\n", sw)
    #audiodata = open_wav_file("/home/drmanhattan/04_projects/ThereminAi/sound/sin_400Hz_-3dBFS_5s.wav")
    #plot_data(audiodata,0,1024)
    #audiodata2= open_wav_file("/home/drmanhattan/04_projects/ThereminAi/sound/sin_440Hz_0dBFS_5s.wav")
    #plot_data(audiodata2,0,1024)

    # Create a client server connection
        #Get host and port
    


    while True:
        freq = record_audio()
    # audiodata4= open_wav_file("/home/drmanhattan/04_projects/ThereminAi/sound/testfile.wav")
    # plot_data(audiodata4,0,1000)
    #print(max(audiodata3[0:200]))
    # dominant_frequency(audiodata4)


    # fig = plt.figure()
    #creating a subplot 
    # subplot1 = fig.add_subplot(1,1,1)

    # ani = animation.FuncAnimation(fig, func=update_plot,fargs=[subplot1,audiodata4], interval=100,blit=True) 
    # plt.show()
    

if __name__ == "__main__":
    print("Program start")
    main()