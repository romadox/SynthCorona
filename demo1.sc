// Hello! This is a very simple SynthCorona file.
// Please feel free to play around with it, and see what happens!
// (Everything following a '//' is a comment and is ignored)


CFG  // Configuration Chunk

TEMPO: 120  // 120 Beats Per Minute
BEAT:  4    // Four steps per Beat--each space/letter is a step!
NORM: T     // Normalize the audio to max volume without clipping.


INS  // Instrument Chunk

// This is a pulse wave--it jumps up to 4, then down to -4, then it repeats!
// We didn't set a period, so the parser will use the length of our pattern.
A: [4,-4]

// This is a triangle wave. It uses "i" to smoothly interpolate between values.
// This time we did set the period ("<prd=4>").
B <prd=4>: [0i9,9i0,0i-9,-9i0]

SEQ A // Sequence Chunk, defining Sequence "A"
   // Our Melody, with Instrument A
G4:   |            A---|        A-      |
F4:   |          A-    |          A-    |
E4:   |        A-      |            A---|
D4:   |    A---        |    A---        |
C4:   |A---            |A---            |

   // Our Bass-Line, with Instrument B
G3:   |    B B     B B |        B B     |
D3:   |        B B     |    B B         |
C3:   |B B             |B B         B-  |

SNG A,A,A,A    // For the song, we just play A four times.
