from obspy import read
st = read("./raw/CHUS_titanSMA_2137_20240818_091000.seed")

print(st)

for i in range(3):
    print(st[i].stats)

# add a vertification that all component data is there
# could loop through stats and validate each one is what we say it is
print(st[0].data.size)
print(st[0].data)

# correction factor
CF = 2

# z_alt = st.select(component="Z")

z_comp = st[0]
z_comp_acc = z_comp
z_comp_acc.data = z_comp_acc.data * (1 / (CF / 0.00098066) )
print(z_comp_acc.data)
print(z_comp.times("relative"))
z_comp_acc.plot(type="relative")


# two ways of achieving the same thing
z_alt = st.select(component="Z")
z_alt_acc = z_comp
z_alt_acc.data = z_comp_acc.data * (1 / (CF / 0.00098066) )
print(z_alt_acc.data)
z_alt_acc.plot(type="relative")
