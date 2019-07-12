// Hello! Welcome to Synth-Corona.
// This is a very simple demo file--it plays my town tune from Animal Crossing

// Everything after a "//" is a comment and is ignored by the renderer.

// We're going to use the Core Sounds library, "core.sc". You'll need to download
// that file and have it in the same folder as this one.

IMP core.sc   // Import the Core Sounds library.

CFG   // Config Chunk, to set up song info

TEMPO: 95   // Set the tempo
NORM: T     // Normalize audio (to max volume)


INS   // Instrument chunk, to create sounds.

// Let's use a basic Triangle Wave from Core Sounds, "WV_TRI".
// Here "A" is the name we're giving our new instrument.
// The meta-tag "<BASE=WV_TRI>" will copy properties from WV_TRI.
// After the colon, we create our Instrument. In this case, we are loading in WV_TRI.
A <BASE=WV_TRI>: WV_TRI


SEQ A   // Sequence chunk. The "A" is this Sequence's name.

F5: |          |  A-        |            |
E5: |    A-    |A-  A-      |            |
D5: |      A---|      A-    |            |
C5: |  A-      |        A---|            |
B4: |          |            |A-          |
A4: |A-        |            |      A-----|
G4: |          |            |  A---      |


SNG A   // The song chunk. Here we are telling the song to play Sequence "A".
