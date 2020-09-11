
import h5py


f = h5py.File('ukdalekD22.h5', 'r+')
f.keys()
f.values()
members = []
f.visit(members.append)
for i in range(len(members)):
    print(members[i])

