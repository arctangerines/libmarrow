from obspy import read, read_inventory
from obspy.signal import freqattributes
import numpy as np
import matplotlib.pylab as plt
st = read("./raw/CHUS_titanSMA_2137_20240818_091000.seed")

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
z_comp_acc.data = z_comp_acc.data * (1 / (CF / 0.00098066) )
z_comp_acc.data = z_comp_acc.data - z_comp_acc.data.mean()
z_comp_acc.detrend("linear")
z_comp_acc.plot(type="relative",outfile="chus_2137.png")
z_comp_acc.plot(type="relative")
z_comp_acc.filter('bandpass', freqmin=1.0, freqmax=20.0)
z_comp_acc.plot(type="relative")

# nfft = len(z_comp_acc.data)
nfft = 1024
freq = np.fft.rfftfreq(nfft, d=z_comp_acc.stats.delta)
spect = np.abs(np.fft.rfft(z_comp_acc.data, n=nfft))
plt.plot(freq, spect)
plt.show()

# z_alt = st.select(component="Z")
# z_alt.plot()
