
// Synth-Corona Simple Instrument Kit
// by: Nash High

// Modules
MDL

// ~~ SPEED MODULES ~~

// ~ Speed Constants for Pitch Shifting ~
// Equal Temperament Speed Ratios
SPD_EQT_UP1: 1.0594630943592953
SPD_EQT_UP2: 1.122462048309373
SPD_EQT_UP3: 1.1892071150027212
SPD_EQT_UP4: 1.2599210498948734
SPD_EQT_UP5: 1.3348398541700346
SPD_EQT_UP6: 1.4142135623730954
SPD_EQT_UP7: 1.498307076876682
SPD_EQT_UP8: 1.5874010519682
SPD_EQT_UP9: 1.6817928305074297
SPD_EQT_UP10: 1.7817974362806794
SPD_EQT_UP11: 1.887748625363388
SPD_EQT_UP12: 2.0

SPD_EQT_DWN1: 0.9438743126816934
SPD_EQT_DWN2: 0.8908987181403393
SPD_EQT_DWN3: 0.8408964152537144
SPD_EQT_DWN4: 0.7937005259840996
SPD_EQT_DWN5: 0.7491535384383405
SPD_EQT_DWN6: 0.7071067811865474
SPD_EQT_DWN7: 0.667419927085017
SPD_EQT_DWN8: 0.6299605249474364
SPD_EQT_DWN9: 0.5946035575013603
SPD_EQT_DWN10: 0.5612310241546863
SPD_EQT_DWN11: 0.5297315471796474
SPD_EQT_DWN12: 0.5

// Pythagorean Just Tuning Speed Values
SPD_PYG_UP1: 256/243
SPD_PYG_UP2: 9/8
SPD_PYG_UP3: 32/27
SPD_PYG_UP4: 81/64
SPD_PYG_UP5: 4/3
SPD_PYG_UP6: 729/512
SPD_PYG_UP7: 3/2
SPD_PYG_UP8: 128/81
SPD_PYG_UP9: 27/16
SPD_PYG_UP10: 16/9
SPD_PYG_UP11: 243/128

SPD_PYG_DWN1: 243/256
SPD_PYG_DWN2: 8/9
SPD_PYG_DWN3: 27/32
SPD_PYG_DWN4: 64/81
SPD_PYG_DWN5: 3/4
SPD_PYG_DWN6: 729/1024
SPD_PYG_DWN7: 2/3
SPD_PYG_DWN8: 81/128
SPD_PYG_DWN9: 16/27
SPD_PYG_DWN10: 9/16
SPD_PYG_DWN11: 128/243

// Five-Limit Just Intonation
SPD_LIM5_UP1: 16/15
SPD_LIM5_UP2: 9/8
SPD_LIM5_UP3: 6/5
SPD_LIM5_UP4: 5/4
SPD_LIM5_UP5: 4/3
SPD_LIM5_UP6: 45/32
SPD_LIM5_UP7: 3/2
SPD_LIM5_UP8: 8/5
SPD_LIM5_UP9: 5/3
SPD_LIM5_UP10: 9/5
SPD_LIM5_UP11: 15/8

SPD_LIM5_DWN1: 15/16
SPD_LIM5_DWN2: 8/9
SPD_LIM5_DWN3: 5/6
SPD_LIM5_DWN4: 4/5
SPD_LIM5_DWN5: 3/4
SPD_LIM5_DWN6: 32/45
SPD_LIM5_DWN7: 2/3
SPD_LIM5_DWN8: 5/8
SPD_LIM5_DWN9: 3/5
SPD_LIM5_DWN10: 5/9
SPD_LIM5_DWN11: 8/15

// ~~ KICK DRUM SPEED ENVELOPES ~~
SPD_KICK_SHORT: [1i<w=30>0.2,0.2i<w=10>0.125]

// Basic Random Decimals (0-1)

// Simple 1-digit random (0-1)
RAND: {0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9}
// 2-digit random (0-1)
RAND_2: RAND+[RAND/10]
// 3-digit random (0-1)
RAND_3: RAND_2+[RAND/100]
// 4-digit random (0-1)
RAND_4: RAND_3+[RAND/1000]
// 5-digit random (0-1)
RAND_5: RAND_4+[RAND/10000]

// Random Values (for use as a wave level, volume, etc.) [0,9)
// Single-Digit Random Value [0-8]
RANDV: RAND*9
// 2-digit Random Value [0-8.9]
RANDV_2: RAND_2*9
// 3-digit Random Value [0-8.99]
RANDV_3: RAND_3*9
// 4-digit Random Value [0-8.999]
RANDV_4: RAND_4*9
// 5-digit Random Value [0-8.9999]
RANDV_5: RAND_5*9

// Some Simple Curves
// Basic Bezier Arc
BEZIER_ARC: [(0i9)i9,9i(9i0)]
// Soft Bezier Arc
BEZIER_ARC_SOFT: [0i(0i4.5),(4.5i9)i9,9i(9i4.5),(4.5i0)i0]


// ~*~*~ ENVELOPES ~*~*~

// ~~ PLUCK ~~
EV_PLK: [0i<w=0.15>9,9i<w=0.35>3,3i<w=2>0]
EV_PLK_SUS: [0i<w=0.15>9,9i<w=0.35>5,5i<w=6>0]
EV_PLK_STAC: [0i<w=0.15>9,9i<w=0.35>1,1i<w=0.25>0]
EV_PLK_SOFT: [0i<w=0.25>7,7i<w=0.35>2,2i<w=2>0]
EV_PLK_SOFT_SUS: [0i<w=0.25>7,7i<w=0.35>3,3i<w=6>0]
EV_PLK_SOFT_STAC: [0i<w=0.15>7,7i<w=0.45>0]
EV_PLK_HARD: [0i<w=0.08>9,9i<w=0.1>6,6i<w=0.5>3,3i<w=2>0]
EV_PLK_HARD_SUS: [0i<w=0.08>9,9i<w=0.25>7,7i<w=0.7>5,5i<w=6>0]
EV_PLK_HARD_STAC: [0i<w=0.08>9,9i<w=0.25>4,4i<w=0.3>0]
EV_PLK_SHORT: [0i<w=0.15>9,9i<w=0.25>2,2i<w=0.1>0]
EV_PLK_SHORT_SUS: [0i<w=0.15>9,9i<w=0.35>2,2i<w=6>0]
EV_PLK_SHORT_STAC: [0i<w=0.15>9,9i<w=0.25>0]
EV_PLK_LONG: [0i<w=0.35>9,9i<w=0.5>4,4i<w=2>0]
EV_PLK_LONG_SUS: [0i<w=0.35>9,9i<w=0.75>5,5i<w=6>0]
EV_PLK_LONG_STAC: [0i<w=0.35>9,9i<w=0.75>2,2i<w=0.1>0]
EV_PLK_DBLTAP: [0i<w=0.15>9,9i<w=0.1>7,7i<w=0.05>9,9i<w=0.35>4,4i<w=2>0]
EV_PLK_SMOOTH: [0i<w=0.25>(0i<w=0.25>9),(9i<w=0.35>5)i<w=0.35>5,5i<w=2>(5i<w=2>0)]
EV_PLK_SMOOTH_SUS: [0i<w=0.25>(0i<w=0.25>9),(9i<w=0.5>5)i<w=0.5>5,5i<w=6>(5i<w=6>0)]
EV_PLK_SMOOTH_STAC: [0i<w=0.2>(0i<w=0.2>9),(9i<w=0.25>3)i<w=0.25>3,3i<w=0.5>(3i<w=0.5>0)]
EV_PLK_LONGTAIL: [0i<w=0.15>9,9i<w=0.35>4,(4i<w=6>0)i<w=6>0]
EV_PLK_LONGTAIL_SUS: [0i<w=0.15>9,9i<w=0.5>6,(6i<w=10>0)i<w=10>0]
EV_PLK_LONGTAIL_STAC: [0i<w=0.15>9,9i<w=0.25>2,(2i<w=4>0)i<w=4>0]
EV_PLK_SUPER_STAC: [0i<w=0.15>9,9i<w=0.35>0]
EV_PLK_SNAP: [0i<w=0.25>9,(9i<w=0.75>0)i<w=0.75>0]
EV_PLK_SNAP_SUS: [0i<w=0.25>9,(9i<w=5.75>0)i<w=5.75>0]
EV_PLK_SNAP_STAC: [0i<w=0.15>9,9i<w=0.1>0]

// ~~ SMOOTH ~~
EV_SMTH: [0i<w=0.35>7,7i<w=0.25>9,9i<w=1.25>5,5i<w=2>0]
EV_SMTH_SUS: [0i<w=0.35>7,7i<w=0.25>9,9i<w=2.25>5,5i<w=6>0]
EV_SMTH_STAC: [0i<w=0.3>7,7i<w=0.15>9,9i<w=0.25>3,3i<w=0.5>0]
EV_SMTH_SOFT: [0i<w=0.35>5,5i<w=0.25>7,7i<w=1.25>4,4i<w=1.6>0]
EV_SMTH_SOFT_SUS: [0i<w=0.35>5,5i<w=0.25>7,7i<w=2>4,4i<w=4>0]
EV_SMTH_SOFT_STAC: [0i<w=0.35>5,5i<w=0.25>7,7i<w=0.75>4,4i<w=0.25>0]
EV_SMTH_HARD: [0i<w=0.15>7,7i<w=0.15>9,9i<w=1>5,5i<w=2>0]
EV_SMTH_HARD_SUS: [0i<w=0.15>7,7i<w=0.15>9,9i<w=1.25>5,5i<w=6>0]
EV_SMTH_HARD_STAC: [0i<w=0.15>7,7i<w=0.15>9,9i<w=0.5>5,5i<w=0.5>0]
EV_SMTH_MUTED: [0i<w=0.35>5,5i<w=0.35>7,7i<w=0.5>1,1i0]
EV_SMTH_MUTED_SUS: [0i<w=0.35>5,5i<w=0.35>7,7i<w=1.25>1,1i<w=4>0]
EV_SMTH_MUTED_STAC: [0i<w=0.35>5,5i<w=0.25>7,7i<w=0.25>0]
EV_SMTH_ROUND: [(0i<w=0.55>9)i<w=0.55>9,9i<w=1.25>(9i<w=1.25>5),(5i<w=2>0)i<w=2>0]
EV_SMTH_ROUND_SUS: [(0i<w=0.55>9)i<w=0.55>9,9i<w=2.25>(9i<w=2.25>5),(5i<w=6>0)i<w=6>0]
EV_SMTH_ROUND_STAC: [(0i<w=0.35>9)i<w=0.35>9,9i<w=0.5>(9i<w=0.5>5),(5i<w=0.5>0)i<w=0.5>0]
EV_SMTH_LONGTAIL: [0i<w=0.35>9,9i<w=1.35>4,(4i<w=6>0)i<w=6>0]
EV_SMTH_LONGTAIL_SUS: [0i<w=0.35>9,9i<w=2.35>4,(4i<w=10>0)i<w=10>0]
EV_SMTH_LONGTAIL_STAC: [0i<w=0.25>9,9i<w=0.25>4,(4i0)i0]
EV_SMTH_LEGATO: [0i<w=0.35>7,7i<w=0.25>9,9i<w=1.25>5,5r-1]
EV_SMTH_SOFT_LEGATO: [0i<w=0.65>7,7i<w=2.25>3,3r-1]
EV_SMTH_HARD_LEGATO: [0i<w=0.25>9,9i<w=0.5>7,7r-1]
EV_SMTH_MAX_LEGATO: [(0i<w=0.65>9)i<w=0.65>9,9r-1]
EV_SMTH_ROUND_LEGATO: [0i<w=0.35>(0i<w=0.35>7),(7i<w=0.35>9)i<w=0.35>9,9i<w=2.25>(9i<w=2.25>5),5r-1]
EV_SMTH_SNAP: [0i<w=0.65>9,(9i<w=1.5>0)i<w=1.5>0]
EV_SMTH_SNAP_SUS: [0i<w=0.65>9,(9i<w=6>0)i<w=6>0]
EV_SMTH_SNAP_STAC: [0i<w=0.5>9,(9i<w=0.25>0)i<w=0.25>0]

// ~~ BOW ~~
EV_BOW: [0i3,3i<w=3>7,7i<w=3>9,9i<w=6>5,5r-1]
EV_BOW_STK: [0i<w=0.75>6,6i<w=2>9,9i<w=6>5,5r-1]
EV_BOW_GTL: [0i<w=1.35>3,3i<w=5>7,7i<w=5>9,9i<w=4>5,5r-1]
EV_BOW_SOFT: [0i<w=3.5>5,5i<w=4>7,7i<w=5>3,3r-1]
EV_BOW_SOFT_STK: [0i<w=1.2>5,5i<w=2.25>7,7i<w=3>3,3r-1]
EV_BOW_SOFT_GTL: [0i<w=5.5>5,5i<w=6>7,7i<w=5>3,3r-1]
EV_BOW_HARD: [0i5,5i<w=2>9,9i<w=4>6,6r-1]
EV_BOW_HARD_STK: [0i<w=0.75>6,6i9,9i<w=4>6,6r-1]
EV_BOW_HARD_GTL: [0i<w=1.75>5,5i<w=4>9,9i<w=6>6,6r-1]
EV_BOW_SLOW: [0i<w=6>9,9i<w=5>5,5r-1]
EV_BOW_SLOW_STK: [0i<w=3>5,5i9,9i7,7i<w=3>5,5r-1]
EV_BOW_SLOW_GTL: [0i<w=6>5,5i<w=8>9,9i<w=4>5,5r-1]
EV_BOW_CONCAVE: [0i<w=4>(0i<w=4>9),9i<w=2>(9i<w=2>6),(6i<w=4>4)i<w=4>4,4r-1]
EV_BOW_CONCAVE_STK: [0i<w=1.2>(0i<w=1.2>9),9i<w=1.4>(9i<w=1.4>6),(6i<w=4>4)i<w=4>4,4r-1]
EV_BOW_CONCAVE_GTL: [0i<w=6>(0i<w=6>7),(7i<w=2>9)i<w=2>9,9i<w=2>(9i<w=2>6),(6i<w=4>4)i<w=4>4,4r-1]
EV_BOW_CONVEX: [(0i<w=4>9)i<w=4>9,9i<w=2>(9i<w=2>6),(6i<w=4>4)i<w=4>4,4r-1]
EV_BOW_CONVEX_STK: [(0i<w=1.2>9)i<w=1.2>9,9i<w=1.4>(9i<w=1.4>6),(6i<w=4>4)i<w=4>4,4r-1]
EV_BOW_CONVEX_GTL: [(0i<w=6>7)i<w=6>7,7i<w=2>(7i<w=2>9),9i<w=2>(9i<w=2>6),(6i<w=4>4)i<w=4>4,4r-1]
EV_BOW_SMOOTH: [0i<w=3>(0i<w=3>5),(5i<w=5>9)i<w=5>9,9i<w=6>(9i<w=2>7),(7i<w=8>3)i<w=8>3,3r-1]
EV_BOW_SMOOTH_STK: [0i<w=0.75>(0i<w=0.75>5),(5i<w=1.2>9)i<w=1.2>9,9i<w=2>(9i<w=2>7),(7i<w=5>3)i<w=4>3,3r-1]
EV_BOW_SMOOTH_GTL: [0i<w=5>(0i<w=5>4),(5i<w=7>9)i<w=7>9,9i<w=6>(9i<w=2>7),(7i<w=8>3)i<w=8>3,3r-1]
EV_BOW_FADEIN: [0i<w=2>4,4i<w=4>9,9i<w=2>4,4i0]
EV_BOW_FADEIN_SUS: [0i<w=2>4,4i<w=4>9,9i<w=2>4,4i<w=8>0]
EV_BOW_FADEIN_STAC: [0i<w=2>4,4i<w=4>9,9i0]
EV_BOW_FADEIN_SLOW: [0i<w=4>(0i<w=4>4.5),(4.5i<w=4>9)i<w=4>9,9i<w=4>(9i<w=4>4.5),(4.5i<w=4>0)i<w=4>0]
EV_BOW_DBLFADE: [0i<w=4>(0i<w=4>4.5),(4.5i<w=4>9)i<w=4>9,9i(9i7),(7i4.5)i4.5,4.5i(4.5i7),(7i9)i9,9i(9i4.5),(4.5i0)i<w=2>0]

// ~~ PERCUSSION ~~
EV_PER: [6i<w=0.15>9,9i<w=0.85>0]
EV_PER_SUS: [6i<w=0.15>9,9i<w=0.85>4,4i<w=1.5>0]
EV_PER_STAC: [6i<w=0.15>9,9i<w=0.35>0]
EV_PER_TAP: [3i<w=0.15>6,6i<w=0.25>9,9i<w=0.25>6,6i<w=0.85>0]
EV_PER_TAP_SUS: [3i<w=0.15>6,6i<w=0.25>9,9i<w=0.25>6,6i<w=0.85>3,3i<w=2>0]
EV_PER_TAP_STAC: [3i<w=0.15>6,6i<w=0.25>9,9i<w=0.25>6,6i<w=0.85>0]
EV_PER_CLICK: [9i<w=0.2>0]
EV_PER_CLICK_SUS: [9i<w=0.2>2,2i<w=1.8>0]
EV_PER_CLICK_STAC: [9i<w=0.07>0]
EV_PER_SNARE: [8i<w=0.15>9,9i<w=0.15>6,6i<w=0.35>1,1i<w=0.25>0]
EV_PER_SNARE_SUS: [8i<w=0.15>9,9i<w=0.15>6,6i<w=0.5>3,3i<w=0.85>0]
EV_PER_SNARE_STAC: [8i<w=0.15>9,9i<w=0.15>6,6i<w=0.35>0]
EV_PER_SNARE_BRUSH: [3i<w=0.55>9,9i<w=0.25>6,6i<w=0.5>2,2i<w=0.25>0]+[{0,0.2,0.4}s3]
EV_PER_SNARE_BRUSHDRAG: [0i<w=0.75>5,5i<w=0.25>9,9i<w=0.75>4,4i<w=0.25>0]+[{0,0.2,0.4}s3]
EV_PER_CYMBAL: [9i<w=0.3>6,6i<w=2>0]+[{0,0.2,0.4}s3]
EV_PER_CYMBAL_STAC: [9i<w=0.2>5,5i0]+[{0,0.2,0.4}s3]
EV_PER_CYMBAL_SUS: [9i<w=0.5>6,6i<w=2>0]+[{0,0.2,0.4}s3]
EV_PER_KICK: [9i<w=0.1>1,1i<w=0.25>0]
EV_PER_KICK_STAC: [9i<w=0.15>0]
EV_PER_KICK_SUS: [9i<w=0.1>3,3i<w=0.9>0]
EV_PER_TOM: [6i<w=0.1>9,9i<w=0.2>4,4i<w=0.8>0]
EV_PER_TOM_STAC: [6i<w=0.1>9,9i<w=0.1>4,4i<w=0.3>0]
EV_PER_TOM_SUS: [6i<w=0.1>9,9i<w=0.6>4,4i<w=1.8>0]
EV_PER_SOFT: [6i<w=0.4>9,9i<w=0.2>2,2i<w=0.9>0]
EV_PER_SOFT_SUS: [6i<w=0.4>9,9i<w=0.6>4,4i<w=1.8>0]
EV_PER_SOFT_STAC: [6i<w=0.3>9,9i<w=0.2>0]

// ~*~*~ WAVEFORMS ~*~*~
INS

// ~~ TRIANGLE WAVES ~~
WV_TRI: [0i9,9i<w=2>-9,-9i0]
WV_TRI_2_3: [0i9,9i<w=3>-9,-9i0]
WV_TRI_1_2: [0i9,9i<w=4>-9,-9i0]
WV_TRI_1_3: [0i9,9i<w=6>-9,-9i0]
WV_TRI_1_4: [0i9,9i<w=8>-9,-9i0]
WV_TRI_3_2: [0i<w=3>9,9i<w=4>-9,-9i<w=3>0]
WV_TRI_2_1: [0i9,9i-9,-9i0]
WV_TRI_3_1: [0i<w=3>9,9i<w=2>-9,-9i<w=3>0]
WV_TRI_4_1: [0i<w=2>9,9i-9,-9i<w=2>0]
WV_TRI_FLATTOP: [0i9,9,9i0]x*[1,-1]
WV_TRI_FLATGAPS: [0,0i9,9,9i0]x*[1,-1]
WV_TRI_FLATBASE_1: [0,0i9,9i0]x*[1,-1]
WV_TRI_FLATBASE_2: [0,0i9,9i0,0]x*[1,-1]
WV_TRI_JAGGED: [0i5,5,5i9,9i5,5,5i0]x*[1,-1]
WV_TRI_FANGS: [0i9,9i5,5,5i9,9i0]x*[1,-1]
WV_TRI_MOUNTAIN: [0i5,5i<w=3>9,9i<w=3>5,5i0]x*[1,-1]
WV_TRI_PEAK: [0i<w=3>5,5i9,9i5,5i<w=3>0]x*[1,-1]
WV_TRI_2_3_JANKY: [0i<w=2>9,9i<w=3>0]x*[1,-1]
WV_TRI_1_2_JANKY: [0i9,9i<w=2>0]x*[1,-1]
WV_TRI_1_3_JANKY: [0i9,9i<w=3>0]x*[1,-1]
WV_TRI_1_4_JANKY: [0i9,9i<w=4>0]x*[1,-1]
WV_TRI_3_2_JANKY: [0i<w=3>9,9i<w=2>0]x*[1,-1]
WV_TRI_2_1_JANKY: [0i<w=2>9,9i0]x*[1,-1]
WV_TRI_3_1_JANKY: [0i<w=3>9,9i0]x*[1,-1]
WV_TRI_4_1_JANKY: [0i<w=4>9,9i0]x*[1,-1]
WV_TRI_2UP_2DOWN: [0i9,9i0]x*[1,1,-1,-1]


// ~~ SQUARE WAVES ~~
WV_SQR: [9,-9]
WV_SQR_4_5: [9r4,-9r5]
WV_SQR_3_4: [9r3,-9r4]
WV_SQR_2_3: [9r2,-9r3]
WV_SQR_1_2: [9,-9r2]
WV_SQR_1_3: [9,-9r3]
WV_SQR_1_4: [9,-9r4]
WV_SQR_5_4: [9r5,-9r4]
WV_SQR_4_3: [9r4,-9r3]
WV_SQR_3_2: [9r3,-9r2]
WV_SQR_2_1: [9r2,-9]
WV_SQR_3_1: [9r3,-9]
WV_SQR_4_1: [9r4,-9]
WV_SQR_UPSTAIRS: [0,9,-9]
WV_SQR_DOWNSTAIRS: [0,-9,9]
WV_SQR_UPDOWNSTAIRS: [0,(9,-9)]r2
WV_SQR_UPSTAIRS_2: [0,4.5,9,-9,-4.5]
WV_SQR_DOWNSTAIRS_2: [0,-4.5,-9,9,4.5]
WV_SQR_UPDOWNSTAIRS_2: [(0,9),4.5]r2x*[1,-1]
WV_SQR_4_5_JANKY: [9r4,-9r5]x*[1,-1]
WV_SQR_3_4_JANKY: [9r3,-9r4]x*[1,-1]
WV_SQR_2_3_JANKY: [9r2,-9r3]x*[1,-1]
WV_SQR_1_2_JANKY: [9,-9r2]x*[1,-1]
WV_SQR_1_3_JANKY: [9,-9r3]x*[1,-1]
WV_SQR_1_4_JANKY: [9,-9r4]x*[1,-1]
WV_SQR_HEARTBYTES: [9,-9,0r2]


// ~~ SAW WAVES ~~
WV_SAW: 9i-9
WV_RAMP: -9i9
WV_SHARP: [0i9,0i-9]
WV_SAW_STAIR: [9i-9,0]
WV_RAMP_STAIR: [-9i9,0]
WV_SAW_THORNS: [(0i9,0i-9),0]r2
WV_SAW_FLAT: [9,9i<w=2>-9,-9]
WV_RAMP_FLAT: [-9,-9i<w=2>9,9]
WV_SAW_EXTRAFLAT: [9,9i-9,-9]
WV_RAMP_EXTRAFLAT: [-9,-9i9,9]
WV_SAW_4_5: [9i<w=4>-9,9i<w=5>-9]
WV_SAW_3_4: [9i<w=3>-9,9i<w=4>-9]
WV_SAW_2_3: [9i<w=2>-9,9i<w=3>-9]
WV_SAW_1_2: [9i-9,9i<w=2>-9]
WV_RAMP_4_5: [-9i<w=4>9,-9i<w=5>9]
WV_RAMP_3_4: [-9i<w=3>9,-9i<w=4>9]
WV_RAMP_2_3: [-9i<w=2>9,-9i<w=3>9]
WV_RAMP_1_2: [-9i9,-9i<w=2>9]
WV_SHARP_4_5: [0i<w=4>9,0i<w=5>-9]
WV_SHARP_3_4: [0i<w=3>9,0i<w=4>-9]
WV_SHARP_2_3: [0i<w=2>9,0i<w=3>-9]
WV_SHARP_1_2: [0i9,9i<w=2>-9]
WV_SHARP_1_3: [0i9,9i<w=3>-9]
WV_SHARP_1_4: [0i9,9i<w=4>-9]
WV_SAW_2UP_2DOWN: [0i9r2]x*[1,-1]
WV_SAW_2UP_1DOWN: [0i9r2,0i-9]


// ~~ SINE LIKE WAVES ~~
// Note: I'm going to call these "sine waves" from
// here on out, but know that they are not actually
// sine waves. They are more appropriately "Bezier waves",
// because they are created through a similar process to
// Bezier curves. However, the end result resembles a sine wave
// visually and in sound character.

WV_SINE: [(0i9)i9,9i(9i0)]x*[1,-1]
WV_SINE_DIMPLE: [0i(0i4.5),(4.5i9)i9,9i(9i4.5),(4.5i0)i0]x*[1,-1]
WV_SINE_OCEAN: [0i(0i9),9i(9i0),(0i-9)i-9,(-9i0)i0]
WV_SINE_OCEAN_RVS: [(0i9)i9,(9i0)i0,0i(0i-9),-9i(-9i0)]
WV_SINE_POINT: [(0i4.5)i9,9i(4.5i0)]x*[1,-1]
WV_SINE_HEART: [(0i26)i4.5,4.5i(26i0)]x*[1,-1]
WV_SINE_ROUND: [((0i9)i9)i9,9i(9i(9i0))]x*[1,-1]
WV_SINE_SAW: 9i(9i-9)
WV_SINE_RAMP: (-9i9)i9
WV_SAW_CONCAVE: (9i-9)i9
WV_RAMP_CONCAVE: -9i(-9i9)
WV_SINE_CONCAVE: [0i(0i9),(9i0)i0]x*[1,-1]
WV_SINE_BOWTIE: [(0i9)i9,-9i(-9i0)]
WV_SINE_DIMPLE_2: [0i(0i2.25),(2.25i4.5)i4.5,4.5i(4.5i6.75),(6.75i9)i9,9i(9i6.75),(6.75i4.5)i4.5,4.5i(4.5i2.25),(2.25i0)i0]x*[1,-1]
WV_SINE_ROUND_2: [(((0i9)i9)i9)i9,9i(9i(9i(9i0)))]x*[1,-1]
WV_SINE_WOBBLY: [(0i21)i6,(6i-6)i(0i3),3i(-3i0)]x*[1,-1]
WV_SINE_LEANING: [(0i27)i18i0,0i(-18i(-27i0))]
WV_SINE_BUMPTAIL: [(0i9)i9,9i<w=2>(9i<w=2>0),(0i<w=2>-9)i<w=2>-9,-9i(-9i0)]
WV_SINE_TAILBUMP: [0i<w=2>9,9i(9i0),(0i-9)i-9,-9i<w=2>(-9i<w=2>0)]
WV_SINE_BUMPTAIL_LONG: [(0i9)i9,9i<w=3>(9i<w=3>0),(0i<w=3>-9)i<w=3>-9,-9i(-9i0)]
WV_SINE_TAILBUMP_LONG: [0i<w=3>9,9i(9i0),(0i-9)i-9,-9i<w=3>(-9i<w=3>0)]
WV_SINE_ORANGE: [0i<w=0.2>(0i<w=0.2>1),(1i<w=0.8>9)i<w=0.8>9,9i<w=2>(9i<w=2>3),(3i0)i0]x*[1,-1]
WV_SINE_CALLIG: [(0i21)i(14i-14)i(-21i0)]x*[2,-2]
WV_SINE_VEXCAVE: [(0i9)i9,9i(9i0),0i(0i-9),(-9i0)i0]
WV_SINE_CAVEX: [0i(0i9),(9i0)i0,(0i-9)i-9,-9i(-9i0)]
WV_SINE_VEXCAVE_ALT <PRD=4>: [(0i9)i9,9i(9i0),0i(0i-9),(-9i0)i0,0i(0i9),(9i0)i0,(0i-9)i-9,-9i(-9i0)]


// ~~ NOISE WAVES ~~
WV_NSE_BLOCK_128 <PRD=1>: [RANDV_5*{1,-1}]s128
WV_NSE_BLOCK_64 <PRD=1>: [RANDV_5*{1,-1}]s64
WV_NSE_BLOCK_32 <PRD=1>: [RANDV_5*{1,-1}]s32
WV_NSE_BLOCK_16 <PRD=1>: [RANDV_5*{1,-1}]s16
WV_NSE_BLOCK_8 <PRD=1>: [RANDV_5*{1,-1}]s8
WV_NSE_LINE_128 <PRD=1>: [[0i<w=0.5>9,9i<w=0.5>0]*{1,-1}lRANDV_5]s128
WV_NSE_LINE_64 <PRD=1>: [[0i<w=0.5>9,9i<w=0.5>0]*{1,-1}lRANDV_5]s64
WV_NSE_LINE_32 <PRD=1>: [[0i<w=0.5>9,9i<w=0.5>0]*{1,-1}lRANDV_5]s32
WV_NSE_LINE_16 <PRD=1>: [[0i<w=0.5>9,9i<w=0.5>0]*{1,-1}lRANDV_5]s16
WV_NSE_LINE_8 <PRD=1>: [[0i<w=0.5>9,9i<w=0.5>0]*{1,-1}lRANDV_5]s8
WV_NSE_SMOOTH_128 <PRD=1>: [[0i<w=0.25>(0i<w=0.25>4.5),(4.5i<w=0.25>9)i<w=0.25>9,9i<w=0.25>(9i<w=0.25>4.5),(4.5i<w=0.25>0)i<w=0.25>0]*{1,-1}lRANDV_5]s32
WV_NSE_SMOOTH_64 <PRD=1>: [[0i<w=0.25>(0i<w=0.25>4.5),(4.5i<w=0.25>9)i<w=0.25>9,9i<w=0.25>(9i<w=0.25>4.5),(4.5i<w=0.25>0)i<w=0.25>0]*{1,-1}lRANDV_5]s16
WV_NSE_SMOOTH_32 <PRD=1>: [[0i<w=0.25>(0i<w=0.25>4.5),(4.5i<w=0.25>9)i<w=0.25>9,9i<w=0.25>(9i<w=0.25>4.5),(4.5i<w=0.25>0)i<w=0.25>0]*{1,-1}lRANDV_5]s8
WV_NSE_SMOOTH_16 <PRD=1>: [[0i<w=0.25>(0i<w=0.25>4.5),(4.5i<w=0.25>9)i<w=0.25>9,9i<w=0.25>(9i<w=0.25>4.5),(4.5i<w=0.25>0)i<w=0.25>0]*{1,-1}lRANDV_5]s4
WV_NSE_SMOOTH_8 <PRD=1>: [[0i<w=0.25>(0i<w=0.25>4.5),(4.5i<w=0.25>9)i<w=0.25>9,9i<w=0.25>(9i<w=0.25>4.5),(4.5i<w=0.25>0)i<w=0.25>0]*{1,-1}lRANDV_5]s2
WV_NSE_RPULSE_64 <PRD=2>: [9,-9]s[(RAND_5s64)*8]
WV_NSE_RPULSE_16 <PRD=2>: [9,-9]s[(RAND_5s16)*8]
WV_NSE_RPULSE_4 <PRD=2>: [9,-9]s[(RAND_5s4)*8]
WV_NSE_RTRI_64 <PRD=4>: [0i9,9i<w=2>-9,-9i0]s[(RAND_5s64)*8]
WV_NSE_RTRI_16 <PRD=4>: [0i9,9i<w=2>-9,-9i0]s[(RAND_5s16)*8]
WV_NSE_RTRI_4 <PRD=4>: [0i9,9i<w=2>-9,-9i0]s[(RAND_5s4)*8]
WV_NSE_RSINE_64 <PRD=4>: [(0i9)i9,9i(9i0),(0i-9)i-9,-9i(-9i0)]s[(RAND_5s64)*8]
WV_NSE_RSINE_16 <PRD=4>: [(0i9)i9,9i(9i0),(0i-9)i-9,-9i(-9i0)]s[(RAND_5s16)*8]
WV_NSE_RSINE_4 <PRD=4>: [(0i9)i9,9i(9i0),(0i-9)i-9,-9i(-9i0)]s[(RAND_5s4)*8]
WV_NSE_DOUBLEBIT <PRD=1>: [RANDV_5*{1,-1}]s[RAND_5*8]
WV_NSE_SUPERCHEAP <PRD=8>: {0,1,2,3,4,5,6,7,8,9}*{1,-1}


// ~~ CHIPPY WAVES ~~
WV_CHP_TRI: [0,2,4,6,8,6,4,2]x*[1,-1]
WV_CHP_TRI_2: [0,1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1]x*[1,-1]
WV_CHP_SINE: [0,4,7,8,9,9,8,7,4]x*[1,-1]
WV_CHP_SINE_2: [0,3,5,6,7r2,8r3,9r4,8r3,7r2,6,5,3]x*[1,-1]
WV_CHP_SAW: [9,6,3,0,-3,-6,-9]
WV_CHP_SAW_2: [9,8,7,6,5,4,3,2,1,0,-1,-2,-3,-4,-5,-6,-7,-8,-9]
WV_CHP_RAMP: [-9,-6,-3,0,3,6,9]
WV_CHP_RAMP_2: [-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9]
WV_CHP_TOOTH: [0,8,9r3,8]x*[1,-1]
WV_CHP_IMPULSE: [9,0r46,-9]
WV_CHP_NOISE <PRD=4>: {0,3,6,9}*{1,-1}
WV_CHP_NOISE_2 <PRD=4>: {0,3,6,9}*{1,-1}s{0.25,0.5,1,2,4,8}
WV_CHP_BUBBLEGUM: [0,4,8,9r4,8,4]x*[1,-1]
WV_CHP_HOUNDS: [3,6,9,-9,-3,-6,0r6]
WV_CHP_NOISE_TRI: [{0,1,2},{3,4,5},{6,7,8},{9,8,7},{6,5,4},{3,2,1}]x*[1,-1]
WV_CHP_NOISE_TRI_LITE: [0,{1,2},3,{4,5},6,{7,8},9,{8,7},6,{5,4},3,{2,1}]x*[1,-1]
WV_CHP_NOISE_TRI_MINI: [0,1,2,{2,3,4},4,5,6,{6,7,8},9,8,7,{7,6,5},5,4,3,{3,2,1}]x*[1,-1]
WV_CHP_RIBBON: [0,1,2,3,5,8,9,8,5,2,-2,-5,-8,-9,-8,-5,-3,-2,-1]
WV_CHP_SIMPLE: [0,5,9,4]x*[1,-1]
WV_CHP_INTERLOCK_4_3: [0,2,4,6]+[0,1,3]x*[1,-1]
WV_CHP_INTERLOCK_3_5: [0,3,5]+[0,1,2,3,4]x*[1,-1]
WV_CHP_MULTLOCK_4_3: [0,1,2,3]*[0,2,3]
WV_CHP_TRILOCK: [0,1,2]+[0,1,2,3]+[0,1,2,3,4]x*[1,-1]
WV_CHP_STRANGE: [0,6,(5,6,7,8,9),6]x*[1,-1]
WV_CHP_FLUX: [0,(3,6,9),(5,7),(3,6,9)]x*[1,-1]
WV_CHP_PRIMEWAVE: [2,3,5,7,5,3,2]x*[1,-1]


// ~*~ INSTRUMENTS ~*~

// ~~ PERCUSSION ~~
KICK_RING <PRD=4>: [0i9,9i0]x*(1,-1)s0.25
KICK_CRUNCHY <PRD=1, LOOP=F, SUS=T>: [9,-9]s<lead=B>SPD_KICK_SHORT
KICK_OCEAN <BASE=WV_SINE_OCEAN, LOOP=F, SUS=T>: WV_SINE_OCEANs<lead=B>SPD_KICK_SHORT

KICK_CRUNCHY_RING<BASE=KICK_CRUNCHY>: [KICK_CRUNCHYi<w=40>KICK_RING,KICK_RINGv[9i<w=2>0]]
KICK_OCEAN_RING<BASE=KICK_OCEAN>: [KICK_OCEANi<w=40>KICK_RING,KICK_RINGv[9i<w=2>0]]
