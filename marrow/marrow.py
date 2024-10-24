from obspy import read, read_inventory
from obspy.signal import freqattributes
from obspy.signal.detrend import polynomial
import numpy as np
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
from RS_function import RS_function

st = read("./raw/CHUS_titanSMA_2137_20240818_091000.seed")
# st = read("./raw/PAUS_titanSMA_2138_20240520_114500.seed")
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

otime = z_comp_acc.stats.starttime
z_comp_acc = z_comp_acc.slice(otime + 25, otime + 60)

# Data correction
z_comp_acc.data = z_comp_acc.data * (1 / (CF / 0.00098066))

# baseline correction
z_comp_acc.detrend("linear")
# polynomial(z_comp_acc.data, order=4, plot=False)
# z_comp_acc.detrend("spline", order=4, dspline=500, plot=False)

# remove mean
z_comp_acc.detrend("demean")

# filter
z_comp_acc.filter("bandpass", freqmin=1.0, freqmax=20.0)

############################################################################
Response_t = "SA"
response_end_t = 4
response_end_t = 4.05
T_for_freq = np.concatenate(
    (
        np.arange(0.05, 0.1, 0.005),
        np.arange(0.1, 0.5, 0.01),
        np.arange(0.5, 1, 0.02),
        np.arange(1, 5, 0.1),
        # np.arange(5, response_end_t, 0.5),
    )
)
# T = np.arange(0.001, response_end_t, 0.05)
T = np.linspace(0.011, response_end_t, 250)
freq = 1 / T_for_freq
# damping factor
xi = 0.05
# Its already rounded up but anyways
dt = round(z_comp_acc.stats.delta, 3)
# convert to hertz
delta_hz = 1 / dt

# create the array in which the data will live
acc_spectra = np.zeros((3, len(T)))
acc_spectra_freq = np.zeros((3, len(T_for_freq)))
acc_spectra[i] = RS_function(z_comp_acc.data, delta_hz, T, xi, Resp_type=Response_t)
acc_spectra_freq[i] = RS_function(
    z_comp_acc.data, delta_hz, T_for_freq, xi, Resp_type=Response_t
)

velocity_spectra = np.zeros((3, len(T)))
velocity_spectra[i] = RS_function(z_comp_acc.data, delta_hz, T, xi, Resp_type="SV")

displacement_spectra = np.zeros((3, len(T)))
displacement_spectra[i] = RS_function(z_comp_acc.data, delta_hz, T, xi, Resp_type="SD")

t = np.linspace(0, len(z_comp_acc.data) * dt, len(z_comp_acc.data))  # Time vector

print("\n\n\n")
print(f"T:{T}")
print(f"dt: {dt}")
print(f"freq:{freq}")
print(f"delta_hz:{delta_hz}")
print(f"acc_spectra:{acc_spectra}")
print(f":{(3, len(T))}")
# print(f":{}")
# print(f":{}")
# print(f":{}")
############################################################################

gs = gridspec.GridSpec(3, 2)
fig_sizes = (18, 10)

fig = plt.figure(figsize=fig_sizes)
ax = fig.add_subplot(gs[0, :])
plt.plot(z_comp_acc.times("relative"), z_comp_acc.data, "b-")
plt.grid()
plt.legend(loc=1)
plt.title("Z comp")
plt.xlabel(f"Time (s) relative to {z_comp_acc.stats.starttime}")
plt.ylabel(f"Acceleration (cm/s^2)")

# fig = plt.figure(figsize=fig_sizes)
ax = fig.add_subplot(gs[1, 0])
plt.plot(T, acc_spectra[i], linewidth=2)
plt.title("Acceleration Response (Period)")
plt.ylabel("Acceleration response (cm/s/s)")
plt.xlabel("Period (s)")
plt.grid()
plt.tight_layout()

# # fig = plt.figure(figsize=fig_sizes)
# # ax = fig.add_subplot(3, 1, 3)
# ax = fig.add_subplot(gs[1,1])
# plt.plot(freq, acc_spectra_freq[i], linewidth=2)
# plt.title("Acceleration Response (Frequency)")
# plt.ylabel("Acceleration response (cm/s/s)")
# plt.xlabel("Frequency (Hz)")
# plt.grid()
# plt.tight_layout()

# fig = plt.figure(figsize=fig_sizes)
# ax = fig.add_subplot(3, 1, 3)
ax = fig.add_subplot(gs[1, 1])
plt.loglog(T, acc_spectra[i], linewidth=2)
plt.title("Acceleration Response (Period) in logarithmic scale")
plt.ylabel("Acceleration response (cm/s/s)")
plt.xlabel("Period (s)")
plt.grid()
plt.tight_layout()

# fig = plt.figure(figsize=fig_sizes)
# ax = fig.add_subplot(3, 1, 3)
ax = fig.add_subplot(gs[2, 0])
# plt.plot(freq, acc_spectra_freq[i], linewidth=2)
plt.plot(T, velocity_spectra[i], linewidth=2)
plt.title("Velocity Response (Period)")
plt.ylabel("Velocity response (cm/s)")
plt.xlabel("Period (s)")
plt.grid()
plt.tight_layout()

# fig = plt.figure(figsize=fig_sizes)
# ax = fig.add_subplot(3, 1, 3)
ax = fig.add_subplot(gs[2, 1])
# plt.plot(freq, acc_spectra_freq[i], linewidth=2)
plt.plot(T, displacement_spectra[i], linewidth=2)
plt.title("Displacement Response (Period)")
plt.ylabel("Displacement response cm")
plt.xlabel("Period (s)")
plt.grid()
plt.tight_layout()

plt.show()

###########################################################################################
gs2 = gridspec.GridSpec(3, 2)
fig2 = plt.figure(figsize=fig_sizes)

ax = fig2.add_subplot(gs2[0, :])
plt.plot(z_comp_acc.times("relative"), z_comp_acc.data, "b-")
plt.grid()
plt.legend(loc=1)
plt.title("Z comp")
plt.xlabel(f"Time (s) relative to {z_comp_acc.stats.starttime}")
plt.ylabel(f"Acceleration (cm/s^2)")

z_comp_acc.integrate()
# z_comp_acc.integrate(method='spline', k=4)
ax = fig2.add_subplot(gs2[1, :])
plt.plot(z_comp_acc.times("relative"), z_comp_acc.data, "b-")
plt.grid()
plt.legend(loc=1)
plt.xlabel(f"Time (s) relative to {z_comp_acc.stats.starttime}")
plt.ylabel(f"Velocity (cm/s)")

z_comp_acc.integrate()
# z_comp_acc.integrate(method='spline', k=4)
ax = fig2.add_subplot(gs2[2, :])
plt.plot(z_comp_acc.times("relative"), z_comp_acc.data, "b-")
plt.grid()
plt.legend(loc=1)
plt.xlabel(f"Time (s) relative to {z_comp_acc.stats.starttime}")
plt.ylabel(f"Displacement (cm)")
plt.show()

# z_comp_acc.plot(type="relative")

# obspy graph
# z_comp_acc.plot(type="relative")

# z_alt = st.select(component="Z")
# z_alt.plot()
