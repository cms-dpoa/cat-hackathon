import awkward as ak
from coffea.nanoevents import NanoEventsFactory, PFNanoAODSchema

#fname = "https://raw.githubusercontent.com/cms-dpoa/cat-hackathon/main/data/doubleeg_nanoaod_eg.root"
fname = "data/doubleeg_nanoaod_eg.root"
events = NanoEventsFactory.from_root(
    fname,
    schemaclass=PFNanoAODSchema.v6,
    metadata={"dataset": "DoubleEg"},
).events()

# PF candidate collection for jets
#print(events.Jet.nConstituents)

# Number of PF candidates, print and save to a text file
n_pfcands=ak.num(events.PFCands, axis=1)

print(n_pfcands)
print(events.PFCands.fields)

import json

with open('PF_n.txt', 'w') as filehandle:
    json.dump(n_pfcands.tolist(), filehandle)

# Plot PF candidate pt and their number and save the images
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_yscale('log')
ax.hist(ak.flatten(events.PFCands.pt), bins=200)
ax.set_title('PF candidate p_t')

fig.savefig("PF_pt.png")

fig, ax = plt.subplots()
ax.hist(ak.num(events.PFCands, axis=1), bins=50)
ax.set_title('n PF candidates')

fig.savefig("PF_n.png")


