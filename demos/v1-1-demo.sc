// A little melody demoing the new features in version 1.1!

IMP core.sc

CFG
TEMPO: 100

INS

// The attack/release settings here ("ATK=0.5" and "REL=0.75") set loop points in the 
// envelope pattern, so we can sustain long notes without repeating the fade-in or trail out.
// Additionally, we use the Length module ("6n0.25") to shorten the middle section to 0.25,
// allowing for a snappier release on very short notes.
A<BASE=WV_TRI,SUS=T>: WV_TRIv<ATK=0.5,REL=0.75>[0i<w=0.5>6,6n0.25,6i<w=0.35>0]

SEQ A

A5: |      A         |                |
G5: |A----- A      A |                |
F5: |        A-     A|               A|
D5: |                |A-    A-      A |
C5: |          A A-  |        A--- A  |
A4: |                |  A A-      A   |

SEQ B

G5: |                |      A         |                |                |
F5: |      A A-      |        A-      |        A-     A|               A|
D5: |A-     A        |A-              |A-     A      A |A-    A-      A |
C5: |          A-A- A|          A-A- A|      A   A A-  |        A--- A  |
A4: |  A A-        A |  A A-        A |  A A-          |  A A-      A   |

SEQ C

A5: |      A         |                |
G5: |A----- A      A |                |
F5: |        A-     A|                |
D5: |                |A-    A-        |
C5: |          A A-  |        A------ |
A4: |                |  A A-          |

SNG Ar2,B,C