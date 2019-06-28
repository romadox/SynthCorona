// For this demo, we'll do Greensleeves, with a melody and some percussion.

IMP core.sc   // Import Core Sounds. You'll need core.sc in the same folder as this.

CFG   // Config chunk
TEMPO: 90   // 80 beats per minute
NORM: T     // Normalize on

INS

// In the first demo, we loaded a waveform from Core Sounds.
// Now we will use both a waveform an an envelope, for a more dynamic sound.
// The "v" operator is for enVelope (or Volume, if you prefer).
// WV_TRI_2_3 is the waveform; EV_SMTH_LEGATO is our envelope, both from core.sc.
A <BASE=WV_TRI_2_3>: WV_TRI_2_3vEV_SMTH_LEGATO

// For a bass sound, we'll create a square wave from scratch.
// This is simply a pattern, which repeats the numbers 4 and -4.
// These numbers represent the signal values that make up a soundwave,
// And since there are no gradual transitions between the numbers, 
// we get a square wave.
B: [2,-2]

// Now, for a little hat sound, we'll use core sounds again.
// Here we also use "l", the level operator, to reduce the volume to 4 (from 9).
C <BASE=WV_NSE_BLOCK_32>: WV_NSE_BLOCK_16vEV_PER_STACl5


// Now that we have our Instruments, let's sequence the song.
// We could certainly write out all of Greensleeves in order,
// but I notice a number of repeating parts in the melody.
// I'm going to split them up into reusable pieces whenever possible.

SEQ A   // The very first pickup note.
A4: |A-|

SEQ B   // The call portion of the first part of the melody.

//  Melody
F5: |         A  |            |
E5: |      A-- A-|            |
D5: |    A-      |A---        |
C5: |A---        |            |
B4: |            |    A-    A-|
A4: |            |         A  |
G4: |            |      A--   |

//  Bass
C3: |      B---  |            |
A2: |B---      B-|            |
G2: |            |B-- B-      |
E2: |            |      B---  |

// Drum
D6: |  C C   C C |  C C   C C |

SEQ C   // First response for the first part of the melody.

// Melody
C5: |A---        |            |
B4: |            |A---        |
A4: |    A-A-- A-|          A-|
a4: |         A  |    A-      |
E4: |            |      A---  |

// Bass
A2: |B---        |            |
F2: |      B---  |            |
E2: |            |B---  B---  |

// Drum
D6: |    C   C C |    C C   C |

SEQ D   // Second response for the first part of the melody.

// Melody
C5: |A--         |            |
B4: |   A        |            |
A4: |    A-      |A-----A-----|
a4: |      A-  A-|            |
g4: |        A-  |            |

// Bass
A2: |            |B---        |
F2: |B---        |            |
E2: |      B---  |      B---  |

// Drum
D6: |C   C   C C |  C C C     |

SEQ E   // Call portion of the second part of the melody.

// Melody
G5: |A-----A--   |            |
g5: |         A  |            |
E5: |          A-|            |
D5: |            |A---        |
B4: |            |    A-    A-|
A4: |            |         A  |
G4: |            |      A--   |

// Bass
E3: |          B |            |
D3: |            |B---        |
C3: |B---  B--   |            |
G2: |            |      B---  |

// Drum
D6: |  C C   C C |  C C   C C |

SEQ F   // First response for the second part of the melody.

// Melody
C5: |A---        |            |
B4: |            |A---        |
A4: |    A-A-- A-|            |
a4: |         A  |    A-      |
E4: |            |      A-----|

// Bass
A2: |B---        |            |
F2: |      B---  |            |
E2: |            |B---  B---  |

//Drum
D6: |C   C C   C |    C C     |

SEQ G   // Second response for the second part of the melody.

// Melody
C5: |A--         |            |
B4: |   A        |            |
A4: |    A-      |A-----A-----|
a4: |      A-  A-|            |
g4: |        A-  |            |

// Bass
A2: |            |B---  B---- |
F2: |B---        |            |
E2: |      B---  |            |

// Drum
D6: |    C   C C |C   C C     |


// Now we arrange it all together!
SNG A,[B,(C,D)]r2,[E,(F,G)]r2