from evtx.Evtx import Evtx

# Print the Evtx class to check its type
print("Evtx class:", Evtx)
print("Type of Evtx:", type(Evtx))

# Optionally, instantiate Evtx to see if it works as expected
try:
    evtx_instance = Evtx("example.evtx")
    print("Successfully created an Evtx instance:", evtx_instance)
except Exception as e:
    print("Error creating Evtx instance:", e)
