#!/usr/bin/env bash
# 16feb2023

# this is meant to sub in place of something like meld

# currently, mainly for kicad 7 circuits

# assumptions
# - kicad 7 is installed
# - firefox is installed (as the .pdf/.svg viewer)
# - meld is installed, and was the previous default diff viewer

# future
# - instead of using pdf, use svg with this tool https://github.com/easyw/k-eediff
# 	- e.g.	firefox --new-window B-SCAN22-BASE-1.svg

file1=$1
file2=$2

firefox --new-window $file1 $file2

MOST_KICAD_LAYERS=F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,B.Adhesive,F.Adhesive,B.Paste,F.Paste,B.Silkscreen,F.Silkscreen,B.Mask,F.Mask,User.Drawings,User.Comments,User.Eco1,User.Eco2,Edge.Cuts,Margin,B.Courtyard,F.Courtyard,B.Fab,F.Fab,User.1,User.2

if [[ $file1 == *.kicad_pcb ]]; then
	OUTPUTFORMAT=pdf

	echo $file1

	kicad-cli pcb export $OUTPUTFORMAT --layers $MOST_KICAD_LAYERS $file1
	kicad-cli pcb export $OUTPUTFORMAT --layers $MOST_KICAD_LAYERS $file2

	firefox --new-window $file1.$OUTPUTFORMAT $file2.$OUTPUTFORMAT

else
	meld $file1 $file2
fi

