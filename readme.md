
      === SYNTH-CORONA ===
           User Guide

 I - What??

    Synth-Corona is a text-based music composer, sequencer, and synthesizer.
    Simply type a document in a text-editor (mono-type editors work best),
    and the Synth-Corona script (sc.py) will render it into a WAV audio file.

    Synth-Corona uses a specific parsing language to create synthesizers,
    patterns, and songs. This guide covers the specifics of the parsing
    language, but it might be a bit confusing without first seeing what
    we're talking about.

    As such, I recommend opening up "demo1.txt" right now. It is a complete
    SynthCorona music file, which plays a short tune. Look it over, then pop
    back over here to figure out what exactly is going on over there.

    Whenever you want to render a song, simply run "sc.py" from Python3,
    then enter the path/name of the file you want to render. The script will
    create a WAV file of the song.

  II - Overview

    Synth-Corona files are made up of Config, Instrument, Sequence, and Song
    blocks, each indicated by a header line. A Song is made up of Sequences, and
    Sequences indicate which Instrument will play which note at a given time.

    The Config block describes properties like tempo and beat length.

    Instrument blocks describe the synthesizers that will play the sound. This
    is done by creating a pattern of values between -9 and 9, which will be
    used as the sample intensities in the sound wave. There are a variety of
    operations that can be used in this process.

  III - Headers

    Headers indicate which block is to follow. They are as follows:
      - CFG : Configuration Block (this must come before Instrument, Sequence,
              and Song blocks!)
      - INS : Instrument Block
      - SEQ : Sequence Block (each block describes one Sequence)
      - SNG : Song Block
      - IMP : Import Block (all on one line).

  IV - Naming

    As you create Instruments and Sequences, you'll give them names so you can
    refer to them elsewhere. For both, it is best to use a single character as
    the name. Additionally, you cannot use any of the reserved characters, which
    indicate operations. As a general rule, capital letters are free to use,
    though a few lower-case letters are reserved.

    You can use the same name for an Instrument and a Sequence, but obviously
    not the same name for two of the same kind.

    Here are the current reserved characters: +-*/frixlvcs{}[]()<>1234567890.,|

  V - Operators

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
        l    |   Level       | Uses B as a level (0-9) for A    |     AlB
        v    |   Envelope    | Like level, at a constant speed  |     AvB
        i    |   Interpolate | Lin. Interp. A to B, over W steps|     AiB
        r    |   Repeat      | Repeats an item X times          |     ArX
        x    |   Cross       | Uses each A item with each B item|     Ax*B
        -    |   Invert      | Inverts an item                  |     -4
        f    |   Floor       | Update A only on whole steps     |     fA
        c    |   Constant    | Run A with Song Steps, not freq  |     cA
        s    |   Speed       | Run A at Bx speed (as a ratio)   |     AsB

    Notes:
      *  Add, Subtract, Multiply, Divide, and Level all perform operations
         on two different Modules, "A" and "B". Since these can have different
         lengths, one Module is assigned the "lead", meaning we will stop
         once it is finished, and we will reset the other module if we have
         to. By default, Module "A" (the first Module you list) is the lead.
         However, there are times when you might need to use the length from
         "B", so this is an option via a meta-tag:
            A/<lead=B>B
         This creates a Division operation that will use the length of "B" as
         its lead.

      *  Typically Interpolate has a width of 1, meaning it does its full
         gradient in one step. You can change this width using a
         meta-tag: Ai<w=4>B
         In this instance, we are saying that we want to interpolate A to B
         but we want to do it over 4 steps ("<w=4>").

      *  The level operation is like volume--each item in B is converted
         into a percentage (-1 to 1), which is this multiplied by the value
         in A. This is equivalent to A*(B/9), since we use 9 as a maximum value.

      *  Envelope is similar to a combination of Level and Constant--time
         is processed based on song steps for module B, so the envelope
         will be the same length regardless of the pitch the instrument is
         playing.

         There are two properties you can set with envelopes:
         RATE ("R") controls how fast the envelope plays, in song-steps.
         For instance:
            Av<r=2>[0,1,2,3]
         This sets the rate to 2 ("<r=2>"), which means we will take two
         envelope steps per song step. The instrument we are enveloping
         is "A", and the volume levels are "[0,1,2,3]".

         Additionally, you can set the LOOP property of an envelope, to
         tell it whether to repeat after the envelope is finished.
            Av<l=T>[3,4,5]
         In this example, we have set loop to True ("<l=T>"), so we will
         cycle through the volumes, creating a jagged tremolo effect.
            Av<l=F>[3,4,5,4,2,0]
         In this example, we will not loop the envelope, so we will raise
         the volume to 5, then down to 0, and that is when the instrument
         will stop.

         It's a good idea to end these envelopes with a 0, to reduce pops.
         By default, LOOP is set to "True".

      *  The Constant operation allows you to make other modules behave like the
         Envelope module, where time is based in song-steps. Constant also has
         both the RATE and the LOOP options, which work just like they do in
         Envelope.

         One thing to take note of with Constant-time modules is that they do
         not always play nicely with flexible-time modules. For instance,
         if we do:
            [0,1,2,3]+c[2,3,4,5]
         The first pattern is going to update at a different speed than the
         second, so even though they are the same lengths, they are not going
         to finish at the same time.

      *  The Cross operation is to be combined with another operator
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


  VI - Instruments

    Instruments are described with a name, metadata, and a definition:

      INS
      A <prd=7>: {0,2,3,4,-4,-3,-2}

    Above, "A" is the instrument name, <prd=7> indicates that the wave period
    of this instrument is 7 steps, to the right of the colon is the definition.
    This particular instance creates a Pattern, which makes something like a
    blocky saw wave.

    The ":" separates the name side from the definition, and is required.

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

  VII - Sequences

    Sequences are defined with the "SEQ" header, a name, and then a list of
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
    is parsed. As such it *does not count as a step*.

    The character "-" indicates sustain, and will continue the previously played
    Instrument, without resetting it.

    The musical pattern begins with the first non-space, non-barline character,
    and ends with the final non-barline character (including spaces). This uses
    the earliest beginning and latest end from all lines in the sequence, so
    if you have a short line, you don't need to fill it with spaces.

    If you want to start the sequence with silence, use a "-" on one of the
    lines.

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

  VIII - The Song block

    The Song block is where you will arrange Sequences into an overall song.
    Only one Song per file is permitted. Song blocks begin with the "SNG"
    header, then a series of Sequence names, separated by commas. This can be
    on one line or multiple lines:

      SNG A, B, A, C

        is the same as

      SNG
      A,B,A,C

    As with Instrument patterns and Pitches, you may use operators to customize
    your song:

      SNG [A, A+B, C, (C, D)]r2

    The above example will play SEQ "A", both "A" and "B" together, "C", and
    then "C" again, then it will repeat a second time, using "D" instead of "C".

  IX - The Config Block

    The configuration block lets you set up details about the overall song.
    Parameters are:

      "TEMPO" -- Song tempo, in beats per minute. Defaults to 120.
      "BEAT"  -- Beat length, in song steps (each space/letter). Default: 4.
      "RATE"  -- Sample rate of the WAV file. Defaults to 44100.
      "DEPTH" -- Bit depth of the WAV file, in bits. Default is 16.

    Parameters are set with the following format:

      TEMPO: 105

  X - Imports

    If you have complex instruments or patterns that you want to use in
    different files, you can import other files using the "IMP" header:

      IMP /wherever/your/file/is/file.txt

    Importing like this will load all instruments and patters into the current
    file, under their original names. Generally, putting IMP statements at the
    beginning of the file is best, to prevent overwriting your other stuff.
