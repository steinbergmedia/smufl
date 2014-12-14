#! /usr/bin/env python

# Minimal SMuFL meta data generator for FontForge.
# The script must be invoked from within the font's directory
# Only the font's default settings and the bounding boxes
# are exported for now (anchors and such can be added in the future...)
# Written by Robert P. - poeticprocessing 2014

import fontforge
import sys
import os
import json

nargs = len(sys.argv)
if nargs != 2:
    print ( "Oops... Font file name missing!" )
    sys.exit (1)
    
fontFileName = sys.argv[1]
fontName = os.path.splitext(fontFileName)[0]
path = fontFileName
try:
    font = fontforge.open(path)
except EnvironmentError:
    print ( "Aargh... Error opening font file %s!" % fontFileName)
    sys.exit (1)

fontVersion = font.version
metadata = {'fontName': fontName, 'fontVersion': fontVersion}

print ("Generating %s SMuFL minimal metadata..." % (fontFileName) )

#customize these values if necessary:
engravingDefaults = {
    'arrowShaftThickness': '0.16',
    'barlineSeparation': '0.4',
    'beamSpacing': '0.25',
    'beamThickness': '0.5',
    'bracketThickness': '0.5',
    'dashedBarlineDashLength': '0.5',
    'dashedBarlineGapLength': '0.25',
    'dashedBarlineThickness': '0.16',
    'hairpinThickness': '0.16',
    'legerLineExtension': '0.4',
    'legerLineThickness': '0.16',
    'lyricLineThickness': '0.16',
    'octaveLineThickness': '0.16',
    'pedalLineThickness': '0.16',
    'repeatBarlineDotSeparation': '0.16',
    'repeatEndingLineThickness': '0.16',
    'slurEndpointThickness': '0.1',
    'slurMidpointThickness': '0.22',
    'staffLineThickness': '0.13',
    'stemThickness': '0.12',
    'subBracketThickness': '0.16',
    'textEnclosureThickness': '0.16',
    'thickBarlineThickness': '0.5',
    'thinBarlineThickness': '0.16',
    'tieEndpointThickness': '0.1',
    'tieMidpointThickness': '0.22',
    'tupletBracketThickness': '0.16'}
    
metadata["engravingDefaults"] = engravingDefaults

glyphBBoxes = dict()
count = 0
started = False
for glyph in font:
    g = font[glyph]
    if g.unicode != -1:
        count += 1
        g.addExtrema();
        bbox = g.boundingBox();
        bBoxNE = (round(bbox[2]/250., 3), round(bbox[3]/250.,3) )
        bBoxSW = (round(bbox[0]/250., 3), round(bbox[1]/250.,3) )
        glyphBBoxes[g.glyphname] = {'bBoxNE':bBoxNE, 'bBoxSW':bBoxSW}

print ( "%d defined glyphs processed." % (count) )

metadata["glyphBBoxes"] = glyphBBoxes
output = json.dumps(metadata, sort_keys=True, indent=4, separators=(',', ': '))
#print(output)

jsonFileName = fontName.lower() + "_metadata.json"
outfile = open(jsonFileName, "w")
outfile.write(output)
outfile.close()