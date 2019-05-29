from SynthCorona import SynthCorona
from sys import argv

if(len(argv)>1):
    stng = argv[1]
else:
    print("\n\n\n\n\n\n\n\n\n")
    print("               === SYNTH-CORONA ===               ")
    print("                musical typewriter                ")
    print()
    print("                  by: Nash High                   ")
    print("                  version: 0.0.5                  ")
    print("\n\n\n\n\n\n\n\n\n")
    stng = input("Enter the path to the song file, or drag it in: ")
inx = stng.rfind("\\")
if(inx == -1):
    inx = stng.rfind("/")

header = stng[0:inx+1]
name = stng[inx+1:len(stng)]
ext = name.rfind(".")
if(ext > 0):
    name = name[0:ext]

tone = SynthCorona()
tone.parse(stng)
tone.render(header + name + ".wav")
