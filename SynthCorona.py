""" SYNTH-CORONA: MUSICAL TYPEWRITER

    This is a little code language for creating chiptunes. It features a highly
    modular design which can be applied to instruments, pitches, sequences,
    and patterns.

    Version 1.1.1

"""

#TODO: SeqLine does not handle ADJUST steps -- should it?
#TODO: Should SeqLine step pitch & pan by delta*frameslice?
#      What happens if we apply Speed(Seq,2) etc?
import wave
import sys, random, time


# Major headers
HEADERS = {"CFG", "INS", "MDL", "SEQ", "PAT", "BLK", "SNG", "IMP"}
# Reserved symbols (which cannot be used in names)
# Note: Names can contain numbers, but they cannot begin with a number.
RESERVED = "+-*/rixlvcs{}[]()<>.,|"
# List of operators
OPERATORS = "+-=*/rixlvs"
# Rendering chunk size -- atm, only determines how often progress label
# is updated (in samples).
CHUNK = 1028*1
# Maximum signal value, as written in a SC file (absolute value).
MAX_VAL = 9

# Indicates that we are parsing an Instrument
INST = 0
# Indicates that we are parsing a pitch
TONE = 1
# Indicates that we are parsing a Sequence
SEQN = 2
# Indicates that we are parsing a generic module
MDLE = 3

# Time it takes a non-sustain Instrument to release to 0, in ms
INS_REL_TIME = 6
# Instrument signal codes -- These are sent in as const values in step()
# to send the Instrument special instructions.
# Tells Inst to use the delta value as const.
DELTA = -1
# Tells the Inst to stop, triggering any release operations.
STOP = -2
# Tells the Inst that this is a step adjustment. ADJUST is done regularly when
# a module ends and is reset, in order to sync it with whatever extra amount
# it was stepped previously. Accordingly, Insts should step the delta value
# exactly, without applying rate or frequency adjustments.
ADJUST = -3
# Tells modules inside an instrument to release--specifically Envelope.
# Inst does not pass on STOP commands, because nested Insts might not need to
# stop (i.e., a waveform should not stop). We send release instead, to let
# modules know a release has occurred, but that they should not stop.
RELEASE = -4

class SCParseError(Exception):
    """ Exception for syntax errors discovered while parsing a SC file. """

    def __init__(self, msg="", line=0):
        """ Initializer

            Keyword Arguments:
            msg -- Message describing the error.
            line -- The line number of where the error was tripped.
        """
        self.message = msg + " Line: " + str(line)

    def __str__(self):
        """ Returns the error message (with line number). """
        return self.message

class SCModule:
    """ Base class for Modules in SynthCorona.

        Modules are used to create Instruments, Sequences, and Song Patterns,
        as well as controlling pitch.

        Each module generally performs a single simple function, but they can
        be combined and nested to create complex patterns and operations.
    """

    def step(self, delta, const=-1):
        """ Steps the module forward in time.

            Delta is the local time amount by which to step, which is used
            by most modules. However, certain modules are designed to operate
            independently of things like pitch require a constant time amount,
            which is provided by const.

            Additionally, some negative const values are used to send modules
            the following commands:
                DELTA (const = -1): Use the delta value for const value.
                STOP (const = -2): Tells the module to stop, or Insts to release.
                ADJUST (const = -3): Indicates a special time-adjustment. This
                        tells modules to advance by delta exactly, without applying
                        any rate modifications. When const=ADJUST, we generally
                        assume that delta=get_extra() from some previous module,
                        or from this module, before it was reset.

            Arguments:
            delta -- Local time slice.
            const -- Constant time value, or command signal.
        """
        raise NotImplementedException()

    def step_tails(self, delta, const=-1):
        """ Steps any tails in the module forward in time.

            Tails are sustaining sounds in Instruments & Sequences that have
            been released but are not yet silent.

            Arguments:
            delta -- Local time slice.
            const -- Constant time value.
        """
        raise NotImplementedException()

    def read(self, tails=False,stereo=True,signal=True):
        """ Reads the module at its current position.

            (Occasionally, other upkeep steps are occur here as well. See
            individual modules for details.)

            The tails argument determines whether we will read sustaining notes
            or active instruments. One important thing to note is that certain
            modules like Val do not behave differently based on tails. In
            certain cases this means Val ends up getting read twice and is
            doubled. To prevent this, modules that do not apply to tails have
            a property "no_tails". Use getattr() to check for this field, and
            do not perform a second read() on it if you find it. (An example of
            this process can be found in Pattern.)

            The signal argument is not currently used. It was added for a change
            that did not end up being beneficial, but I have left it in in case
            it becomes useful. As a note, signals are represented within the
            range [-9,9], which corresponds to how they are depicted in SC code.

            Arguments:
            tails -- Whether we are reading tails or active sounds.
            stereo -- Whether we are reading in stereo.
            signal -- Whether we are reading a signal value, or a simple number.
        """
        raise NotImplementedException()

    def reset(self):
        """ Performs a small reset on a module.

            This is interpreted as a simple refreshing of the cycle throughout
            the song. Some modules do not entirely clear all of their parameters
            during reset(), but merely prepare themselves to begin again.

            When a module needs to be full re-initialized, clear() is the
            appropriate method to use.

            When resetting a finished module, it is often necessary to account
            for the small amount of time that has passed the completion mark
            (this avoids subtle distortions due to accumulating lost time).
            The standard process for this is as follows:

                extra = mdl.get_extra() # Store the amount of extra time.
                mdl.reset()             # Reset the module.
                mdl.step(extra,ADJUST)  # Adjust-step the module by extra

            If you are moving to a new module (i.e., in Pattern), you will
            do mdlB.step(extra,ADJUST), to pass the extra time on to the next
            module.
        """
        raise NotImplementedException()

    def clear(self):
        """ Performs a full clear on the module.

            This resets the module to its initial state. This function is a
            deeper refresh than reset(), which is intended for basic cycling
            of completed modules.
        """
        raise NotImplementedException()

    def done(self):
        """ Checks if the module is finished.
        """
        raise NotImplementedException()

    def get_extra(self):
        """ If the module is done, reports how much time we have advanced after
            finishing.

            In another sense -- this is how far the cursor has passed the end
            of this module. Whenever a module finishes, generally there is some
            extra time, which we will have to account for when resetting or
            moving to a new module.

            (See reset() for an outline of how to process this extra time.)
        """
        raise NotImplementedException()

    def length(self):
        """ Reports the module length.

            Note: In certain situations, an accurate length cannot be known.
            (For example, a Set with modules of different lengths.)
        """
        raise NotImplementedException()

    def set_freq(self,freq):
        """ For Instruments, sets the current frequency.

            Since Instruments are often nested within other modules, this
            must be a module function, so they can pass the frequency along
            to any Insts they may contain.

            Arguments:
            freq -- The frequency (in Hz)
        """
        raise NotImplementedException()

    def clone(self):
        """ Creates a deep copy of the module and returns it.
        """
        raise NotImplementedException()

class SynthCorona:
    """ Core SynthCorona class.

        Handles parsing an SC file into a modules and song data, as well as
        rendering that data into a Wave audio file.
    """

    def __init__(self):
        """ Empty initializer.

            Once initialized, call parse() to load song data and populate.
        """

        self.path = ""
        self.cfg = dict()
        self.insts = dict()
        self.modules = dict()
        self.seqs = dict()
        self.song = None
        self.tones = self.buildTones()
        self.freqs = self.buildFreqs()

        self.tempo = 120
        self.stereo = True
        self.beat = 4
        self.rate = 44100
        self.depth = 16
        self.normalize = True
        self.freq = 440
        self.framesperstep = (60*self.rate)/(self.tempo*self.beat)
        self.frameslice = 1/self.framesperstep
        self.rel_time = INS_REL_TIME*self.rate/1000

        self.curParseModule = "None"

    def buildTones(self):
        """ Builds the tones dictionary, which maps note/oct codes to their
            value in cents. This corresponds directly to how notes are
            depicted in SC -- i.e. "C4", "a2", "D#6", "F 3", etc.

            Generates 10 octaves (0-9).
        """

        slts = ["C", "d", "D", "e", "E", "F", "g", "G", "a", "A", "b", "B"]
        dlts = ["C ", "C#", "Db", "D ", "D#", "Eb", "E ", "F ", "F#", "Gb",
                "G ", "G#", "Ab", "A ", "A#", "Bb", "B ", ]
        dvals = [0, 1, 1, 2, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 10, 11, 11]
        ky = dict()

        for oct in range(10):
            for step in range(len(slts)):
                nm = slts[step]+str(oct)
                ky[nm] = (12*oct+step)*100
            for inx in range(len(dlts)):
                nm = dlts[inx]+str(oct)
                ky[nm] = (12*oct+dvals[inx])*100
        return ky

    def buildFreqs(self):
        """ Builds a list of pre-baked frequencies for each cent in the 10 octaves
            of the tones array. When pitches are read in SC, we will access the
            corresponding index of this array, rather than calculating on the fly.
        """

        freqs = []
        for i in range(12000):
            freqs.append(calc_freq(i-self.tones["A4"]))
        return freqs

    def parse(self, filename):
        """ Parses the SC file at filename and loads its information into this
            instance of SynthCorona.

            Arguments:
            filename -- The path of the file to parse.

            Throws SCParseError if any SC syntax errors are found while parsing.
        """

        # We pull the directory from the SC path, to use for importing files
        # from the same folder, without needing an absolute path.
        fldr = filename.rfind("\\")
        if(fldr < filename.rfind("/")):
            fldr = filename.rfind("/")
        if(fldr < 0):
            fldr = 0
        self.path = filename[0:fldr+1]

        # The SC file text, split into lines.
        text = open(filename).read()
        text = text.splitlines()

        # Parser states, indicating what type of chunk we are parsing.
        CFG = 0
        INS = 1
        MDL = 2
        SEQ = 3
        BLK = 4
        SNG = 5

        # Current parser block. This is changed by block headers.
        state = CFG

        # These variables affect Sequences. We'll reuse them for each Seq we
        # parse, but they need to be preserved across multiple lines while each
        # Sequence is being parsed.

        # The name that identifies a Sequence in SC code & in seqs Dict
        seqName = ""
        # Panning module to be applied to a whole Sequence.
        seqPan = None
        # The individual lines of a Sequence.
        seqLines = []
        # Holds each Sequence-level module in the song. We will
        # add new modules to this for each line under the SNG header.
        songSteps = []

        # Main parsing loop.
        for i in range(len(text)):
            line = text[i]

            # Identify and omit commented lines
            cmt = line.find("//")
            if(cmt >= 0):
                line = line[0:cmt]

            if(line != "" and not(line.isspace())):
                # Import Header -- loads imported file into this SynthCorona
                if(line.startswith(("IMP", "imp"))):
                    line = line[4:len(line)].strip()
                    if(line.find("\\")<0 and line.find("/")<0):
                        line = self.path + line
                        print(line)
                    tmp = SynthCorona()
                    try:
                        tmp.parse(line)
                    except SCParseError:
                        print("Error importing file: " + line)
                        raise

                    for i in tmp.insts.values():
                        i.parent = self
                    for s in tmp.seqs.values():
                        s.parent = self
                    self.modules.update(tmp.modules)
                    self.insts.update(tmp.insts)
                    self.seqs.update(tmp.seqs)
                # Configuration Header
                elif(line.startswith(("CFG", "cfg"))):
                    state = CFG
                # Instrument Header
                elif(line.startswith(("INS", "ins"))):
                    state = INS
                # Module Header
                elif(line.startswith(("MDL", "mdl"))):
                    state = MDL
                # Sequence Header. Clear Seq variables for new Sequence.
                elif(line.startswith(("SEQ", "seq"))):
                    seqPan = Val(0)
                    seqLines = []
                    state = SEQ
                    seqName = line[3:len(line)].strip()
                    # Parse Sequence meta-data
                    if("<" in seqName):
                        seqName = seqName.split("<")
                        if(seqName[1].find(">")<0):
                            raise SCParseError("Missing '>' in meta tag.",i)
                        seqName, meta = seqName[0].strip(), seqName[1].split(">")[0].split(",")
                        for mt in meta:
                            mt = mt.strip()
                            # Sets pan / pan module for the whole Sequence.
                            # (Modules must be loaded: they can't be described in meta)
                            if(mt.startswith(("pan", "PAN"))):
                                mt = mt.split("=")[1].lstrip()
                                if(mt in self.modules):
                                    seqPan = self.modules[mt].clone()
                                elif(mt != "" and (mt[0].isnumeric() or mt[0]=="." or mt[0]=="-")):
                                    invert = False
                                    if(mt.startswith("-")):
                                        invert = True
                                        mt = mt[1:len(mt)]
                                    num = ""
                                    while(len(mt)>0 and (mt[0].isnumeric() or mt[0] == ".")):
                                        num = num + mt[0]
                                        mt = mt[1:len(mt)]
                                    num = float(num)
                                    seqPan = Val(num)
                                    if(invert):
                                        seqPan = Invert(seqPan)
                    self.curParseModule = "SEQ: " + seqName
                # Block Header (Blocks are Sequence Modules)
                # We also accept "PAT" here, cause I always forget & call it that.
                # Officially, it is "Block", since "Pattern" is a module already.
                elif(line.startswith(("PAT", "pat", "BLK", "blk"))):
                    state = BLK
                # Song Header
                elif(line.startswith(("SNG", "sng"))):
                    state = SNG
                    self.curParseModule = "SONG"
                    line = line[3:len(line)].lstrip()
                    if(line.startswith(":")):
                        line = line[1:len(line)].lstrip()
                    if(len(line)>0 and not line.isspace()):
                        self.parseSongLine(line, songSteps)
                # If line doesn't start with Header string, parse based on state
                else:
                    # Configuration Chunk
                    if(state == CFG):
                        # Sets the master tempo.
                        if(line.startswith(("TEMPO","TMP","tempo","tmp"))):
                            line = line.split(":")[1].strip()
                            self.tempo=int(line)
                        # Sets the beat length (in song steps)
                        elif(line.startswith(("BEAT", "beat"))):
                            line = line.split(":")[1].strip()
                            self.beat=int(line)
                        # Sets the audio sample rate
                        elif(line.startswith(("RATE", "rate"))):
                            line = line.split(":")[1].strip()
                            self.rate=int(line)
                        # Sets the audio bit depth
                        elif(line.startswith(("DEPTH", "depth"))):
                            line = line.split(":")[1].strip()
                            self.depth=int(line)
                        # Sets the song name
                        elif(line.startswith(("NAME","TITLE","name","title"))):
                            line = line.split(":")[1].strip()
                            self.name=line
                        # Sets the song to Stereo Mode
                        elif(line.startswith(("STEREO","stereo"))):
                            self.stereo = True
                        # Sets the song to Mono mode
                        elif(line.startswith(("MONO","mono"))):
                            self.stereo = False
                        # Sets whether to normalize the audio (T/F)
                        elif(line.startswith(("NORMALIZE","normalize","NORM","norm"))):
                            line = line.split(":")[1].strip()
                            self.normalize=not line.startswith(("F","f","0"))

                        # Update some core values based on rate/tempo/beat
                        self.framesperstep = (60*self.rate)/(self.tempo*self.beat)
                        self.frameslice = 1/self.framesperstep
                        self.rel_time = INS_REL_TIME*self.rate/1000
                    # Song chunk
                    elif(state == SNG):
                        if(len(line)>0 and not line.isspace()):
                            self.parseSongLine(line, songSteps)
                    # Instrument / Module chunk
                    elif(state == INS or state == MDL):
                        # Separate the module name / description
                        name = line.split(":")
                        name, desc = name[0].strip(), name[1].strip()
                        # Wave period of instruments, in module steps
                        period = -1
                        # Whether the instrument loops
                        loop = True
                        # Whether the instrument sustains
                        sus = False
                        # Panning module of the instrument
                        pan = Val(0)
                        # Parse meta data
                        if("<" in name):
                            name = name.split("<")
                            if(name[1].find(">")<0):
                                raise SCParseError("Missing '>' in meta tag.",i)
                            name, meta = name[0].strip(), name[1].split(">")[0].split(",")
                            for mt in meta:
                                mt = mt.strip()
                                # Parse wave period
                                if(mt.startswith(("period", "PERIOD", "prd", "PRD"))):
                                    mt = mt.split("=")[1].lstrip()
                                    period = int(mt)
                                # Parse looping property (T/F)
                                elif(mt.startswith(("loop", "LOOP", "l", "L"))):
                                    mt = mt.split("=")[1].lstrip()
                                    loop = mt.startswith(("T","t","1"))
                                # Parse sustain property (T/F)
                                elif(mt.startswith(("sus", "SUS", "SUSTAIN", "sustain", "s", "S"))):
                                    mt = mt.split("=")[1].lstrip()
                                    sus = mt.startswith(("T","t","1"))
                                # Parse the pan value / load a pan module
                                elif(mt.startswith(("pan", "PAN"))):
                                    mt = mt.split("=")[1].lstrip()
                                    if(mt in self.modules):
                                        pan = self.modules[mt].clone()
                                    elif(mt != "" and (mt[0].isnumeric() or mt[0]=="." or mt[0]=="-")):
                                        invert = False
                                        if(mt.startswith("-")):
                                            invert = True
                                            mt = mt[1:len(mt)]
                                        num = ""
                                        while(len(mt)>0 and (mt[0].isnumeric() or mt[0] == ".")):
                                            num = num + mt[0]
                                            mt = mt[1:len(mt)]
                                        num = float(num)
                                        pan = Val(num)
                                        if(invert):
                                            pan = Invert(pan)
                                # Loads meta properties from another instrument
                                elif(mt.startswith(("BASE","base"))):
                                    mt = mt.split("=")[1].lstrip()
                                    ins = self.insts[mt]
                                    if(ins != None):
                                        period = ins.period
                                        loop = ins.loop
                                        sus = ins.sus
                                        pan = ins.pan.clone()
                        # Parses the description, either as Inst or Module
                        if(state == INS):
                            # Identifies module, for error reporting
                            self.curParseModule = "INS: " + name
                            self.insts[name] = Inst(self, self.parseModule(desc, INST, i), period, loop, sus,pan)
                        else:
                            # Identifies module, for error reporting
                            self.curParseModule = "MDL: " + name
                            self.modules[name] = self.parseModule(desc, MDLE, i)
                    # Block chunk
                    elif(state == BLK):
                        # Separate block name / description
                        name = line.split(":")
                        name, desc = name[0].strip(), name[1].strip()
                        # Pan module
                        pan = Val(0)
                        # Parse meta data for the block
                        if("<" in name):
                            name = name.split("<")
                            if(name[1].find(">")<0):
                                raise SCParseError("Missing '>' in meta tag.",i)
                            name, meta = name[0].strip(), name[1].split(">")[0].split(",")
                            for mt in meta:
                                mt = mt.strip()
                                # Parse pan value / load pan module
                                if(mt.startswith(("pan", "PAN"))):
                                    mt = mt.split("=")[1].lstrip()
                                    if(mt in self.modules):
                                        pan = self.modules[mt].clone()
                                    elif(mt != "" and (mt[0].isnumeric() or mt[0]=="." or mt[0]=="-")):
                                        invert = False
                                        if(mt.startswith("-")):
                                            invert = True
                                            mt = mt[1:len(mt)]
                                        num = ""
                                        while(len(mt)>0 and (mt[0].isnumeric() or mt[0] == ".")):
                                            num = num + mt[0]
                                            mt = mt[1:len(mt)]
                                        num = float(num)
                                        pan = Val(num)
                                        if(invert):
                                            pan = Invert(pan)
                        # Identifies block, for error reporting
                        self.curParseModule = "BLOCK: " + name
                        self.seqs[name] = SeqBlock(self.parseModule(desc,SEQN,i),pan)
                    # Sequence chunk
                    elif(state == SEQ):
                        if(line != "" and not line.isspace()):
                            # Panning module
                            pan = Val(0)
                            # Sequence name
                            name = line.split(":")[0].strip()
                            # Parse meta data
                            if(name.startswith("<")):
                                name = name[1:len(name)].split(">",1)
                                if(name[1].find(">")<0):
                                    raise SCParseError("Missing '>' in meta tag.",i)
                                name, meta = name[1].strip(), name[0].split(",")
                                for mt in meta:
                                    mt = mt.strip()
                                    # Parse pan value / load pan module
                                    if(mt.startswith(("pan", "PAN"))):
                                        mt = mt.split("=")[1].lstrip()
                                        if(mt in self.modules):
                                            pan = self.modules[mt].clone()
                                        elif(mt != "" and (mt[0].isnumeric() or mt[0]=="." or mt[0]=="-")):
                                            invert = False
                                            if(mt.startswith("-")):
                                                invert = True
                                                mt = mt[1:len(mt)]
                                            num = ""
                                            while(len(mt)>0 and (mt[0].isnumeric() or mt[0] == ".")):
                                                num = num + mt[0]
                                                mt = mt[1:len(mt)]
                                            num = float(num)
                                            pan = Val(num)
                                            if(invert):
                                                pan = Invert(pan)
                            # Identifies module, for error reporting
                            self.curParseModule = "SEQ: " + name
                            # Parse the actual sequence data.
                            # Seq lines start/end with first/last bar in the line.
                            startInx = line.find("|")
                            endInx = line.rfind("|")
                            # Parse the pitch module for this sequence line.
                            pitch = self.parseModule(name, TONE, i)
                            # Trim line to sequence data
                            if(startInx >= 0 and endInx > startInx):
                                line = line[startInx:endInx]
                            # Once trimmed, all bars are omitted. Midline bars
                            # are for visual reference only (i.e. measure lines)
                            line = line.replace("|", "")
                            # The sequence pattern
                            pat = []
                            # Count variable (probably could do for loop at this point?)
                            ct = 0
                            while(ct < len(line)):
                                # A space indicates silence
                                if(line[ct] == " "):
                                    pat.append(None)
                                # Hyphen indicates we should sustain prev. inst
                                elif(line[ct] == "-"):
                                    pat.append("-")
                                # Inst names represent an attack by that inst
                                elif(line[ct] in self.insts):
                                    pat.append(self.insts[line[ct]].clone())
                                # Raise an Error if we don't recognize the Inst
                                else:
                                    raise SCParseError("Unrecognized Instrument in sequence line: " + line[ct],i)
                                ct += 1
                            seqLines.append(SeqLine(self, pitch, pat, pan))
                        # Check if this is the end of Sequence chunk --
                        # If so, pack up this Sequence & add it to seqs.
                        if(i+1>=len(text) or text[i+1][0:3] in HEADERS):
                            self.seqs[seqName] = Sequence(seqLines, self, seqPan)
            elif(state == SEQ):
                # Current line is blank, so we are skipping it. However, we still
                # need to check if it is the end of a Sequence chunk & if so
                # add the current Sequence to self.seqs
                if(i+1>=len(text) or text[i+1][0:3] in HEADERS):
                    self.seqs[seqName] = Sequence(seqLines, self, seqPan)
        self.song = Song(songSteps,self)

    def render(self, filename):
        """ Renders the Song into a Wave file.

            Arguments:
            filename -- The path of the output file.
        """

        # Take note of the time before we begin.
        startTime = time.clock()
        # Create our output file.
        out = wave.open(filename, 'wb')

        # Set the number of channels in output file.
        if(self.stereo):
            out.setnchannels(2)
        else:
            out.setnchannels(1)
        # Set sample width (in bytes)
        out.setsampwidth(int(self.depth/8))
        # Set sample rate
        out.setframerate(self.rate)
        # Note song length (for process monitoring)
        # ** Depending on modules in the song, this might not be accurate. **
        len = self.song.length()
        # Print song size info
        print("Song Duration: " + str(int(len/self.rate*100)/100))
        print("Song Sample Length: " + str(len))
        # Total number of samples we have processed so far.
        samps = 0
        # Process chunk counter for whether we should update progress info
        count = 0
        # List of rendered frames.
        frames = []
        # List of pre-normalized frames.
        prenorm = []
        # Current peak value (for normalization)
        peak = 0
        # Value of the last read sample. (We use this after the render loop
        # to add decay, so it can't be declared within the loop.)
        dec = -1
        # Maximum signal absolute value
        maxI = 2**(self.depth-1)-1
        # Express max as a ratio of parser MAX_VAL; to save computations
        max = maxI / MAX_VAL
        # Number of bytes in audio file depth.
        bytes = int(self.depth/8)
        # Whether WAV values are signed or unsigned
        sgned = bytes!=1

        # Main render loop
        while(not self.song.done()):
            # Read & Render next sample for stereo songs
            if(self.stereo):
                dec = self.song.read(stereo=True,signal=True)
                # Render without normalizing
                if(not self.normalize):
                    valL = int(max*limit(dec[0]))
                    valR = int(max*limit(dec[1]))
                    if(bytes == 1):
                        valL += maxI
                        valR += maxI
                    valL = valL.to_bytes(bytes, byteorder="little", signed=sgned)
                    valR = valR.to_bytes(bytes, byteorder="little", signed=sgned)
                    frames.append(valL)
                    frames.append(valR)
                # Normalize ON -- read frame & prepare for normalizing
                else:
                    if(abs(dec[0])>peak):
                        peak = abs(dec[0])
                    if(abs(dec[1])>peak):
                        peak = abs(dec[1])
                    prenorm.append(dec)
            # Render the next sample for mono songs.
            else:
                dec = self.song.read(stereo=False,signal=True)
                # Render without normalizing
                if(not self.normalize):
                    val = int(max*limit(dec))
                    if(bytes == 1):
                        val += maxI
                    val = val.to_bytes(bytes, byteorder="little", signed=sgned)
                    frames.append(val)
                # Normalize ON -- Read sample & prepare for normalization
                else:
                    if(abs(dec)>peak):
                        peak = abs(dec)
                    prenorm.append(dec)
            self.song.step(1)
            count += 1
            samps += 1

            # Every 512 frames, update progress counter.
            if(count > 512):
                elp = time.clock()-startTime
                sys.stdout.write("\r")
                ppct = samps/len
                sys.stdout.write("PROGRESS: " + '{:>5}'.format(str(int(ppct*10000)/100)))
                sys.stdout.write(" : RATE: " + '{:>9}'.format(str(int(samps/elp*100)/100)))
                sys.stdout.write(" : [")
                i = -0.015
                while(i < 1):
                    i += 0.05
                    if(ppct >= i):
                        sys.stdout.write("*")
                    else:
                        sys.stdout.write(" ")
                sys.stdout.write("]")
                sys.stdout.flush()
                count = 0
        # If we're normalizing, we need to scale everything now that we know
        # the final peak value
        if(self.normalize):
            # Calculate ratio between peak value & signal maximum
            # All frames will be scaled by this
            rtio = (MAX_VAL * 0.9999) / peak
            for sp in prenorm:
                # Normalize & render for stereo songs
                if(self.stereo):
                    dec = [sp[0]*rtio,sp[1]*rtio]
                    valL = int(dec[0]*max)
                    valR = int(dec[1]*max)
                    if(bytes == 1):
                        valL += maxI
                        valR += maxI
                    valL = valL.to_bytes(bytes, byteorder="little", signed=sgned)
                    valR = valR.to_bytes(bytes, byteorder="little", signed=sgned)
                    frames.append(valL)
                    frames.append(valR)
                # Normalize & render for mono songs
                else:
                    dec = sp*rtio
                    val = int(dec*max)
                    if(bytes == 1):
                        val += maxI
                    val = val.to_bytes(bytes, byteorder="little", signed=sgned)
                    frames.append(val)
        # Add a bit of decay to the end of the song, to avoid popping.
        # Decay time, in samples
        decay = int(0.001*self.rate)
        for i in range(decay):
            # Scalar to fade the sample out as i approaches decay.
            tmp = 1-(i/decay)
            # Calculate & render decay for stereo songs
            if(self.stereo):
                tmp = [dec[0]*tmp,dec[1]*tmp]
                valL = int(max*tmp[0])
                valR = int(max*tmp[1])
                if(bytes == 1):
                    valL += maxI
                    valR += maxI
                valL = valL.to_bytes(bytes, byteorder="little", signed=sgned)
                valR = valR.to_bytes(bytes, byteorder="little", signed=sgned)
                frames.append(valL)
                frames.append(valR)
            # Calculate & render decay for mono songs
            else:
                tmp *= dec
                val = int(max*dec)
                if(bytes == 1):
                    val += maxI
                val = val.to_bytes(bytes, byteorder="little", signed=sgned)
                frames.append(val)

        # One last update to progress printouts -- so we end on 100%.
        sys.stdout.write("\r")
        ppct = samps/len
        sys.stdout.write("PROGRESS: " + '{:>5}'.format(str(int(ppct*10000)/100)))
        sys.stdout.write(" : RATE: " + '{:>9}'.format(str(int(samps/elp*100)/100)))
        sys.stdout.write(" : [")
        i = -0.015
        while(i < 1):
            i += 0.05
            sys.stdout.write("*")
        sys.stdout.write("]")
        sys.stdout.flush()

        # Write all rendered samples to the WAV file & close it.
        out.writeframes(b''.join(frames))
        out.close()

        # We're done! Print how long it took.
        renderTime = time.clock()-startTime
        print("\nRENDER TIME: " + str(int(renderTime*100)/100) + "                        ")

    def parseModule(self, stng, type, line=0):
        """ Parses a SynthCorona module from a string.

            This is the method to use if you have a full description string to
            parse. This uses popModule to isolate operands in binary operations
            & then wraps them in operator modules as necessary.

            In this method, binary operators are parsed left-to-right, which is in
            turn the only order of operations in Synth-Corona.
            So A+B*C = (A+B)*C != A+(B*C)

            Use any grouping module (Pattern, Set, Series) to change the order of
            operations if necessary.

            Previously created modules/Insts/Sequences can be referenced by
            name. They will be copied into the new module via clone().

            Arguments:
            stng -- String containing the module description.
            type -- Tells us what the module is for. Options: INST, TONE, SEQN, MDLE
            line -- Current parser line; for error reporting.

            Returns the SynthCorona module.
        """

        # Parses the first standalone module & sends us [mdl, remaining string]
        modA = self.popModule(stng, type,line)
        modA, stng = modA[0], modA[1]

        # Now loop through additional operators & modules until we reach end of line.
        while(stng != "" and not stng.isspace()):
            # Whether modA needs to be wrapped in a Cross module.
            cross = False
            # The operator string
            op = stng.lstrip()[0]
            stng = stng[1:len(stng)].lstrip()

            # x indicates a Cross module; flag Cross & carry on
            if(op == "x"):
                op = stng[0]
                stng = stng[1:len(stng)].lstrip()
                cross = True

            # Separate out any meta data for the given operation.
            meta = self.parseMeta(stng)
            meta, stng = meta[0], meta[1]

            # Pop the second operand.
            mdl = self.popModule(stng, type, line)
            mdl, stng = mdl[0], mdl[1]

            # Match up our binary operator & wrap them all into a module
            # + indicates Addition
            if(op == "+"):                        # addition
                alead = True
                for mt in meta:
                    if(mt.startswith(("LEAD","LD","lead","ld"))):
                        mt = mt.split("=")[1]
                        alead = not (mt.startswith("B") or mt.startswith("b"))
                modA = Add(modA, mdl, alead)
            # - indicates Subtraction
            elif(op == "-"):                        # subtraction
                alead = True
                for mt in meta:
                    if(mt.startswith(("LEAD","LD","lead","ld"))):
                        mt = mt.split("=")[1]
                        alead = not (mt.startswith("B") or mt.startswith("b"))
                modA = Subtract(modA, mdl,alead)
            # r indicates Repetition
            elif(op == "r"):                        # repetition
                modA = Repeat(modA, mdl)
            # * indicates Multiplication.
            elif(op == "*"):                        # multiplication
                alead = True
                for mt in meta:
                    if(mt.startswith(("LEAD","LD","lead","ld"))):
                        mt = mt.split("=")[1]
                        alead = not (mt.startswith("B") or mt.startswith("b"))
                modA = Multiply(modA, mdl, alead)
            # / indicates Division.
            elif(op == "/"):                        # multiplication
                alead = True
                for mt in meta:
                    if(mt.startswith(("LEAD","LD","lead","ld"))):
                        mt = mt.split("=")[1]
                        alead = not (mt.startswith("B") or mt.startswith("b"))
                modA = Divide(modA, mdl)
            # i indicates Interpolation.
            elif(op == "i"):
                width = 1
                for mt in meta:
                    # Width is the duration of the interpolation.
                    if(mt.startswith(("WID", "WIDTH", "w", "W"))):
                        mt = mt.split("=")[1]
                        width = float(mt)
                        if(width == None or width <= 0):
                            width = 1
                modA = LinInterp(modA, mdl, width)
            # l indicates Level/Volume. 0 is silent, 9 is max, -x is inverted.
            elif(op == "l"):
                alead = True
                for mt in meta:
                    if(mt.startswith(("LEAD","LD","lead","ld"))):
                        mt = mt.split("=")[1]
                        alead = not (mt.startswith("B") or mt.startswith("b"))
                modA = Level(modA, mdl, alead)
            # v indicates an Envelope. This applies volume control in constant time.
            elif(op == "v"):
                rate = 1
                loop = False
                atk = 0
                rels = -1
                for mt in meta:
                    if(mt.startswith(("REL","rel"))):
                        mt = mt.split("=")[1].strip()
                        rels = float(mt)
                        if(rels == None or rels <= 0):
                            rels = -1
                    elif(mt.startswith(("R","r","RATE","rate"))):
                        mt = mt.split("=")[1].strip()
                        rate = float(mt)
                        if(rate == None or rate <= 0):
                            rate = 1
                    elif(mt.startswith(("L","l","LOOP","loop"))):
                        mt = mt.split("=")[1].strip()
                        loop = mt.startswith(("T","t","1"))
                    elif(mt.startswith(("ATK","atk","ATTACK","attack"))):
                        mt = mt.split("=")[1].strip()
                        atk = float(mt)
                        if(atk == None or atk < 0):
                            atk = 0
                modA = Envelope(modA, mdl,
                        (self.tempo*self.beat)/(60*self.rate)*rate,loop,atk,rels)
            # s indicates Speed/Playback rate. This is applied to constant time
            # updates as well, so it does affect pitch!
            elif(op == "s"):
                alead = True
                for mt in meta:
                    if(mt.startswith(("LEAD","LD","lead","ld"))):
                        mt = mt.split("=")[1]
                        alead = not (mt.startswith("B") or mt.startswith("b"))
                modA = Speed(modA, mdl, alead)
            # n indicates Length override.
            elif(op == "n"):
                modA = Length(modA, mdl)
            # If we need to, wrap the operation module in a Cross module.
            if(cross):
                modA = Cross(modA)
        return modA

    def popModule(self, stng, type, line=0):
        """ 'Pops' the first fully-described module off the front of the given
            string and parses it.

            This method handles parsing of all modules except binary operators,
            which are handled by parseModule(). Given a string describing a
            binary operation, this method will parse the first operand.

            This method is called by parseModule() & is mostly intended to reduce
            code repetition within that method.

            Keyword arguments:
            stng -- String containing the full module description.
            type -- Tells us what this module is for. Options: INST, TONE, SEQN, MDLE.
            line -- Current parser line; for error reporting.

            Returns a 2-tuple: (parsed first module, remaining string).
        """

        # The module we're parsing.
        modA = None
        # Whether we will need to wrap with an Invert (indicated by a '-')
        invert = False
        # Constant-rate indicator. -1 means skip; Any positive value is read as
        # the rate value for a Const module.
        const = -1
        # If const != -1, this indicates whether our Const module should loop.
        cloop = True

        stng = stng.lstrip()
        # Throw an error if we are grabbing an empty module.
        if(stng == "" or stng.isspace()):
            raise SCParseError("Empty module at " + self.curParseModule + ".",line)
            return (Val(0), "")
        # A '-' indicates that we will invert the popped module (Invert).
        if(stng[0] == "-"):
            stng = stng[1:len(stng)]
            invert = True
        # A 'c' indicates that we will apply a constant-rate module (Const).
        elif(stng[0] == "c"):
            const = 1
            stng = stng[1:len(stng)].lstrip()
            # Const currently offers 2 meta tags: 'r' or 'rate' for the speed,
            # and 'l' or 'loop' for whether to loop the results.
            #if(stng[0] == "<"):
            #    end = stng.find(">")
            #    if(end<0):
            #        raise SCParseError("Missing '>' in meta tag.",line)
            #    end += 1
            #    meta, stng = stng[0:end], stng[end:len(stng)]
            if(len(stng)>0 and stng[0] == "<"):
                meta = self.parseMeta(stng)
                meta, stng = meta[0], meta[1]
                #meta = meta[1:len(meta)-1].strip().split(",")
                for mt in meta:
                    if(mt.startswith(("R", "r", "RATE", "rate"))):
                        const = float(mt.split("=")[1])
                        if(const == None or const < 1):
                            const = 1
                    elif(mt.startswith(("L", "l", "LOOP", "loop"))):
                        mt = mt.split("=")[1].strip()
                        cloop = mt.startswith(("T","t","1"))

        value = None
        # For TONE or generic modules, 2-char pitch literal ("d4").
        if((type == TONE or type == MDLE) and stng[0:2] in self.tones):
            value = self.tones[stng[0:2]]
            stng = stng[2:len(stng)]
        # For TONE or generic modules, 3-char pitch literal ("C#4")
        elif((type == TONE or type == MDLE) and stng[0:3] in self.tones):
            value = self.tones[stng[0:3]]
            stng = stng[3:len(stng)]
        # Numeric literal
        elif(stng[0].isnumeric() or stng[0] == "."):
            num = ""
            while(len(stng)>0 and (stng[0].isnumeric() or stng[0] == ".")):
                num = num + stng[0]
                stng = stng[1:len(stng)]
            value = float(num)

        # A value module, either from pitch or numerics parsed above
        if(value != None):
            vlength = 1
            if(len(stng)>0 and stng[0] == "<"):
                meta = self.parseMeta(stng)
                meta, stng = meta[0], meta[1]
                #meta = meta[1:len(meta)-1].strip().split(",")
                for mt in meta:
                    if(mt.startswith(("LEN","len","LN","ln"))):
                        mt = mt.split("=")[1].strip()
                        vlength = float(mt)
            modA = Val(value, vlength)
        # Pattern
        elif(stng[0] == "["):
            set = self.extractPattern(stng,line)
            stng, modA = set[1], self.parsePattern(set[0], type)
        # Set
        elif(stng[0] == "{"):
            set = self.extractSet(stng,line)
            stng, modA = set[1], self.parseSet(set[0], type)
        # Series
        elif(stng[0] == "("):
            set = self.extractSeries(stng,line)
            stng, modA = set[1], self.parseSeries(set[0], type)
        # Otherwise, check if it is a reference to another module.
        else:
            i = 0
            while(i < len(stng) and stng[i] not in RESERVED):
                i+= 1
            name = stng[0:i]
            stng = stng[i:len(stng)]
            meta = self.parseMeta(stng)
            meta, stng = meta[0], meta[1]
            if(type == INST or type == MDLE):
                if(name in self.insts):
                    modA = self.insts[name].clone()
                    for mt in meta:
                        mt = mt.strip()
                        if(mt.startswith(("MODULE", "MDL", "module", "mdl"))):
                            modA = modA.mdl
                        elif(mt.startswith(("period", "PERIOD", "prd", "PRD"))):
                            mt = mt.split("=")[1].lstrip()
                            modA.period = int(mt)
                        elif(mt.startswith(("loop", "LOOP", "l", "L"))):
                            mt = mt.split("=")[1].lstrip()
                            modA.loop = mt.startswith("t") or mt.startswith("T") or mt.startswith("1")
                        elif(mt.startswith(("sus", "SUS", "SUSTAIN", "sustain", "s", "S"))):
                            mt = mt.split("=")[1].lstrip()
                            modA.sus = mt.startswith("t") or mt.startswith("T") or mt.startswith("1")
                        elif(mt.startswith(("BASE","base"))):
                            mt = mt.split("=")[1].lstrip()
                            ins = self.insts[mt]
                            if(ins != None):
                                period = ins.period
                                loop = ins.loop
                                sus = ins.sus
                elif(name in self.modules):
                    modA = self.modules[name].clone()
                else:
                    raise SCParseError("Invalid inst: " + name, line)
                    #print("Error! Invalid inst: " + name + ". Line: " + str(line))
            elif(type == TONE):
                if(name in self.tones):
                    vlength = 1
                    for mt in meta:
                        if(mt.startswith(("LEN","len","LN","ln"))):
                            mt = mt.split("=")[1].strip()
                            vlength = float(mt)
                            if(vlength == None or vlength <= 0):
                                vlength = 1
                    modA = Val(self.tones[name], vlength)
                elif(name in self.modules):
                    modA = self.modules[name].clone()
                else:
                    # this is an error
                    raise SCParseError("Invalid Pitch: " + name, line)
                    #print("Error! Invalid Pitch: " + name)
            elif(type == SEQN):
                if(name in self.seqs):
                    modA = self.seqs[name].clone()
                elif(name in self.modules):
                    modA = SeqBlock(self.modules(),Val(0))
                else:
                    # this is an error
                    raise SCParseError("Invalid Sequence: " + name,line)
                    #print("Error! Invalid Sequence: \"" + name + "\"")
        # at this point, we need modA & to've cut modA out of stng
        # now we'll test for operatens, and add them
        # wrap modA with any single operatens
        if(invert):
            modA = Invert(modA)
        if(const>0):
            modA = Const(modA,(self.tempo*self.beat)/(60*self.rate),const,cloop)

        return (modA, stng)

    def parseMeta(self, stng):
        """ Separates out individual meta tags from a meta description.

            Tags must be delimited by commas.

            Arguments:
            stng -- The meta description. This can include brackets, or not.
        """

        stng = stng.lstrip()

        if(len(stng)<=0):
            return ([], stng)

        meta = []
        if(stng[0] == "<"):
            endmeta = stng.find(">")
            if(endmeta<0):
                raise SCParseException("Missing '>' in meta tag.",i)
            meta = stng[1:endmeta]
            stng = stng[endmeta+1:len(stng)]
            meta = meta.strip().split(",")

        return (meta, stng)

    def extractPattern(self, stng, line=0):
        """ Separates out a Pattern description from a larger description
            string, and trims away the brackets.

            Arguments:
            stng -- A module description.
            line -- Current parser line, for error reporting.

            Returns a 2-tuple: (pattern description, remaining string)
        """

        inx = 0
        brackets = 0

        while(inx < len(stng)):
            if(stng[inx] == "["):
                brackets += 1
            elif(stng[inx] == "]"):
                brackets -= 1
            inx += 1
            if(brackets == 0):
                return (stng[1:inx-1], stng[inx:len(stng)])
        if(brackets > 0):
            raise SCParseError("Expected ']'.",line)
            #print("Error: Expecting ']' in line " + str(line) + ".")
        else:
            raise SCParseError("Expected '['.",line)
            #print("Error: Expecting '[' in line " + str(line) + ".")

    def extractSet(self, stng, line=0):
        """ Separates out a Set description from a larger description
            string, and trims away the brackets.

            Arguments:
            stng -- A module description.
            line -- Current parser line, for error reporting.

            Returns a 2-tuple: (set description, remaining string)
        """

        inx = 0
        brackets = 0

        while(inx < len(stng)):
            if(stng[inx] == "{"):
                brackets += 1
            elif(stng[inx] == "}"):
                brackets -= 1
            inx += 1
            if(brackets == 0):
                return (stng[1:inx-1], stng[inx:len(stng)])
        if(brackets > 0):
            raise SCParseError("Expected '}'.",line)
        else:
            raise SCParseError("Expected '{'.",line)

    def extractSeries(self, stng,line=0):
        """ Separates out a Series description from a larger description
            string, and trims away the brackets.

            Arguments:
            stng -- A module description.
            line -- Current parser line, for error reporting.

            Returns a 2-tuple: (series description, remaining string)
        """

        inx = 0
        brackets = 0

        while(inx < len(stng)):
            if(stng[inx] == "("):
                brackets += 1
            elif(stng[inx] == ")"):
                brackets -= 1
            inx += 1
            if(brackets == 0):
                return (stng[1:inx-1], stng[inx:len(stng)])
        if(brackets > 0):
            raise SCParseError("Expecting ')'.",line)
        else:
            raise SCParseError("Expecting '('.",line)

    def parseSongLine(self, stng, mdls, line=0):
        """ Parses a list of Sequence modules, to be added to the Song.

            This is called for each non-empty line of the SNG chunk, and newly
            parsed Sequences are added to mdls.

            Arguments:
            stng -- String representing the line of Sequences.
            mdls -- List of Song modules. We append new Sequences to this.
            line -- Current parser line, for error reporting.
        """

        bits = []
        brace = 0
        bracket = 0
        paren = 0
        inx = 0
        while(inx < len(stng)):
            if(stng[inx]=="," and brace == 0
                    and bracket == 0 and paren == 0):
                bits.append(stng[0:inx])
                stng = stng[inx+1:len(stng)]
                inx = 0
            else:
                if(stng[inx]=="["):
                    bracket += 1
                elif(stng[inx]=="]"):
                    bracket -= 1
                elif(stng[inx]=="{"):
                    brace += 1
                elif(stng[inx]=="}"):
                    brace -= 1
                elif(stng[inx]=="("):
                    paren += 1
                elif(stng[inx]==")"):
                    paren -= 1
                inx += 1
        if(len(stng)>0):
            bits.append(stng)

        for ln in bits:
            ln = ln.strip()
            mdls.append(self.parseModule(ln,SEQN,line))

    def parsePattern(self, stng, type, line=0):
        """ Parse a Pattern module.

            This uses parseModule() for each module, then wraps the list with
            a Pattern module.

            Arguments:
            stng -- Pattern description string (bounding brackets removed)
            type -- The type of module we're parsing. Options: INST, TONE, SEQN, MDLE.
            line -- Current parser line, for error-reporting.
        """

        bits = []
        brace = 0
        bracket = 0
        paren = 0
        inx = 0
        while(inx < len(stng)):
            if(stng[inx]=="," and brace == 0
                    and bracket == 0 and paren == 0):
                bits.append(stng[0:inx])
                stng = stng[inx+1:len(stng)]
                inx = 0
            else:
                if(stng[inx]=="["):
                    bracket += 1
                elif(stng[inx]=="]"):
                    bracket -= 1
                elif(stng[inx]=="{"):
                    brace += 1
                elif(stng[inx]=="}"):
                    brace -= 1
                elif(stng[inx]=="("):
                    paren += 1
                elif(stng[inx]==")"):
                    paren -= 1
                inx += 1
        if(len(stng)>0):
            bits.append(stng)
        ary = []
        for ln in bits:
            ary.append(self.parseModule(ln.strip(), type, line))
        return Pattern(ary)

    def parseSet(self, stng, type, line=0):
        """ Parse a Set module.

            This uses parseModule() for each module, then wraps the list with
            a Set module.

            Arguments:
            stng -- Set description string (bounding brackets removed)
            type -- The type of module we're parsing. Options: INST, TONE, SEQN, MDLE.
            line -- Current parser line, for error-reporting.
        """

        bits = []
        brace = 0
        bracket = 0
        paren = 0
        inx = 0
        while(inx < len(stng)):
            if(stng[inx]=="," and brace == 0
                    and bracket == 0 and paren == 0):
                bits.append(stng[0:inx])
                stng = stng[inx+1:len(stng)]
                inx = 0
            else:
                if(stng[inx]=="["):
                    bracket += 1
                elif(stng[inx]=="]"):
                    bracket -= 1
                elif(stng[inx]=="{"):
                    brace += 1
                elif(stng[inx]=="}"):
                    brace -= 1
                elif(stng[inx]=="("):
                    paren += 1
                elif(stng[inx]==")"):
                    paren -= 1
                inx += 1
        if(len(stng)>0):
            bits.append(stng)

        ary = []
        for ln in bits:
            ary.append(self.parseModule(ln.strip(), type, line))
        return Set(ary)

    def parseSeries(self, stng, type, line=0):
        """ Parse a Series module.

            This uses parseModule() for each module, then wraps the list with
            a Series module.

            Arguments:
            stng -- Series description string (bounding brackets removed)
            type -- The type of module we're parsing. Options: INST, TONE, SEQN, MDLE.
            line -- Current parser line, for error-reporting.
        """

        bits = []
        brace = 0
        bracket = 0
        paren = 0
        inx = 0
        while(inx < len(stng)):
            if(stng[inx]=="," and brace == 0
                    and bracket == 0 and paren == 0):
                bits.append(stng[0:inx])
                stng = stng[inx+1:len(stng)]
                inx = 0
            else:
                if(stng[inx]=="["):
                    bracket += 1
                elif(stng[inx]=="]"):
                    bracket -= 1
                elif(stng[inx]=="{"):
                    brace += 1
                elif(stng[inx]=="}"):
                    brace -= 1
                elif(stng[inx]=="("):
                    paren += 1
                elif(stng[inx]==")"):
                    paren -= 1
                inx += 1
        if(len(stng)>0):
            bits.append(stng)

        ary = []
        for ln in bits:
            ary.append(self.parseModule(ln.strip(), type, line))
        return Series(ary)

class SeqLine(SCModule):
    """ Represents a single line of a Sequence module.

        This corresponds to a single line of the SEQ chunk of a SC file.
        SeqLine has a single module determining pitch and can play only 1
        instrument at a time. This is similar to a monophonic "voice" within
        a piece, though different Instruments can be used in the same SeqLine.
    """

    def __init__(self, parent, pitch, pat, pan=None):
        """ Initializes with the given parent and pitch module and the given
            pattern.

            The pattern data is extracted by SynthCorona.parse() into a list.
            Each index is either an Instrument or a string: "-" or " ",
            with hyphens indicating sustain & spaces indicating release/silence.

            Arguments:
            parent -- The SynthCorona module to which this part belongs.
            pitch -- Pitch module.
            pat -- Pattern data list.
            pan -- Pan module. Defaults to Val(0) (centered) if none is given.
        """

        self.parent = parent
        self.seq = None
        self.pat = pat
        self.pitch = pitch
        self.pan = pan
        if(self.pan == None):
            self.pan = Val(0)
        self.cur = 0
        self.curInx = 0
        if(self.pat[self.curInx] == None or self.pat[self.curInx] == "-"):
            self.curInst = None
        else:
            self.curInst = self.pat[self.curInx]

    def step(self, delta, const=-1):
        self.cur += delta
        if(const != ADJUST):
            self.pitch.step(self.parent.frameslice, 1)
            self.pan.step(self.parent.frameslice,1)
            if(self.curInst != None):
                if(self.cur >= self.parent.framesperstep-self.parent.rel_time and
                        (self.curInx >= len(self.pat)-1 or self.pat[self.curInx+1] != "-")):
                    self.curInst.stop()
                    self.seq.tails.append(self.curInst.clone())
                    self.curInst = None
                elif(self.curInst.stopped):
                    self.seq.tails.append(self.curInst.clone())
                    self.curInst = None
                else:
                    self.curInst.step(delta,const)

        if(self.cur >= self.parent.framesperstep):
            self.cur %= self.parent.framesperstep
            self.curInx += 1
            if(not self.done()):
                if(self.pat[self.curInx] != "-"):
                    self.curInst = self.pat[self.curInx]

    def read(self,tails=False,stereo=True,signal=True):
        if(stereo):
            if(self.pitch.done()):
                extra = self.pitch.get_extra()
                self.pitch.reset()
                self.pitch.step(extra,ADJUST)
            if(self.pan.done()):
                extra = self.pan.get_extra()
                self.pan.reset()
                self.pan.step(extra,ADJUST)
            if(self.curInst != None):
                freq = self.parent.freqs[int(self.pitch.read(stereo=False,signal=False))]
                if(self.curInst.freq != freq):
                    self.curInst.set_freq(freq)
                return pan(self.curInst.read(),self.pan.read(stereo=False,signal=False))
            else:
                return [0,0]
        else:
            if(self.pitch.done()):
                extra = self.pitch.get_extra()
                self.pitch.reset()
                self.pitch.step(extra,ADJUST)
            if(self.curInst != None):
                freq = self.parent.freqs[int(self.pitch.read(stereo=False,signal=False))]
                if(self.curInst.freq != freq):
                    self.curInst.set_freq(freq)
                return self.curInst.read(stereo=False,signal=False)
            else:
                return 0

    def reset(self):
        self.curInx = 0
        self.cur = 0
        for p in self.pat:
            if(p != None and p != "-"):
                p.clear()
        if(self.pat[0] != "-"):
            self.curInst = self.pat[0]

    def clear(self):
        self.curInx = 0
        self.cur = 0
        self.pitch.clear()
        self.pan.clear()
        for p in self.pat:
            if(p != None and p != "-"):
                p.clear()
        if(self.pat[0] != "-"):
            self.curInst = self.pat[0]

    def done(self):
        return self.curInx >= len(self.pat)

    def get_extra(self):
        if(self.done()):
            return self.cur
        else:
            return 0

    def length(self):
        return len(self.pat)*self.parent.framesperstep

    def clone(self):
        patclone = []
        for p in self.pat:
            if(p != None and p != "-"):
                patclone.append(p.clone())
            else:
                patclone.append(p)
        return SeqLine(self.parent, self.pitch.clone(), patclone, self.pan.clone())

    def to_string(self):
        """ Compiles and returns a string representing this SeqLine.

            This was probably for testing something -- it isn't pretty.
        """
        return ("LINE: " + self.pitch.to_string() + ": " + self.pat.to_string())

class Sequence(SCModule):
    """ Contains sequence data (in the form of SeqLines) for a section/pattern
        within a song.

        Sequences are Modules, so they can be combined/manipulated as with
        any other module, though this must be done under the BLK (Block) header
        of a SC file.
    """

    def __init__(self, lines, parent, pan=None):
        """ Initializer.

            Arguments:
            lines -- The SeqLines that comprise this Sequence.
            parent -- The SynthCorona parent.
            pan -- Option panning module (pans the whole pattern).
        """

        self.parent = parent
        self.lines = lines
        self.pan = pan
        if(self.pan == None):
            self.pan = Val(0)
        self.stopped = False
        self.len = 0
        for l in lines:
            l.seq = self
            if(l.length() > self.len):
                self.len = l.length()
        self.tails = []

    def step(self, delta, const=-1):
        if(const == STOP):
            self.stopped = True
            return
        if(not self.stopped):
            self.pan.step(delta,1)
            for ln in self.lines:
                # Const is always 1, so you can speed up Seq's without
                # changing instrument pitches.
                # However, this means we MUST update Seq's once per sample.
                if(not ln.done()):
                    ln.step(delta,1)

    def step_tails(self, delta, const=-1):
        for t in self.tails:
            # just a regular step here: we're stepping the Insts in tails
            t.step(delta,1)
            if(t.done()):
                self.tails.remove(t)

    def read(self,tails=False,stereo=True,signal=True):
        if(tails):
            if(stereo):
                sum = [0,0]
                for t in self.tails:
                    # we always set tails=F because tails should be an Inst--
                    # tails is more for Sequences
                    val = t.read(False,stereo,signal)
                    sum[0] += val[0]
                    sum[1] += val[1]
                return pan(sum,self.pan.read(stereo=False,signal=False))
            else:
                sum = 0
                for t in self.tails:
                    # we always set tails=F because tails should be an Inst--
                    # tails is more for Sequences
                    sum += t.read(False,stereo,signal)
                return sum
        else:
            if(stereo):
                if(self.pan.done()):
                    extra = self.pan.get_extra()
                    self.pan.reset()
                    self.pan.step(extra,ADJUST)
                sum = [0,0]
                if(not self.stopped):
                    for ln in self.lines:
                        if(not ln.done()):
                            val = ln.read(tails,stereo,signal)
                            sum[0] += val[0]
                            sum[1] += val[1]
                return pan(sum,self.pan.read(stereo=False,signal=False))
            else:
                sum = 0
                if(not self.stopped):
                    for ln in self.lines:
                        if(not ln.done()):
                            sum += ln.read(tails,stereo,signal)
                return sum

    def reset(self):
        self.pan.reset()
        for ln in self.lines:
            ln.reset()
        self.stopped = False

    def clear(self):
        self.pan.clear()
        for ln in self.lines:
            ln.clear()
        #self.tails = []
        self.stopped = False

    def done(self):
        if(not self.stopped):
            for ln in self.lines:
                if(not ln.done()):
                    return False
            return True
        else:
            return len(self.tails) == 0

    def get_extra(self):
        return self.lines[0].get_extra()

    def length(self):
        if(not self.stopped):
            return self.len
        else:
            len = 0
            for t in self.tails:
                if(t.length() > len):
                    len = t
            return len

    def clone(self):
        tlines = []
        for l in self.lines:
            tlines.append(l.clone())
        return Sequence(tlines, self.parent, self.pan.clone())

class SeqBlock(SCModule):
    """ Sequence wrapper for modules. When Sequence modules are parsed by the
        BLK/PAT chunk, they will be packaged in this.

        Like basic Sequences, this has a Sequence-level panning module, pan,
        which defaults to centered.
    """

    def __init__(self, module, pan=None):
        """ Initializer.

            Arguments:
            module -- The module to be wrapped. Should contain Sequence data.
            pan -- Optional panning module. Defaults to Val(0)
        """

        self.module = module
        if(pan == None):
            pan = Val(0)
        self.pan = pan

    def step(self, delta, const=-1):
        self.pan.step(delta,const)
        self.module.step(delta,const)

    def step_tails(self, delta, const=-1):
        self.module.step_tails(delta,const)

    def read(self,tails=False,stereo=True,signal=True):
        if(stereo):
            if(self.pan.done()):
                extra = self.pan.get_extra()
                self.pan.reset()
                self.pan.step(extra,ADJUST)
            return pan(self.module.read(tails,stereo,signal),self.pan.read(stereo=False,signal=False))
        else:
            return self.module.read(tails,stereo,signal)

    def reset(self):
        self.pan.reset()
        self.module.reset()

    def clear(self):
        self.pan.clear()
        self.module.clear()

    def done(self):
        return self.module.done()

    def get_extra(self):
        return self.module.get_extra()

    def length(self):
        return self.module.length()

    def clone(self):
        return SeqBlock(self.module.clone(),self.pan.clone())

class Song(SCModule):
    """ Module class representing a song.

        This is primarily composed of a list of Sequences (or SeqBlock), which
        are run and read one after the other.
    """

    def __init__(self, pat, parent):
        """ Initializer.

            Arguments:
            pat -- Sequence pattern that comprises the Song.
            parent -- SynthCorona that is running this show.
        """

        self.pat = pat
        self.curInx = 0
        self.parent = parent
        self.tails = []

    def step(self, delta, const=-1):
        # Step Sequences that are sustaining (self.tails)
        for t in self.tails:
            t.step_tails(delta, const)
            if(t.done()):
                self.tails.remove(t)
        if(self.curInx < len(self.pat)):
            self.pat[self.curInx].step(delta,delta)
            # Step sustained notes in current Sequence
            self.pat[self.curInx].step_tails(delta,delta)
            if(self.pat[self.curInx].done()):
                self.pat[self.curInx].step(0,STOP)
                if(getattr(self.pat[self.curInx], "no_tails", None) == None):
                    self.tails.append(self.pat[self.curInx])
                self.curInx += 1

    def read(self,tails=False,stereo=True,signal=False):
        if(stereo):
            sum = [0,0]
            if(self.curInx < len(self.pat)):
                val = self.pat[self.curInx].read(tails,stereo,signal)
                sum[0] += val[0]
                sum[1] += val[1]
                if(getattr(self.pat[self.curInx], "no_tails", None) == None):
                    val = self.pat[self.curInx].read(True,stereo,signal)
                    sum[0] += val[0]
                    sum[1] += val[1]
            for t in self.tails:
                val = t.read(True,stereo,signal)
                sum[0] += val[0]
                sum[1] += val[1]
            return sum
        else:
            sum = 0
            if(self.curInx < len(self.pat)):
                sum += self.pat[self.curInx].read(tails,stereo,signal)
                if(getattr(self.pat[self.curInx], "no_tails", None) == None):
                    # add tails from current Sequence.
                    sum += self.pat[self.curInx].read(True,stereo,signal)
            for t in self.tails:
                # add tails from past Sequences.
                sum += t.read(True,stereo,signal)
            return sum

    def reset(self):
        self.clear()

    def clear(self):
        self.curInx = 0
        for p in self.pat:
            p.clear()

    def done(self):
        return len(self.tails) == 0 and (self.curInx >= len(self.pat))

    def get_extra(self):
        return self.curInx-len(self.pat)

    def length(self):
        sum = 0
        for mdl in self.pat:
            sum += mdl.length()
        return sum

class Inst(SCModule):
    """ Module representing an instrument/synth.

        Along with core module functions, Insts also have set_freq(), which
        sets the current pitch.

        Insts also have several unique properties:
        period -- Indicates the length of 1 period of the core waveform.
        loop -- Whether this Inst should loop after its module has finished.
        sus -- Whether this Inst should sustain (until module completion), after stop().
        pan -- Instrument-level pan module.

        Pitch is achieved by playing the module at a rate based on the frequency
        and the wave period. This rate affects delta in step() calls, but it does
        not affect const, (the constant-time argument).

        Similarly, Inst always uses const to step, to prevent other adjustments
        to delta from affecting the pitch. The main exception to this is the
        Speed module, which does affect pitch (by changing the const value).

        Because of the above, you can easily nest Insts within other Insts
        without affecting pitch.
    """

    def __init__(self, parent, module, prd=-1, loop=True, sus=False, pan=None):
        """ Initializer.

            Arguments:
            parent -- SynthCorona parent.
            module -- Module for creating the Inst's sound.
            prd -- Period length. If -1, we will use module.length(), which will
                work as long as the module describes exactly 1 oscillation.
            loop -- Whether to loop our module. Default: True.
            sus -- Whether to sustain our module. Default: False. If true, loop is overrided to False.
            pan -- Instrument-level panning module. Defaults to centered.
        """

        if(sus):
            loop = False
        self.parent = parent
        self.mdl = module
        self.stopped = False
        self.release = None
        if(prd < 1):
            self.period = self.mdl.length()
        else:
            self.period = prd
        self.loop = loop
        self.sus = sus
        self.pan = pan
        if(self.pan == None):
            self.pan = Val(0)
        self.rate = 0
        self.freq = 1
        self.last = 0

    def set_freq(self, freq):
        self.freq = freq
        self.rate = self.freq*self.period/self.parent.rate
        self.mdl.set_freq(freq)

    def step(self, delta, const=-1):
        if(const < 0):
            # bypass rate adjustment
            if(const == ADJUST):
                if(self.stopped):
                    self.release.step(delta,const)
                else:
                    self.mdl.step(delta,const)
                return
            # stop command
            elif(const == STOP):
                self.mdl.step(0,RELEASE)
                self.pan.step(0,RELEASE)
                if(self.sus):
                    self.release = self.mdl
                else:
                    if(not self.mdl.done()):
                        self.release = Multiply(self.mdl, Const(LinInterp(Val(1),Val(0),self.parent.rel_time),1),False)
                    else:
                        self.release = Const(LinInterp(StereoVal([self.last[0],self.last[1]]),Val(0),self.parent.rel_time),1)
                self.stopped = True
                return
            # release command -- pass this forward to our module
            elif(const == RELEASE):
                self.mdl.step(0,const)
                self.pan.step(0,const)
                return
            # otherwise, set const to delta
            else:
                const=delta
        self.pan.step(const*self.rate,const)
        if(self.stopped):
            self.release.step(const*self.rate, const)
        else:
            self.mdl.step(const*self.rate, const)
            if(self.done()):
                if(self.loop):
                    extra = self.get_extra()
                    self.reset()
                    # ADJUST Const tells Inst to bypass its freq. rate
                    self.step(extra,ADJUST)
                else:
                    self.stop()

    def read(self,tails=False,stereo=True,signal=True):
        if(stereo):
            if(self.pan.done()):
                extra = self.pan.get_extra()
                self.pan.reset()
                self.pan.step(extra,ADJUST)
            if(self.stopped):
                self.last = pan(self.release.read(tails,stereo,signal),self.pan.read(stereo=False,signal=False))
                return self.last
            else:
                if(self.loop or not self.done()):
                    self.last = pan(self.mdl.read(tails,stereo,signal),self.pan.read(stereo=False,signal=False))
                    return self.last
                else:
                    return [0,0]
        else:
            if(self.stopped):
                val = self.release.read(tails,stereo,signal)
                self.last = [val,val]
                return val
            else:
                if(self.loop or not self.done()):
                    val = self.mdl.read(tails,stereo,signal)
                    self.last = [val,val]
                    return val
                else:
                    return 0

    def reset(self):
        self.mdl.reset()
        self.pan.reset()

    def clear(self):
        self.release = None
        self.stopped = False
        self.mdl.clear()
        self.pan.clear()

    def done(self):
        if(self.stopped):
            return self.release.done()
        else:
            return self.mdl.done()

    def get_extra(self):
        if(self.stopped):
            return self.release.get_extra()
        else:
            return self.mdl.get_extra()

    def clone(self):
        cp = Inst(self.parent, self.mdl.clone(), self.period, self.loop, self.sus, self.pan.clone())
        cp.stopped = self.stopped
        if(self.release != None):
            cp.release = self.release.clone()
        else:
            cp.release = None
        cp.rate = self.rate
        cp.freq = self.freq
        return cp

    def length(self):
        if(self.stopped):
            return self.release.length()
        else:
            return self.mdl.length()

    def stop(self):
        self.step(0,STOP)

class Val(SCModule):
    """ Module representing a single fixed value.

        This module has length 1 and always returns its value on read().
    """

    def __init__(self, val=0, ln=1):
        self.val = val
        self.cur = 0
        self.no_tails = True
        self.len = ln

    def step(self, delta, const=-1):
        if(const >= 0 or const == DELTA or const == ADJUST):
            self.cur += delta

    def step_tails(self, delta, const=-1):
        #self.step(delta, const)
        pass

    # 'tails' here is irrelevant; search for "no_tails" property to avoid doubling
    def read(self,tails=False,stereo=True,signal=True):
        if(stereo):
            return [self.val,self.val]
        else:
            return self.val

    def reset(self):
        self.cur = 0

    def clear(self):
        self.cur = 0

    def done(self):
        return self.cur >= self.len

    def get_extra(self):
        if(self.done()):
            return self.cur-self.len
        else:
            return 0

    def clone(self):
        tmp = Val(self.val, self.len)
        tmp.cur = self.cur
        return tmp

    def length(self):
        return self.len

    def set_freq(self, freq):
        pass

class StereoVal(SCModule):
    """ Module representing a single value, in stereo.

        Right now, the only we place we use this is when creating tails to fade
        out instruments. It isn't necessary for general purposes, as simply
        panning a Val module covers that better.

        Like Val, StereoVal has a length of 1.
    """

    def __init__(self, val=[0,0], ln=1):
        """ Initializer.

            Arguments:
            val -- The value, as a 2-tuple or 2-list.
            ln -- The module length. Defaults to 1.
        """

        self.val = val
        self.cur = 0
        self.no_tails = True
        self.len = ln

    def step(self, delta, const=-1):
        if(const >= 0 or const == DELTA or const == ADJUST):
            self.cur += delta

    def step_tails(self, delta, const=-1):
        self.step(delta, const)

    # 'tails' here is irrelevant; search for "no_tails" property to avoid doubling
    def read(self,tails=False,stereo=True,signal=True):
        if(stereo):
            return self.val
        else:
            return self.val[0]

    def reset(self):
        self.cur = 0

    def clear(self):
        self.cur = 0

    def done(self):
        return self.cur >= self.len

    def get_extra(self):
        if(self.done()):
            return self.cur-self.len
        else:
            return 0

    def clone(self):
        tmp = StereoVal(self.val, self.len)
        tmp.cur = self.cur
        return tmp

    def length(self):
        return self.len

    def set_freq(self, freq):
        pass

class Pattern(SCModule):
    """ Represents a sequence of modules, to be played one after the other.

        This differs from Series in that Pattern plays through each of its
        modules before finishing. Series plays through its current module,
        finishes, then plays the next one after reset().

        Accordingly, the length of Pattern is the sum of the lengths of its
        modules.
    """

    def __init__(self, pat=(Val(0),Val(1))):
        """ Initializer

            Arguments:
            pat -- The pattern, as a list of Modules.
        """

        self.pat = pat
        self.curInx = 0
        self.extra = 0

    def step(self, delta, const=-1):
        if(not self.done()):
            self.pat[self.curInx].step(delta, const)
            while(not self.done() and self.pat[self.curInx].done()):
                self.extra = self.pat[self.curInx].get_extra()
                self.pat[self.curInx].reset()
                self.curInx += 1
                if(not self.done()):
                    self.pat[self.curInx].step(self.extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        if(tails):
            if(stereo):
                cur = None
                if(self.curInx < len(self.pat)):
                    cur = self.pat[self.curInx]
                sum = [0,0]
                for mdl in self.pat:
                    if(mdl != cur and getattr(mdl, "no_tails", None) == None):
                        val = mdl.read(tails,stereo,signal)
                        sum[0] += val[0]
                        sum[1] += val[1]
                    elif(mdl == cur):
                        val = mdl.read(tails,stereo,signal)
                        sum[0] += val[0]
                        sum[1] += val[1]
                return sum
            else:
                cur = None
                if(self.curInx < len(self.pat)):
                    cur = self.pat[self.curInx]
                sum = 0
                for mdl in self.pat:
                    if(mdl != cur and getattr(mdl, "no_tails", None) == None):
                        sum += mdl.read(tails,stereo,signal)
                    elif(mdl == cur):
                        sum += mdl.read(tails,stereo,signal)
                return sum
        else:
            if(not self.done()):
                return self.pat[self.curInx].read(tails,stereo,signal)
            else:
                if(stereo):
                    return [0,0]
                else:
                    return 0

    def step_tails(self, delta, const=-1):
        for mdl in self.pat:
            mdl.step_tails(delta, const)

    def reset(self):
        if(not self.done()):
            self.pat[self.curInx].reset()
        self.curInx = 0

    def clear(self):
        self.curInx = 0
        for p in self.pat:
            p.clear()

    def done(self):
        return self.curInx>=len(self.pat)

    def get_extra(self):
        if(self.done()):
            return self.extra
        else:
            return 0

    def clone(self):
        pt = []
        for p in self.pat:
            pt.append(p.clone())
        tmp = Pattern(pt)
        tmp.curInx = self.curInx
        tmp.extra = self.extra
        return tmp

    def length(self):
        sum = 0
        for p in self.pat:
            sum += p.length()
        return sum

    def set_freq(self, freq):
        for p in self.pat:
            p.set_freq(freq)

class Set(SCModule):
    """ Module for selecting random modules from a set.

        Each time Set is reset (or initialized), a random module is selected,
        and it will be played the next time through.

        Note: If the modules in the Set have differing lengths, Set.length()
        will yield unpredictable results. Generally, this is not a problem,
        but it may cause some unexpected behavior (i.e., the progress bar
        might exceed 100%).
    """

    def __init__(self, set=[Val(0)]):
        self.set = set
        self.curMod = random.choice(self.set)

    def step(self, delta, const=-1):
        self.curMod.step(delta, const)

    def read(self,tails=False,stereo=True,signal=True):
        if(tails):
            if(stereo):
                sum = [0,0]
                for mdl in self.set:
                    if(mdl != self.curMod and getattr(mdl, "no_tails", None) == None):
                        val = mdl.read(tails,stereo,signal)
                        sum[0] += val[0]
                        sum[1] += val[1]
                    elif(mdl == self.curMod):
                        val = mdl.read(tails,stereo,signal)
                        sum[0] += val[0]
                        sum[1] += val[1]
                return sum
            else:
                sum = 0
                for mdl in self.set:
                    if(mdl != self.curMod and getattr(mdl, "no_tails", None) == None):
                        sum += mdl.read(tails,stereo,signal)
                    elif(mdl == self.curMod):
                        sum += mdl.read(tails,stereo,signal)
                return sum
        else:
            return self.curMod.read(tails,stereo,signal)

    def step_tails(self, delta, const=-1):
        for mdl in self.set:
            mdl.step_tails(delta, const)

    def reset(self):
        self.curMod.reset()
        self.curMod = random.choice(self.set)

    def clear(self):
        for m in self.set:
            m.clear()
        self.curMod = random.choice(self.set)

    def done(self):
        return self.curMod.done()

    def get_extra(self):
        return self.curMod.get_extra()

    def clone(self):
        st = []
        for s in self.set:
            st.append(s.clone())
        tmp = Set(st)
        tmp.curMod = tmp.set[self.set.index(self.curMod)]
        return tmp

    def length(self):
        return self.curMod.length()

    def set_freq(self, freq):
        for m in self.set:
            m.set_freq(freq)

class Series(SCModule):
    """ Module for playing a series of modules as part of a longer pattern.

        Series differs from Pattern in that Series plays modules one at a time--
        when the current module is finished, Series is done(), and SC moves on.
        Each time Series is reset, it moves on to the next module in the
        sequence.

        Note: clear() will fully reset Series, setting the first module to
        current. Also, different clones of Series operate independently, which
        means that Series might not work as planned in some situations.
        Generally, if you have to reference the module containing Series multiple
        times in the SC code, it won't work properly. Try rephrasing it to use
        Repeat instead, if possible.
    """
    def __init__(self, srs=[Val(0)]):
        self.srs = srs
        self.curInx = 0

    def step(self, delta, const=-1):
        self.srs[self.curInx].step(delta, const)

    def read(self,tails=False,stereo=True,signal=True):
        if(tails):
            if(stereo):
                cur = self.srs[self.curInx]
                sum = [0,0]
                for mdl in self.srs:
                    if(mdl != cur and getattr(mdl, "no_tails", None) == None):
                        val = mdl.read(tails,stereo,signal)
                        sum[0] += val[0]
                        sum[1] += val[1]
                    elif(mdl == cur):
                        val = mdl.read(tails,stereo,signal)
                        sum[0] += val[0]
                        sum[1] += val[1]
                return sum
            else:
                cur = self.srs[self.curInx]
                sum = 0
                for mdl in self.srs:
                    if(mdl != cur and getattr(mdl, "no_tails", None) == None):
                        sum += mdl.read(tails,stereo,signal)
                    elif(mdl == cur):
                        sum += mdl.read(tails,stereo,signal)
                return sum
        else:
            if(self.srs[self.curInx].done()):
                # This section probably should never happen -- should we just return 0?
                extra = self.srs[self.curInx].get_extra()
                self.srs[self.curInx].reset()
                self.srs[self.curInx].step(extra,ADJUST)
            return self.srs[self.curInx].read(tails,stereo,signal)

    def step_tails(self, delta, const=-1):
        for mdl in self.srs:
            mdl.step_tails(delta, const)

    def reset(self):
        self.srs[self.curInx].reset()
        self.curInx += 1
        if(self.curInx >= len(self.srs)):
            self.curInx = 0

    def clear(self):
        self.curInx = 0
        for m in self.srs:
            m.clear()

    def done(self):
        return self.srs[self.curInx].done()

    def get_extra(self):
        return self.srs[self.curInx].get_extra()

    def clone(self):
        sr = []
        for s in self.srs:
            sr.append(s.clone())
        tmp = Series(sr)
        tmp.curInx = self.curInx
        return tmp

    def length(self):
        return self.srs[self.curInx].length()

    def set_freq(self, freq):
        for s in self.srs:
            s.set_freq(freq)

class Invert(SCModule):
    """ Module for negation.

        Multiplies all output by -1.
    """

    def __init__(self, mdl):
        """ Initializer.

            Arguments:
            mdl -- The module to negate.
        """

        self.mdl = mdl

    def step(self, delta, const=-1):
        self.mdl.step(delta, const)

    def read(self,tails=False,stereo=True,signal=True):
        val = self.mdl.read(tails,stereo,signal)
        if(stereo):
            return [-val[0],-val[1]]
        else:
            return -val

    def step_tails(self, delta, const=-1):
        self.mdl.step_tails(delta, const)

    def reset(self):
        self.mdl.reset()

    def clear(self):
        self.mdl.clear()

    def done(self):
        return self.mdl.done()

    def get_extra(self):
        return self.mdl.get_extra()

    def clone(self):
        return Invert(self.mdl.clone())

    def length(self):
        return self.mdl.length()

    def set_freq(self, freq):
        self.mdl.set_freq(freq)

class Level(SCModule):
    """ Module for setting the volume of a module.

        This uses signal values, so 9 is max volume; 0 is silence. Negative
        level values will similarly invert the output.
    """

    def __init__(self, mdl, env, alead=True):
        """ Initializer.

            Arguments:
            mdl -- The input module.
            env -- The volume level module.
            alead -- If true, we stop when mdl stops; otherwise, when env stops.
        """

        self.a = mdl
        self.b = env
        self.a_lead = alead

    def step(self, delta, const=-1):
        self.a.step(delta, const)
        self.b.step(delta, const)
        if(self.a_lead):
            if(self.b.done() and not self.a.done()):
                extra = self.b.get_extra()
                self.b.reset()
                self.b.step(extra,ADJUST)
        else:
            if(self.a.done() and not self.b.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        valA = self.a.read(tails,stereo,signal)
        valB = self.b.read(tails,stereo,True)
        if(stereo):
            return [valA[0]*as_decimal(valB[0]),valA[1]*as_decimal(valB[1])]
        else:
            return valA*as_decimal(valB)

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)
        self.b.step_tails(delta,const)

    def reset(self):
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.a.clear()
        self.b.clear()

    def done(self):
        if(self.a_lead):
            return self.a.done()
        else:
            return self.b.done()

    def get_extra(self):
        if(self.a_lead):
            return self.a.get_extra()
        else:
            return self.b.get_extra()

    def length(self):
        if(self.a_lead):
            return self.a.length()
        else:
            return self.b.length()

    def clone(self):
        return Level(self.a.clone(), self.b.clone(), self.a_lead)

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Envelope(SCModule):
    """ Volume envelope module.

        This is similar to Level, except the volume module runs in constant
        time, based on song steps. This lets you create an envelope that
        doesn't vary based on Instrument pitch.

        Like Level, this uses signal values, so 9 is max volume, 0 is silence.
        Negative values will similarly invert the output.
    """

    def __init__(self, mdl, env, rate=1, loop=False, atk=0, rels=-1):
        """ Initializer.

            Arguments:
            mdl -- The input module.
            env -- The envelope module.
            rate -- Playback rate for the envelope module. 1 is in time with
                    song steps; 2 is twice as fast; 0.5 half, etc.
            loop -- Whether to loop when the volume module is finished.
            atk  -- The attack marker, used when looping.
            rels -- The release point, in song steps. Will loop up to this
                    point until STOP, then will play through. -1 for no release.
        """

        self.a = mdl
        self.b = env
        # so you don't have to spend an hour searching in the future --
        # the reason Const does rate/frameslice & Envelope does just rate
        # is that we actually are setting the rate in the parser
        # (don't ask me why though)
        self.rate = rate
        self.loop = loop
        self.attack = atk
        self.release = rels
        self.cur = 0
        self.stopped = False

    def step(self, delta, const=-1):
        if(const == STOP or const == RELEASE):
            self.a.step(0,const)
            self.b.step(0,const)
            self.stopped = True
        elif(const == ADJUST):
            self.cur += delta
            self.b.step(delta, const)
        else:
            if(const == DELTA):
                const = delta
            self.a.step(delta, const)
            self.b.step(const*self.rate, const)

            self.cur += const*self.rate
            # If a release point is set, we will loop at it until STOP, then play through
            if(self.release > 0):
                if(not self.stopped and self.cur >= self.release):
                    self.cur %= self.release
                    self.cur += self.attack
                    self.b.reset()
                    self.b.step(self.cur,ADJUST)

            if(self.a.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)
            if(self.loop and self.b.done()):
                extra = self.b.get_extra()
                extra += self.attack
                self.b.reset()
                self.b.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        if(stereo):
            valA = self.a.read(tails,stereo,signal)
            valB = self.b.read(tails,stereo,True)
            return [valA[0]*as_decimal(valB[0]),valA[1]*as_decimal(valB[1])]
        else:
            return self.a.read(tails,stereo,signal)*as_decimal(self.b.read(tails,stereo,True))

    def step_tails(self, delta, const=-1):
        if(const == DELTA):
            const = delta
        self.a.step_tails(delta,const)
        self.b.step_tails(const*self.rate, const)

    def reset(self):
        if(self.loop):
            self.a.reset()
            self.b.reset()
            self.b.step(self.attack,ADJUST)
            self.cur = self.attack

    def clear(self):
        self.a.clear()
        self.b.clear()
        self.cur = 0
        self.stopped = False

    def done(self):
        return self.b.done()

    def get_extra(self):
        return self.b.get_extra()#/self.rate

    def length(self):
        return self.b.length()/self.rate

    def clone(self):
        tmp = Envelope(self.a.clone(), self.b.clone(), self.rate, self.loop, self.attack, self.release)
        tmp.stopped = self.stopped
        tmp.cur = self.cur
        return tmp

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Const(SCModule):
    """ Plays a module in constant time, based on song steps.

    """

    def __init__(self, mdl, frameslice, rate=1, loop=True):
        """ Initializer.

            Arguments:
            mdl -- Input module.
            frameslice -- Ratio between song steps and samples (I think...
                    anyway, this should be SynthCorona.frameslice)
            rate -- Playback rate. 1 is in time with song steps; 2 is twice as
                    fast; 0.5 half, etc.
            loop -- Whether to loop the module once it's finished.
        """

        self.mdl = mdl
        self.rate = rate*frameslice
        self.frameslice = frameslice
        self.loop = loop

    def step(self, delta, const=-1):
        if(const == STOP or const == RELEASE):
            self.mdl.step(0,const)
        elif(const == ADJUST):
            self.mdl.step(delta, ADJUST)
        else:
            if(const == DELTA):
                const = delta
            self.mdl.step(const*self.rate,const)

    def read(self,tails=False,stereo=True,signal=True):
        return self.mdl.read(tails,stereo,signal)

    def step_tails(self, delta, const=DELTA):
        if(const == DELTA):
            const = delta
        self.mdl.step_tails(const*self.rate,const)

    def reset(self):
        if(self.loop):
            self.mdl.reset()

    def clear(self):
        self.mdl.clear()

    def done(self):
        return self.mdl.done()

    def get_extra(self):
        return self.mdl.get_extra()#/self.rate

    def length(self):
        return self.mdl.length()/self.rate

    def clone(self):
        tmp = Const(self.mdl.clone(), 1, 1, self.loop)
        tmp.rate = self.rate
        return tmp

    def set_freq(self, freq):
        self.mdl.set_freq(freq)

class Speed(SCModule):
    """ Module for changing playback rate.

        This module modifies both delta and const in step(), so it DOES affect
        pitch when applied to Inst. However, I have done some witchcraft so if
        you apply Speed to a Sequence module, it will not be passed down to
        Insts, so pitch will not be affected.
    """

    def __init__(self, mdl, rate=Val(1), alead=True):
        """ Initializer.

            Arguments:
            mdl -- Input module.
            rate -- Playback rate module.
            alead -- If true, we stop when mdl stops; otherwise, when rate stops.
        """

        self.mdl = mdl
        self.rate = rate
        self.a_lead = alead

    def step(self, delta, const=-1):
        if(const >= 0):
            self.mdl.step(delta*self.rate.read(stereo=False,signal=False),const*self.rate.read(stereo=False,signal=False))
        elif(const == DELTA):
            self.mdl.step(delta*self.rate.read(stereo=False,signal=False),delta*self.rate.read(stereo=False,signal=False))
        elif(const == STOP or const == RELEASE):
            self.mdl.step(0,const)
        elif(const == ADJUST):
            self.mdl.step(delta, const)
        self.rate.step(delta,const)
        if(self.a_lead):
            if(self.rate.done()):
                extra = self.rate.get_extra()
                self.rate.reset()
                self.rate.step(extra, ADJUST)
        else:
            if(self.mdl.done()):
                extra = self.mdl.get_extra()
                self.mdl.reset()
                self.mdl.step(extra, ADJUST)

    def read(self, tails=False,stereo=True,signal=True):
        return self.mdl.read(tails,stereo,signal)

    def step_tails(self, delta, const=-1):
        if(const < 0):
            const = delta
        self.mdl.step_tails(delta*self.rate.read(stereo=False,signal=False),const*self.rate.read(stereo=False,signal=False))

    def reset(self):
        self.mdl.reset()
        self.rate.reset()

    def clear(self):
        self.mdl.clear()
        self.rate.clear()

    def done(self):
        if(self.a_lead):
            return self.mdl.done()
        else:
            return self.rate.done()

    def get_extra(self):
        if(self.a_lead):
            return self.mdl.get_extra()
        else:
            return self.rate.get_extra()

    def length(self):
        if(self.a_lead):
            rt = self.rate.read(stereo=False,signal=False)
            if(rt == 0):
                rt = 0.0000000001
            return self.mdl.length()/rt
        else:
            return self.rate.length()

    def clone(self):
        return Speed(self.mdl.clone(), self.rate.clone(), self.a_lead)

    def set_freq(self, freq):
        self.mdl.set_freq(freq)
        self.rate.set_freq(freq)

class LinInterp(SCModule):
    """ Module for linear interpolation between two modules.

        Both modules are updated for the duration. Their outputs are blended
        based on how far we are through the LinInterp width.
    """

    def __init__(self, a, b, wid=1):
        """ Initializer.

            Arguments:
            a -- The start module.
            b -- The end module.
            wid -- Interpolation width (length).
        """

        self.a = a
        self.b = b
        self.width = wid
        self.cur = 0
        self.no_tails = True

    def step(self, delta, const=-1):
        if(const != STOP and const != RELEASE):
            self.cur += delta
        self.a.step(delta,const)
        if(self.a.done() and not self.done()):
            extra = self.a.get_extra()
            self.a.reset()
            self.a.step(extra,ADJUST)
        self.b.step(delta,const)
        if(self.b.done() and not self.done()):
            extra = self.b.get_extra()
            self.b.reset()
            self.b.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        pct = self.cur / self.width
        valA = self.a.read(tails,stereo,signal)
        valB = self.b.read(tails,stereo,signal)
        if(stereo):
            return [valA[0]*(1-pct)+valB[0]*pct,valA[1]*(1-pct)+valB[1]*pct]
        else:
            return valA*(1-pct)+valB*pct

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta, const)
        self.b.step_tails(delta, const)

    def reset(self):
        self.cur = 0
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.cur = 0
        self.a.clear()
        self.b.clear()

    def done(self):
        return self.cur >= self.width

    def get_extra(self):
        if(self.done()):
            return self.cur-self.width
        else:
            return 0

    def clone(self):
        tmp = LinInterp(self.a.clone(), self.b.clone(), self.width)
        tmp.cur = self.cur
        return tmp

    def length(self):
        return self.width

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Multiply(SCModule):
    """ Module that multiplies two inputs together.
    """

    def __init__(self, a, b, alead=True):
        """ Initializer.

            Arguments:
            a -- Input A
            b -- Input B
            alead -- If true, we stop when A stops; otherwise when B stops.
        """

        self.a = a
        self.b = b
        self.a_lead = alead

    def step(self, delta, const=-1):
        self.a.step(delta, const)
        self.b.step(delta, const)
        if(self.a_lead):
            if(self.b.done() and not self.a.done()):
                extra = self.b.get_extra()
                self.b.reset()
                self.b.step(extra,ADJUST)
        else:
            if(self.a.done() and not self.b.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        valA = self.a.read(tails,stereo,signal)
        valB = self.b.read(tails,stereo,False)
        if(stereo):
            return [valA[0]*valB[0],valA[1]*valB[1]]
        else:
            return valA * valB

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)
        self.b.step_tails(delta,const)

    def reset(self):
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.a.clear()
        self.b.clear()

    def done(self):
        if(self.a_lead):
            return self.a.done()
        else:
            return self.b.done()

    def get_extra(self):
        if(self.a_lead):
            return self.a.get_extra()
        else:
            return self.b.get_extra()

    def clone(self):
        return Multiply(self.a.clone(), self.b.clone(), self.a_lead)

    def length(self):
        if(self.a_lead):
            return self.a.length()
        else:
            return self.b.length()

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Divide(SCModule):
    """ Module that divides two inputs.
    """

    def __init__(self, a, b, alead=True):
        """ Initializer.

            Arguments:
            a -- Input A.
            b -- Input B.
            alead -- If true, we stop when A stops; otherwise, when B stops.
        """
        self.a = a
        self.b = b
        self.a_lead = alead

    def step(self, delta, const=-1):
        self.a.step(delta, const)
        self.b.step(delta, const)
        if(self.a_lead):
            if(self.b.done() and not self.a.done()):
                extra = self.b.get_extra()
                self.b.reset()
                self.b.step(extra,ADJUST)
        else:
            if(self.a.done() and not self.b.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        valA = self.a.read(tails,stereo,signal)
        valB = self.b.read(tails,stereo,False)
        if(stereo):
            return [valA[0]/valB[0],valA[1]/valB[1]]
        else:
            return valA/valB

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)
        self.b.step_tails(delta,const)

    def reset(self):
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.a.clear()
        self.b.clear()

    def done(self):
        if(self.a_lead):
            return self.a.done()
        else:
            return self.b.done()

    def get_extra(self):
        if(self.a_lead):
            return self.a.get_extra()
        else:
            return self.b.get_extra()

    def clone(self):
        return Divide(self.a.clone(), self.b.clone(), self.a_lead)

    def length(self):
        return lcm(self.a.length(), self.b.length())

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Add(SCModule):
    """ Module that adds two inputs.
    """

    def __init__(self, a, b, alead=True):
        """ Initializer.

            Arguments:
            a -- Input A.
            b -- Input B.
            alead -- If true, we stop when A stops; otherwise, when B stops.
        """

        self.a = a
        self.b = b
        self.a_lead = alead

    def step(self, delta, const=-1):
        self.a.step(delta, const)
        self.b.step(delta, const)
        if(self.a_lead):
            if(self.b.done() and not self.a.done()):
                extra = self.b.get_extra()
                self.b.reset()
                self.b.step(extra,ADJUST)
        else:
            if(self.a.done() and not self.b.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        valA = self.a.read(tails,stereo,signal)
        valB = self.b.read(tails,stereo,signal)
        if(stereo):
            return [valA[0]+valB[0],valA[1]+valB[1]]
        else:
            return valA+valB

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)
        self.b.step_tails(delta,const)

    def reset(self):
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.a.clear()
        self.b.clear()

    def done(self):
        if(self.a_lead):
            return self.a.done()
        else:
            return self.b.done()

    def get_extra(self):
        if(self.a_lead):
            return self.a.get_extra()
        else:
            return self.b.get_extra()

    def clone(self):
        return Add(self.a.clone(), self.b.clone(), self.a_lead)

    def length(self):
        if(self.a_lead):
            return self.a.length()
        else:
            return self.b.length()

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Subtract(SCModule):
    """ Module that subtracts two inputs.
    """

    def __init__(self, a, b, alead=True):
        """ Initializer.

            Arguments:
            a -- Input A.
            b -- Input B.
            alead -- If true, we stop when A stops; otherwise, when B stops.
        """

        self.a = a
        self.b = b
        self.a_lead = alead

    def step(self, delta, const=-1):
        self.a.step(delta, const)
        self.b.step(delta, const)
        if(self.a_lead):
            if(self.b.done() and not self.a.done()):
                extra = self.b.get_extra()
                self.b.reset()
                self.b.step(extra,ADJUST)
        else:
            if(self.a.done() and not self.b.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)

    def read(self,tails=False,stereo=True,signal=True):
        valA = self.a.read(tails,stereo,signal)
        valB = self.b.read(tails,stereo,signal)
        if(stereo):
            return [valA[0]-valB[0],valA[1]-valB[1]]
        else:
            return valA-valB

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)
        self.b.step_tails(delta,const)

    def reset(self):
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.a.clear()
        self.b.clear()

    def done(self):
        if(self.a_lead):
            return self.a.done()
        else:
            return self.b.done()

    def get_extra(self):
        if(self.a_lead):
            return self.a.get_extra()
        else:
            return self.b.get_extra()

    def clone(self):
        return Subtract(self.a.clone(), self.b.clone(), self.a_lead)

    def length(self):
        if(self.a_lead):
            return self.a.length()
        else:
            return self.b.length()

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Repeat(SCModule):
    """ Module that loops an input a given number of times.
    """

    def __init__(self, mdl, x):
        """ Initializer.

            Arguments:
            mdl -- Input module.
            x -- The number of times to repeat.
        """

        self.a = mdl
        self.b = x
        self.resets = 1

    def step(self, delta, const=-1):
        self.a.step(delta, const)
        reps = self.b.read(stereo=False,signal=False)
        if(self.a.done() and (reps < 0 or self.resets < reps)):
            extra = self.a.get_extra()
            self.a.reset()
            self.a.step(extra,ADJUST)
            self.resets += 1

    def read(self,tails=False,stereo=True,signal=True):
        return self.a.read(tails,stereo,signal)

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)

    def reset(self):
        self.a.reset()
        self.resets = 1

    def clear(self):
        self.a.clear()
        self.resets = 1

    def done(self):
        return self.a.done()

    def get_extra(self):
        return self.a.get_extra()

    def clone(self):
        tmp = Repeat(self.a.clone(), self.b.clone())
        tmp.resets = self.resets
        return tmp

    def length(self):
        if(self.b.read(stereo=False,signal=False)<0):
            return 9999999999999
        else:
            return self.a.length()*self.b.read(stereo=False,signal=False)

    def set_freq(self, freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

class Cross(SCModule):
    """ Module for "crossing" a binary operation.

        Normal binary operators run both operand modules (A and B)
        simultaneously. Cross operations slow down the B module so that A
        completes a full cycle for each step of B. In a sense, we compute
        "all of A for each of B".

        Here's an example:
        Consider [1,2,3,4]*[1,0] --
        Regularly, our output is [1*1,2*0,3*1,4*0] = [1,0,3,0]
        If we take the cross of this, [1,2,3,4]x*[1,0] --
        We get [1*1,2*1,3*1,4*1,1*0,2*0,3*0,4*0] = [1,2,3,4, 0,0,0,0]
    """

    def __init__(self, mdl):
        """ Initializer.

            Arguments:
            mdl -- Input module. Must be a binary operation.
        """
        if(hasattr(mdl, "a") and hasattr(mdl, "b")):
            self.op = mdl
        else:
            raise SCParseError("Invalid Operator for Cross module.",line)
            self.op = mdl
        self.acount = 1
        self.bstep = -1
        self.cur = 0
        self.len = self.op.a.length()*self.op.b.length()

    def step(self, delta, const=-1):
        if(self.bstep < 0):
            self.bstep = 1/(self.op.a.length())
            self.len = self.op.a.length() * self.op.b.length()
        self.op.a.step(delta,const)
        self.acount -= delta*self.bstep
        if(self.op.a.done() or self.acount > 0):
            self.op.b.step(delta*self.bstep,const)
            if(self.op.a.done() and not self.done()):
                extra = self.op.a.get_extra()
                self.op.a.reset()
                self.op.a.step(extra,ADJUST)
                self.bstep = 1/self.op.a.length()
                self.len = self.op.a.length()*self.op.b.length()
                self.acount = 1
        else:
            extra = -self.acount * self.op.a.length()
            self.op.b.step(delta*self.bstep,const)
            self.op.a.reset()
            self.op.a.step(extra,ADJUST)
            self.bstep = 1/self.op.a.length()
            self.len = self.op.a.length() * self.op.b.length()
            self.acount += 1
        self.cur += delta

    def read(self,tails=False,stereo=True,signal=True):
        return self.op.read(tails,stereo,signal)

    def step_tails(self, delta, const=-1):
        self.op.a.step_tails(delta,const)
        self.op.b.step_tails(delta*self.bstep,const)

    def reset(self):
        self.op.reset()
        self.cur = 0
        self.acount = 1
        self.bstep = 1/(self.op.a.length())
        self.len = self.op.a.length()*self.op.b.length()

    def clear(self):
        self.op.clear()
        self.cur = 0
        self.acount = 1
        self.bstep = 1/self.op.a.length()
        self.len = self.op.a.length()*self.op.b.length()

    def done(self):
        return self.cur >= self.len

    def get_extra(self):
        if(self.done()):
            return self.cur-self.len
        else:
            return 0

    def clone(self):
        tmp = Cross(self.op.clone())
        tmp.bstep = self.bstep
        tmp.cur = self.cur
        tmp.acount = self.acount
        tmp.len = self.len
        return tmp

    def length(self):
        return self.op.a.length()*self.op.b.length()

    def set_freq(self, freq):
        self.op.set_freq(freq)

class Length(SCModule):
    """ Overrides the length of a given module. This will:
        - Repeat the module if it stops before length is met.
        - Halt the module early if the length is met before it ends
          (may cause pops!)

        This module takes two inputs, A and B, where A is the signal module
        and B determines the length.
    """

    def __init__(self, a, b):
        """ Initializer.

            Arguments:
            A - The signal module, to be length-overridden.
            B - The length.
        """

        self.a = a
        self.b = b
        self.cur = 0

    def step(self, delta, const=-1):
        self.cur += delta
        self.a.step(delta,const)
        self.b.step(delta,const)

        if(not self.done()):
            if(self.a.done()):
                extra = self.a.get_extra()
                self.a.reset()
                self.a.step(extra,ADJUST)
            if(self.b.done()):
                extra = self.b.get_extra()
                self.b.reset()
                self.b.step(extra,ADJUST)

    def step_tails(self, delta, const=-1):
        self.a.step_tails(delta,const)
        self.b.step_tails(delta,const)

    def read(self, tails=False,stereo=True,signal=True):
        return self.a.read(tails,stereo,signal)

    def reset(self):
        self.cur = 0
        self.a.reset()
        self.b.reset()

    def clear(self):
        self.cur = 0
        self.a.reset()
        self.b.reset()

    def done(self):
        return self.cur >= self.b.read(stereo=False)

    def get_extra(self):
        if(self.done()):
            return self.cur - self.b.read(stereo=False)
        else:
            return 0

    def length(self):
        return self.b.read(stereo=False)

    def set_freq(self,freq):
        self.a.set_freq(freq)
        self.b.set_freq(freq)

    def clone(self):
        tmp = Length(self.a.clone(),self.b.clone())
        tmp.cur = self.cur
        return tmp


def gcd(a, b):
    """ Calculates greatest common denominator.

        Arguments:
        a -- Input A.
        b -- Inpubt B.
    """
    while(b > 0):
        a, b = b, a % b
    return a

def lcm(a, b):
    """ Calculates least common multiple.

        Arguments:
        a -- Input A.
        b -- Input B.
    """

    return a*b/gcd(a,b)

def as_decimal(val):
    """ Converts SC signal values into decimals.

        Signal values range from -9 to 9, so this simply returns the input
        divided by 9.

        Arguments:
        val -- The value to convert to decimal.
    """

    dec = val/MAX_VAL
    return dec

def limit(val):
    """ Hard limits the given signal value.

        This limits to +/-0.9999 * MAX.

        Arguments:
        val -- The signal value to limit.
    """

    if(val >= MAX_VAL):
        return MAX_VAL * 0.9999
    elif(val <= -MAX_VAL):
        return -MAX_VAL * 0.9999
    else:
        return val

def calc_freq(disp):
    """ Calculates the frequency of a given pitch.

        This calculation is performed in cents, and uses A4 for reference. As
        such, input must be expressed in terms of distance to A4--so:
            0 = A4
            300 = C5
            -1200 = A3
            etc.

        Currently, we pre-bake all frequencies when SynthCorona starts up, so
        this is only used initially--afterward, we pull frequencies from a list.

        Arguments:
        disp -- The pitch, expressed as "cents from A4".
    """
    return 440.0 * (2**(1/1200.0))**disp

def pan(vals, pan):
    """ Calculates panning.

        Pan amounts range from -9 (100% L) to 9 (100% R). Excessive values
        will be clipped.

        Arguments:
        vals -- The stereo pair of signal values.
        pan -- The panning adjustment.
    """
    # pan values should range from -9 (100% L) to 9 (100% R)
    pan /= 9
    # clips pan to a max of 100% in either direction
    if(abs(pan)>1):
        pan = pan/abs(pan)
    if(pan == 0):
        return vals
    elif(pan < 0):
        lpan = abs(pan)
        rtol = vals[1]*lpan
        #print("PAN=" + str(pan) + "|rtol: " + str(rtol))
        return [vals[0]+rtol,vals[1]-rtol]
    else:
        ltor = vals[0]*pan
        #print("PAN=" + str(pan) + "|ltor: " + str(ltor))
        return [vals[0]-ltor,vals[1]+ltor]
