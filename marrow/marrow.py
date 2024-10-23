from obspy import read, read_inventory
from obspy.signal import freqattributes
import numpy as np
import matplotlib.pylab as plt
from RS_function import RS_function

# st = read("./raw/CHUS_titanSMA_2137_20240818_091000.seed")
st = read("./raw/PAUS_titanSMA_2138_20240520_114500.seed")
# st = read("./raw/CHUS_titanSMA_2137_20240708_095400.seed")

print(st)

for i in range(3):
    print(st[i].stats)

# add a vertification that all component data is there
# could loop through stats and validate each one is what we say it is
# print(st[0].data.size)
# print(st[0].data)


# correction factor
CF = 2
z_comp = st[0]
z_comp_acc = z_comp
print(z_comp_acc.data)


# Data correction
z_comp_acc.data = z_comp_acc.data * (1 / (CF / 0.00098066))
# z_comp_acc.data = z_comp_acc.data - z_comp_acc.data.mean()
# baseline correction
z_comp_acc.detrend("linear")
z_comp_acc.filter("bandpass", freqmin=1.0, freqmax=20.0)
# remove mean
z_comp_acc.detrend("constant")

############################################################################
Response_t = "SA"
T = np.concatenate(
    (
        np.arange(0.05, 0.1, 0.005),
        np.arange(0.1, 0.5, 0.01),
        np.arange(0.5, 1, 0.02),
        np.arange(1, 5, 0.1),
        np.arange(5, 15.5, 0.5),
    )
)
freq = 1 / T
# damping factor
xi = 0.05
# Its already rounded up but anyways
dt = round(z_comp_acc.stats.delta, 3)
delta_hz = 1 / dt

Sfin = np.zeros((3, len(T)))
Sfin[i] = RS_function(z_comp_acc.data, delta_hz, T, xi, Resp_type=Response_t)

t = np.linspace(0, len(z_comp_acc.data) * dt, len(z_comp_acc.data))  # Time vector
############################################################################


fig = plt.figure()
# not doing much really but will coome back to this later
ax = fig.add_subplot(3, 1, 1)
plt.plot(z_comp_acc.times("relative"), z_comp_acc.data, "b-")
plt.grid()
plt.legend(loc=1)
# TODO: add a timestamp that says 'time relative to xxx'
# TODO: Add a big version of each graph :)

plt.title("Dummy sample")

ax = fig.add_subplot(3, 1, 2)
plt.semilogy(T, Sfin[i], linewidth=2)
plt.ylabel('Acceleration response (cm/s/s)')
plt.xlabel('Period (s)')
plt.grid()
plt.tight_layout()

ax = fig.add_subplot(3, 1, 3)
plt.semilogy(freq, Sfin[i], linewidth=2)
plt.ylabel('Acceleration response (cm/s/s)')
plt.xlabel('Frequency (Hz)')
plt.grid()
plt.tight_layout()

plt.show()

#obspy graph
z_comp_acc.plot(type="relative", block=True)

# Response spectrum
# nfft = len(z_comp_acc.data)
nfft = 1024
freq = np.fft.rfftfreq(nfft, d=z_comp_acc.stats.delta)
spect = np.abs(np.fft.rfft(z_comp_acc.data, n=nfft))
# plt.plot(freq, spect)
# plt.show()

# z_alt = st.select(component="Z")
# z_alt.plot()
