// This is a more complicated demo, using some fancy features.

// Config block--pretty simple, 100bpm, 2 steps per beat, 8-bit
CFG
TEMPO: 100
BEAT: 2
DEPTH: 8
NORM: T

// Instruments! Here's where things get weird.
INS

// This is a triangle wave--0 interp to 4 and back down, then we flip it for the negative side.
A: [0i4,4i0]x*[1,-1]

// This is just a simple pulse wave again.
B: [4,-4]

// This is a volume envelope for instrument B.
// First we take Instrument B, then we cross-level
// it by the pattern on the right.
C<BASE=B>: Bxl[0i<wid=120>8,8r16,8i<wid=160>3,3r3000]

// Now our patterns. I'm making each part in a different pattern,
// then I'll combine some of them in the song.

// "A" is just alternating octaves of C, using Instrument B.
// Each note has the "r2" repeat operator, because otherwise it will alternate each step.
SEQ A
[C5r2,C6r2]:    | A A A A A A A A |

// This plays long notes on Inst C. Each note is a random choice from the set.
SEQ B
{G3r8,C3r8,F3r8,C4r8}:  | C------ C------ |

// This plays a scale on instrument B, just for a little variety.
SEQ C
C6:             |           B-    |
A5:             |         B-      |
G5:             |       B-    B-  |
F5:             |     B-          |
D5:             |   B-          B-|
C5:             | B-              |

// Our song goes like this: First just "A", then we'll play A and B together twice ("(A+B)r2"), then just pattern C, and we'll finish off with two rounds of B.
SNG A,(A+B)r2,C,Br2
