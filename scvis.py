# Instrument Visualizer Script for Synth-Corona
# Reads an SC File & draws waveforms for each Instrument in it.

from PIL import Image, ImageDraw
from SynthCorona import SynthCorona, Repeat, Val
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
    width = int(argv[2])
else:
    width = int(input("Enter the output image width: "))

if(len(argv)>3):
    height = int(argv[3])
else:
    height = int(input("Enter the output image height: "))

if(len(argv)>4):
    reps = int(argv[4])
else:
    reps = int(input("Enter number of wave repetitions: "))

if(len(argv)>5):
    kys = argv[5]
else:
    kys = input("Which Instruments? (comma separated; 'all' for all): ")

if(len(argv)>6):
    freq = float(argv[6])
else:
    freq = float(input("What frequency? (-1 for simple waveforms): "))

SAMPS = 5
BRD = 25
header = stng[0:inx+1]
name = stng[inx+1:len(stng)]
ext = name.rfind(".")
if(ext > 0):
    name = name[0:ext]

sc = SynthCorona()
sc.parse(stng)
count = 0

if(kys in ["ALL","all"]):
    kys = sc.insts.keys()
else:
    kys = kys.split(",")

ln = len(kys)
wd = (width-(2*BRD))*SAMPS
sc.rate = wd

for ky in kys:
    ky = ky.strip()
    print(str(count) + " of " + str(ln))
    inst = sc.insts[ky].clone()
    frames = []
    img = Image.new("1",(width,height))
    draw = ImageDraw.Draw(img)
    if(freq <= 0):
        inst.set_freq(1)
        len = int(inst.period*reps)/inst.rate
    else:
        inst.set_freq(freq)
        len = int(inst.length()*reps)
    chnk = int(len/wd)
    for i in range(wd):
        frames.append(inst.read(stereo=False))
        for i in range(chnk):
            inst.step(1,1)
    hscale = (height-(2*BRD))/9.0/2
    mid = height/2
    last = (BRD,mid)
    for i in range(wd):
        next = (i//SAMPS+BRD,mid-(frames[i]*hscale))
        draw.line([last,next],fill=1,width=1)
        last = next

    img.save(header + ky + ".jpg")
    count += 1
print("Done!")
