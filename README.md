# mygitdiffviewer
This is so I can filter out which program to view/handle diffs from gitk's view diff button.



Status:
Not working. 
gitk passes arguments like this, not the filename as expected:

file:///home/x/Documents/git_repos/general/general_electronics/.git/modules/modules/2022/M-CAM-OV5640/.gitk-tmp.YrWprd/2/[a72fd759b4996a38570a67b465d987220135189e]

not sure what to do, pausing work.


# Installation

Make these scripts executable
``` bash
sudo chmod +x mygitdiffviewer.sh
sudo chmod +x pythontest.py
```

Do this once, so the executable will link to the script in the other file

``` bash
ln -s ./mygitdiffviewer.sh ~/.local/bin/mygitdiffviewer 
```

You can check this with

``` bash
ls -al ~/.local/bin | grep mygitdiffviewer
```