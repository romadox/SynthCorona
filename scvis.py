# Instrument Visualizer Script for Synth-Corona
# Reads an SC File & draws waveforms for each Instrument in it.

from PIL import Image, ImageDraw
from SynthCorona import SynthCorona
from sys import argv

if(len(argv)>1):
    stng = argv[1]
else:
    print("\n\n\n\n\n\n\n\n\n")
    print("               === SYNTH-CORONA ===               ")
    print("               Instrument Visualizer              ")
    print()
    print("                  by: Nash High                   ")
    print("                  version: 1.0.0                  ")
    print("\n\n\n\n\n\n\n\n\n")
    stng = input("Enter the path to the song file, or drag it in: ")
inx = stng.rfind("\\")
if(inx == -1):
    inx = stng.rfind("/")

if(len(argv)>2):
    width = int(argv[1])
else:
    width = int(input("Enter the output image width: "))

if(len(argv)>3):
    height = int(argv[2])
else:
    height = int(input("Enter the output image height: "))

SAMPS = 5
BRD = 10
header = stng[0:inx+1]
name = stng[inx+1:len(stng)]
ext = name.rfind(".")
if(ext > 0):
    name = name[0:ext]

sc = SynthCorona()
sc.parse(stng)
count = 0
ln = len(sc.insts.keys())

for ky in sc.insts.keys():
    print(str(count) + " of " + str(ln))
    inst = sc.insts[ky].mdl
    img = Image.new("1",(width,height))
    draw = ImageDraw.Draw(img)
    step = inst.length()/((width-(2*BRD))*SAMPS)
    hscale = -(height-(2*BRD))/9.0/2
    mid = height/2
    last = (BRD,mid)
    for i in range((width-BRD-BRD)*SAMPS):
        next = (i//SAMPS+BRD,mid-(inst.read(stereo=False)*hscale))
        draw.line([last,next],fill=1,width=2)
        inst.step(step,1)
        last = next
    next = (i//SAMPS+BRD,mid-(inst.read(stereo=False)*hscale))
    draw.line([last,next],fill=1,width=2)

    img.save(header + ky + ".jpg")
    count += 1
print("Done!")
