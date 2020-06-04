#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys
import math

from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=1000,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=1, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1

q = queue.Queue()


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    # Fancy indexing with mapping creates a (necessary!) copy:
    conversion = indata[::args.downsample, mapping]
    # print("This is the conversion",conversion)
    q.put(conversion)


def findfreq(inputdata):

    inputdata = np.ravel(inputdata)
    
    sine_wave = 10*[np.sin(2 * np.pi * 440 * x/48000) for x in range(48000)]
    sine_wave2 = 9*[np.sin(2 * np.pi * 540 * x/48000) for x in range(48000)]
    sine_wave = sine_wave + sine_wave2
    # print("Size of Input data is", len(inputdata))
    #data_fft = np.fft.fft(inputdata)
    #frequencies = np.abs(data_fft)
    #print("The frequency is {} Hz".format(np.argmax(frequencies)))
    ## print(len(sine_wave))
    
    # samplerate = sd.query_devices(args.device, 'input')['default_samplerate']
    # print("This is the samplerate, ", samplerate)  
    w = np.fft.fft(inputdata)
    #w = np.fft.fft(sine_wave)
    print("Lenght of FFT Output", w.shape)
    # print(w)
    freqs = np.fft.fftfreq(len(w))
    print("Lenght of FFT FREQ Output", freqs.shape)
    
    # print(freqs.min(), freqs.max())
    # (-0.5, 0.499975)

    # Find the peak in the coefficients
    idx = np.argmax(np.abs(w))
    # print("This is idx,",idx)
    freq = freqs[idx]
    freq_in_hertz = np.around(abs(freq * 44100))
    print("Frequency should be, ", freq_in_hertz)
    # 439.8975

    return 0


def update_plot(frame):
    """This is called by matplotlib for each plot update.

    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.

    """
    global plotdata
    while True:
        try:
            data = q.get_nowait()
            ftransformed = findfreq(data)
            
        except queue.Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    
    
    return lines


if __name__ == "__main__":

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            args.samplerate = device_info['default_samplerate']
            print("The sample rate is,:", args.samplerate)

        length = int(args.window * args.samplerate / (1000 * args.downsample))
        plotdata = np.zeros((length, len(args.channels)))

        fig, ax = plt.subplots()
        lines = ax.plot(plotdata)
        if len(args.channels) > 1:
            ax.legend(['channel {}'.format(c) for c in args.channels],
                    loc='lower left', ncol=len(args.channels))
        ax.axis((0, len(plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False,
                    right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)

        print("DEVICE ID IS:", args.device)

        stream = sd.InputStream(
            device=args.device, channels=1,
            samplerate=44100, callback=audio_callback, blocksize=8000, dtype='int16')

        ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)

        with stream:
            plt.show()
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))