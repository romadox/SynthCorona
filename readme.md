<h1>Synth-Corona</h1>
<h2>I. What is it?</h2>

Synth-Corona is a code language for creating chiptunes from scratch in your favorite
mono-space text editor. It features a highly modular design, allowing a wide range 
of control over sounds, pitch, panning, sequences, and song structure.

The renderer script parses Synth-Corona code into a WAV audio file.

<h2>II. Get Started</h2>

The renderer is built in Python3, so you'll need that to run it. You can use <a href="https://www.python.org/download/releases/3.0/">standard 
Python</a>, but I recommend <a href="https://pypy.org/">pypy3</a> instead. Synth-Corona 
is very CPU demanding, and pypy tends to run SC about 10x as fast as regular Python.
      
To get Synth-Corona, download <b>SynthCorona.py</b> and <b>sc.py</b>. SynthCorona.py is the 
nuts-and-bolts, and sc.py is the runnable renderer. They'll need to be in the same folder.

To run it, use: <code>python3 /your/filepath/sc.py</code> for regular Python.

Or: <code>pypy3 /your/filepath/sc.py</code> for PyPy.

This will prompt you for the Synth-Corona file you would like to render. If you like,
you can also send your SC file from the command line:
      <code>python3 /your/filepath/sc.py /your/sc/filepath/song.sc</code>
      
To test out your setup and get a quick feel for what Synth-Corona code looks like,
download <b>demo1.sc</b>, or one of the other demo files, and give it a go! The rest of this
guide goes over writing Synth-Corona code, so I highly recommend browsing over some of
the samples first.

<h2>III. Headers & Chunks</h2>

Synth-Corona files are made up of Config, Module, Instrument, Sequence, and Song
chunks, each indicated by a header line. A Song is made up of Sequences, and
Sequences indicate which Instrument will play which note at a given time. Sequences
can also be grouped into Blocks, for more complex arrangements.

The Config chunk describes properties like tempo and beat length.

The Instrument chunk describes the synthesizers that will play the sound. Unlike 
most synthesizers, which give you a waveform and let you manipulate it, Synth-Corona
instruments are built from scratch using various modules to form the wave.

In the Module chunk, generic modules can be created, which can then be used in 
Instruments and Sequences, or for controlling pitch or panning.

Each chunk begins with a header. They are as follows:
<ul>
<li>CFG : Configuration (this must come before Instrument, Sequence, and Song chunks!)</li>
<li>INS : Instrument</li>
<li>MDL : Generic Module</li>
<li>SEQ : Sequence (each header describes one Sequence)</li>
<li>BLK/PAT: Sequence Block (for creating song patterns out of Sequences)</li>
<li>SNG : Song Chunk</li>
<li>IMP : Import (all on one line).</li>
</ul>

<h2>IV. Naming</h2>

As you create Instruments and Sequences, you'll give them names so you can
refer to them elsewhere. Instruments that will be used in a Sequence must 
be named with a single character (for alignment). Other modules/Instruments 
can have longer names.

You cannot use any of the reserved characters, which indicate operations. For
best practice, do not use lowercase characters in names, as lowercase is for
operators.

You can use the same name for an Instrument and a Sequence, but obviously
not the same name for two of the same kind.

Here are the current reserved characters: <code>+-*/%rixlvcstnjk{}[]()\<>.,|</code>

<h2>V. Operators</h2>

Operators let you perform various pattern and mathematical functions in
creating your song.

      SYMBOL |   Operator    |   DESCRIPTION                    |   USAGE
             |               |                                  |
        []   |   Pattern     | Plays items in sequence          |  [0,1,2,1]
        ()   |   Series      | Plays items individually in order|  (0,1,2,3)
        {}   |   Set         | Plays a random item from the set |  {0,1,2,3}
        +    |   Add         | Adds two items together          |     A+2
        -    |   Subtract    | Subtracts two items              |     C-A
        *    |   Multiply    | Multiply two items together      |     3*B
        /    |   Divide      | Divides an item by another       |     B/2
        %    |   Modulus     | Remainder after dividing values  |     A%B 
        l    |   Level       | Uses B as a level (0-9) for A    |     AlB
        v    |   Envelope    | Like level, at a constant speed  |     AvB
        i    |   Interpolate | Lin. Interp. A to B, over W steps|     AiB
        r    |   Repeat      | Repeats an item X times          |     ArX
        x    |   Cross       | Uses each A item with each B item|     Ax*B
        -    |   Invert      | Inverts an item                  |     -4
        c    |   Constant    | Run A with Song Steps, not freq  |     cA
        s    |   Speed       | Run A at Bx speed (as a ratio)   |     AsB
        n    |   Length      | Set the duration of A to B.      |     AnB
        t    |   Absolute Val| Returns absolute value of A.     |     tA
        k    |   Attack Pt.  | Set looping Attack point         |     AkB
        j    |   Release Pt. | Set looping Release point        |     AjB

<h3>Notes:</h3>

<ul>
<li>Add, Subtract, Multiply, Divide, Modulus, and Level all perform operations
on two different Modules, "A" and "B". Since these can have different
lengths, one Module is assigned the "lead", meaning we will stop
once it is finished, and we will reset the other module if we have
to. By default, Module "A" (the first Module you list) is the lead.
However, there are times when you might need to use the length from
"B", so this is an option via a meta-tag:
<code>A/\<lead=B>B</code>
This example creates a Division operation that will use the length of "B" as
its lead.
</li>
<li>Typically Interpolate has a width of 1, meaning it does its full
gradient in one step. You can change this width using a
meta-tag: <code>Ai\<w=4>B</code>
In this instance, we are saying that we want to interpolate A to B
but we want to do it over 4 steps ("\<w=4>").
</li>
<li>The level operation is like volume--each item in B is converted
into a percentage (-1 to 1), which is then multiplied by the value
in A. This is equivalent to <code>A*(B/9)</code>, since we use 9 as a maximum value.
</li>
<li>Envelope is similar to a combination of Level and Constant. Time
is processed based on song steps for module B, so the envelope
will be the same length regardless of the pitch the instrument is
playing.

There are four properties you can set with envelopes:
      <ul>
            <li>
                  <b>RATE</b> ("R") controls how fast the envelope plays, in song-steps.
                  For instance:
                        <code>Av\<r=2>[0,1,2,3]</code>
                  This sets the rate to 2 (<code>\<r=2></code>), which means we will take two
                  envelope steps per song step. The instrument we are enveloping
                  is <code>A</code>, and the volume levels are <code>[0,1,2,3]</code>.
            </li>
            <li>
                  <b>LOOP</b> ("L") tells the envelope whether to repeat after it is finished.
                  <code>Av\<l=T>[3,4,5]</code>
                  In this example, we have set loop to True (<code>\<l=T></code>), so we will
                  cycle through the volumes, creating a jagged tremolo effect.
                        <code>Av\<l=F>[3,4,5,4,2,0]</code>
                  In this example, we will not loop the envelope, so we will raise
                  the volume to 5, then down to 0, and that is when the instrument
                  will stop.
                  It's a good idea to end these envelopes with a 0, to reduce pops.
                  By default, LOOP is set to "True".
            </li>
            <li>
                  <b>ATTACK</b> ("ATK") sets the envelope attack point. When the envelope loops, it will
                  start back at this point, so any fade-in section is not also repeated.
                  By default this is set to 0, which is the same as having no attack period.
            </li>
            <li>
                  <b>RELEASE</b> ("REL") sets the envelope release point. Anything after the release
                  point will only be played if the note has been released. While the note is 
                  sustaining, the envelope will loop back from RELEASE to ATTACK (or the 
                  beginning, if no ATTACK is set). By default, RELEASE is set to -1, which 
                  indicates that the envelope has no release point.
            </li>
      </ul>
</li>
<li>
The Constant operation allows you to make other modules behave like the
Envelope module, where time is based in song-steps. Constant also has
both the RATE, LOOP, ATTACK, and RELEASE options, which work just like they do in
Envelope.

One thing to take note of with Constant-time modules is that they do
not always play nicely with flexible-time modules. For instance,
if we do:
      <code>[0,1,2,3]+c[2,3,4,5]</code>
The first pattern is going to update at a different speed than the
second, so even though they are the same lengths, they are not going
to finish at the same time.
</li>
<li>The Cross operation is to be combined with another operator
("x*" or "xl", etc.). With Cross, we will step through each item in A
before stepping to the next B. For example, see how the addition of
these two patterns is is different with and without Cross:

                     Simple Addition             Cross Addition
          Patterns: [1,2,3,4]+[0,1,2]    vs    [1,2,3,4]x+[0,1,2]
                     Step:     Result:           Step:     Result:
                     1+0         1                1+0        1
                     2+1         3                2+0        2
                     3+2         5                3+0        3
                     4+0         4                4+0        4
                     1+1         2                1+1        2
                     2+2         4                2+1        3
                     3+0         3                3+1        4
                     4+1         5                4+1        5
                     1+2         3                1+2        3
                     2+0         2                2+2        4
                     3+1         4                3+2        5
                     4+2         6                4+2        6

</li>
<li>
The Repeat module also supports ATTACK and RELEASE. These work similar to how they do in Envelope and Const, except that Repeat will also play past the Release point on its final repetition, even if the instrument has not been released yet.
</li>
</ul>
<h2>VI. Instruments</h2>

Instruments are described with a name, metadata, and a definition:

      INS
      A <prd=7>: {0,2,3,4,-4,-3,-2}

Above, <code>A</code> is the instrument name, <code>\<prd=7></code> indicates that the wave period
of this instrument is 7 steps, to the right of the colon is the definition.
This particular instance creates a Pattern, which makes something like a
blocky saw wave.

The ":" separates the name side from the definition and is required.

Instruments and their definition have to all be on one line. If you need to
do a longer formula, you can easily link one instrument into another,
provided it has been defined above:

      INS
      A: [0i4,-4i0]
      B: 2*A

The above instrument A defines a smooth saw wave. Instrument B multiplies
A by two, increasing the amplitude.

Meta-data lets you add a litle extra control to your instrument. Here
are the current options:

          NAME        TAG(S)              DESCRIPTION

         Period       prd      Indicates how many steps in the pattern
                               represent one full cycle of the sound wave.
                               By default, it is the length of the pattern.
                               
         Panning      pan      Sets the panning for the instrument. This can 
                               be a value from -9 (100% L) to 9 (100% R), or 
                               it can be a reference to a general Module.

         Loop       l, loop    Indicates whether the Instrument should loop
                               continuously, or stop after playing through once.

         Sustain    s, sus     Indicates whether this Instrument should finish
                               playing its pattern after it is stopped.

         Base        base      Imports the above properties from another
                               instrument. For example: <base=SINE>
                               Will import properties from Instrument "SINE".
                               This is handy, for example, if you are going to
                               use SINE in the instrument, but don't know its
                               period. Any meta-tags specified after "BASE" will
                               overwrite the ones that were imported.

<h2>VII. Sequences & Sequence Blocks</h2>

<b>Sequences</b> are defined with the "SEQ" header, a name, and then a list of
lines that indicate Pitch and Pattern:

      SEQ A
      A4:  |        B B     |                |
      G4:  |    B B     B-- |                |
      F4:  |                |B B             |
      E4:  |                |    B B         |
      D4:  |                |        B B     |
      C4:  |B B             |            B-  |

The above Sequence, "A", describes the first two bars of "Twinkle Twinkle,
Little Star", to be played on Instrument "B".

Each row/line of the sequence describes a pitch; each space represents a
step; and non-space letters indicate the instrument to play at that step.

The character "|" is reserved as a barline, and is removed before the line
is parsed. As such it *does not count as a step*. Sequence lines begin with
the first "|" and end with the last one; these are the only required barlines,
and others can be placed for readability purposes or omitted.

The character "-" indicates sustain, and will continue the previously played
Instrument, without resetting it.

Before the ":" is, of course, the pitch indicator. For this, you can use any
of the following two- and three- character strings to indicate musical notes:

(in these examples, "O" indicates an octave number, 0-9)

      Two-Char: AO, bO, BO, CO, dO, DO, eO, EO, FO, gO, GO, aO
        (Here lower-case letters indicate flats.)
      Three-Char: A O, A#O, BbO, B O, C O, C#O, DbO, D O, D#O, EbO, E O, F O,
                  F#O, GbO, G O, G#O, AbO
        (Spaces between natural notes and their octaves are required)

Additionally, you can use operations on pitches, or create patterns and
randomizable sets with them. Note that all pitch values are stored and
calculated in cents, so 100=1 semitone. Here are some examples:

      A4+50:                          (A4 plus a quarter-step)
      (A 4, B 4, C#5, D 5, E 5):      (An ascending scale)
      A4+[0i50, 50i0]:                (A4 with +50 vibrato)
      {A3, D4}:                       (Either A3 or D4)

You can also reference general modules here:

      MDL
      VIB: [-25i25,25i-25]s8  // A general-purpose vibrato module
      
      SEQ A
      A4+VIB: |N---    N------  |  // A4 with vibrato
      E4+VIB: |    N---         |  // E4 with vibrato
      
<b>Sequence Blocks</b> allow you to use module operations on your Sequences 
and save them into more complex patterns. For instance:

      SEQ A
      G4: |X       X       |
      
      SEQ B
      C5: |  Y   Y   Y   Y |
      A4: |Y   Y       Y   |
      
      BLK
      C: Ar4
      D: [B,B+A]
      
In the above, we define Sequences A and B first, then create Sequence Blocks
that use them. The first block, C, repeats A four times. Block D plays B, 
then plays both B and A (<code>B+A</code>).

Like the INS and MDL chunks, Sequence Blocks are defined all on one line, and
multiple Blocks can be created under the BLK header (whereas each SEQ header 
describes a different Sequence).

<h2>VIII. The Song Chunk</h2>

The Song chunk is where you will arrange Sequences into an overall song.
Song chunks begin with the "SNG" header, then a series of Sequence names, separated by commas.
This can be on one line or multiple lines:

      SNG A, B, A, C

  is the same as

      SNG
      A,B,A,C

By default, a song will have the same name as the source code file (so "my-song.sc" renders to
"my-song.wav"). However, you can set a specific name by adding a colon like this:

      SNG my-song2: A,B,A,C
      
Here, the colon is separating the "SNG" header and the song name, "my-song2", from the arrangement
"A,B,A,C". The colon is necessary, otherwise Synth-Corona will assume you are arranging the song,
instead of naming it.

Additionally, you can render multiple songs from one Synth-Corona file by simply adding more SNG
chunks:

      SNG my-song: A,B,A,C
      SNG my-song2:
      Ar2,B,C
      SNG my-song3: B,A,C
      
(Note that if there are two unnamed Song chunks, they will both default to the source name, so the
second one will overwrite the first!)

As with Instrument patterns and Pitches, you may use operators to customize
your song:

      SNG [A, A+B, C, (C, D)]r2

The above example will play SEQ "A", both "A" and "B" together, "C", and
then "C" again, then it will repeat a second time, using "D" instead of "C".

<h2>IX - The Config Block</h2>

The configuration block lets you set up details about the overall song.
Parameters are:

      TEMPO -- Song tempo, in beats per minute. Defaults to 120.
      BEAT  -- Beat length, in song steps (each space/letter). Default: 4.
      RATE  -- Sample rate of the WAV file. Defaults to 44100.
      DEPTH -- Bit depth of the WAV file, in bits. Default is 16.
      NORMALIZE -- Whether to normalize the output.
      STEREO -- Sets the song to Stereo.
      MONO -- Sets the song to Mono.

Parameters are set with the following format:

      TEMPO: 105

<h2>X. Imports</h2>

If you have complex instruments or patterns that you want to use in
different files, you can import other files using the "IMP" header:

      IMP /wherever/your/file/is/file.txt

Importing like this will load all instruments and patters into the current
file, under their original names. Generally, putting IMP statements at the
beginning of the file is best, to prevent overwriting your other stuff.
