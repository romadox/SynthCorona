// This is the sound-effects design file from our 2019 Ludum Dare game, Dusk Strider!
// You can find the game here: https://joehasdied.itch.io/dusk-strider

// It was hastily typed up in the final few hours of the game jam, but now I am going
// to use it as an example of how the new batch rendering options can be useful for
// creating sound effects (and just how to do batch renders in general).

// Some of these sounds never made it into the game. Also, you're welcome to use them
// in your own projects, or modify them if you like!

// Here are the features we're making sounds for:
// 	- Player movement (SKATE)
//	- Player jump (JUMP)
//	- Player sliding down wall (SLIDE)
//	- Player landing from jump/fall (LAND)
//	- Player dies (DIE)
//	- Rings (RING)
//	- Dead-zone noise blocks (NOISE)
//	- Player claims checkpoint (CHECKPOINT)


// As usual, we'll be using Core Sounds for this. You'll need core.sc in the same folder.
IMP core.sc

// Config chunk
CFG
// Turning off normalization, so we can get more control over sound volumes.
NORM: F

// Instrument chunk
INS

// Base skate sound, for when the player moves (not implemented)
SKATE <BASE=WV_NSE_SMOOTH_8>: WV_NSE_SMOOTH_8v<r=2,l=t>[0i<w=3>2,0.25r3,0.25i0.45,0.45i<w=0.85>0]
// Skate sound, bundled up for use in a SEQ; with some panning funkyness for fullness
A: SKATE<PAN=3>l3+(SKATE<PAN=-3>l3)

// Base jump sound
JUMP <BASE=WV_SINE_ROUND, LOOP=F, SUS=T>: WV_SINE_ROUNDv<r=2>[3i6,6i6,6i<w=3.85>0]
// Some extra noise for the jump sound
JUMP_NSE <BASE=WV_NSE_SMOOTH_8, LOOP=F, SUS=T>: (WV_NSE_SMOOTH_8l1.35)v<r=2>[2i3,3i<w=5>2,2i<w=4.85>0,0]
// Bundling up the non-noise portion of jump sound
B: JUMPl5
// Bundling up the noise portion of jump sound
C: JUMP_NSE<PAN=3>l3+(JUMP_NSE<PAN=-3>l3)

// Sound for sliding down vertical walls
SLIDE <BASE=WV_NSE_SMOOTH_8>: WV_NSE_SMOOTH_8v<l=t>[4i<w=3>6,6i<w=1>5]
// Bundling up the slide sound, with panning for fullness
D <BASE=SLIDE>: SLIDE<PAN=3>l3+(SLIDE<PAN=-3>l1)

// Landing sound
LAND <BASE=WV_SINE_ROUND, LOOP=F, SUS=T>: WV_SINE_ROUNDs<r=6>[(4+SPD_EQT_UP5)i1,1r-1]v<r=2>[6i0]
// Bundling up the landing sound
E <BASE=LAND>: LANDl4

// Unused version of the death sound
//DIE <BASE=WV_SINE_ROUND, LOOP=F>: (WV_SINE_ROUND+(WV_NSE_RPULSE_16l1))sc<r=2>[(1i<w=4.5>16)i<w=4.5>16,16i<w=2>16,16i<w=1>0]v[1i<w=4>(1i<w=4>4),0]

// Implemented death sound (aka the Warp-Back-To-Checkpoint Screech)
DIE <BASE=WV_SINE_ROUND, LOOP=F>: (WV_SINE_ROUND+(WV_NSE_RPULSE_16l1))sc[0.5i<w=1>(0.5i<w=1>16),16i<w=2>20,20i<w=0.5>0.25,0.25i<w=2>0,0r-1]v[1i<w=4>(1i<w=4>4),4r3,0]
// Bundling death sound
F <BASE=DIE>: [DIE<PAN=-3>l3]+[DIE<PAN=3>s1.025l3]

// Whooshy sound for rings to make (probably not implemented)
RINGS <BASE=WV_NSE_RPULSE_16, LOOP=T>: WV_NSE_RPULSE_16sc[0.5i2,2i<w=4>0.5]v<l=t>[1i<w=2>4,4i<w=4>1]
// Bundling up ring sound
R <BASE=RINGS>: RINGSl0.5

// Dead-zone static sound (not implemented)
NOISE <BASE=WV_NSE_RPULSE_16, LOOP=T>: WV_NSE_RPULSE_16sc{1,1,2,2i1,1i2,0.5,0.25,2,SPD_EQT_UP2,SPD_EQT_DWN2,SPD_EQT_UP5}s0.0625
// Bundling up dead-zone static
N <BASE=NOISE>: [NOISE<PAN=3>l1]+[NOISE<PAN=-3>l1]

// Sound for claiming a checkpoint
CHECKPOINT <BASE=WV_TRI_2_3, LOOP=F,SUS=T>: WV_TRI_2_3sc<r=8>[0.5,SPD_EQT_DWN5,1r-1]vEV_PLK_SUS
// Bundling up checkpoint sound
P <BASE=CHECKPOINT>: CHECKPOINTl5


// SEQUENCES -- Here we assign pitches & play the sounds.
// I've made a different SEQ for each sound.

SEQ A // Skate sound
[{A5,D6,B5,E6}i<w=1.5>{G6,E6,g6},E6i<w=0.5>{D6,A5,B5}]: |A-------|

SEQ B // Jump Sound -- combination of jump tone & jump noise
[A3i<w=0.05>A4,A4i<w=0.5>D4,D4r2,D4i<w=0.5>D6]: |B        |
[A5i<w=2>D6,D6r7]:                              |C        |

SEQ C // Slide sound
D5: |D---------------|----------------|----------------|

SEQ D // Land Sound
D2: |E       |

SEQ E // Death sound
g3: |F----------|

SEQ F // Ring sound
D1: |R-----------|------------|

SEQ G // Dead zone noise
D1: |N---------------|

SEQ H // Checkpoint noise
A5: |P       |


// SONGS -- here we list the batch of files to render.

SNG skate: A   	 // Skate sound as skate.wav
SNG jump: B    	  // Jump sound as jump.wav
SNG slide: C   	  // Slide sound as slide.wav
SNG land: D    	  // Land sound as land.wav
SNG die: E     	  // Death sound as die.wav
SNG ring: F    	  // Ring sound as ring.wav
SNG noise: G   	  // Noise sound as noise.wav
SNG checkpoint: H // Checkpoint sound as checkpoint.wav