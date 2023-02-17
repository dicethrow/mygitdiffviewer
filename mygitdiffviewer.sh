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

# get parent folder of this file, which needs to resolve the ld link, from https://stackoverflow.com/questions/59895/how-do-i-get-the-directory-where-a-bash-script-is-located-from-within-the-script
DIR=$(dirname -- "$( readlink -f -- "$0"; )")

# get path of the containing git repo
GITDIR=$(git rev-parse --show-toplevel)

$DIR/pythontest.py $DIR $GITDIR "$file1" "$file2" # quotes as the filenames may have spaces? yuck!

# firefox --new-window $file1 $file2

# want this to be all layers but I'm too lazy to type them all out
MOST_KICAD_LAYERS=F.Cu,In1.Cu,In2.Cu,In3.Cu,In4.Cu,B.Cu,B.Adhesive,F.Adhesive,B.Paste,F.Paste,B.Silkscreen,F.Silkscreen,B.Mask,F.Mask,User.Drawings,User.Comments,User.Eco1,User.Eco2,Edge.Cuts,Margin,B.Courtyard,F.Courtyard,B.Fab,F.Fab,User.1,User.2

for filename in $DIR/tempdir/*.kicad_pcb; do
	OUTPUTFORMAT=pdf
	RESULT=$filename.$OUTPUTFORMAT	
	kicad-cli pcb export $OUTPUTFORMAT --layers $MOST_KICAD_LAYERS --output $RESULT $filename
	rm $filename
done


found=0
for filename in $DIR/tempdir/*; do
	found=1
done
echo found_is_$found >> $DIR/app.log
if [[ $found == 1 ]]; then
	firefox --new-window $DIR/tempdir/*
else
	meld $file1 $file2
fi
