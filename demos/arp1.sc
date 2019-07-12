// Simple demo for creating arpeggiators with Core Sounds speed constants.

IMP core.sc   // Import Core Sounds

INS
// Base waveform -- sort of a lop-sided triangle wave
WV: [0i<w=2>9,9i<w=2>0,0i-9,-9i0]
// Base waveform with simple volume envelope
EV<BASE=WV>: WVv<R=4,LOOP=T>[0.5i1,1i<w=3>0.5]

// Our first arpeggiator -- An ascending major chord.
A<BASE=WV>: EVsc(1,SPD_EQT_UP4,SPD_EQT_UP7,2)
// Ascending minor chord.
B<BASE=WV>: EVsc(1,SPD_EQT_UP3,SPD_EQT_UP7,2)
// Ascending minor seventh chord.
C<BASE=WV>: EVsc(1,SPD_EQT_UP3,SPD_EQT_UP7,SPD_EQT_UP10)

SEQ A
E4: |                |        C-------|
A3: |B-------        |B-------        |
G3: |        A-------|                |

SEQ B
A3: |B----   |

SNG Ar4,B
