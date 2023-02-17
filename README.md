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

# Notes

this command saved that file at that sha to a file
```
git --no-pager --git-dir /home/x/Documents/git_repos/general/general_electronics/.git/modules/modules/2022/M-CAM-OV5640 show 3b3d07fee13f4fd7141db379282c73d263ffc48e:v1.kicad_pcb > v1
```

this prints the commit
```
git --no-pager --git-dir /home/x/Documents/git_repos/general/general_electronics/.git/modules/modules/2022/M-CAM-OV5640 show 09abd80919a10a42b1eb6be66258197e8cc298c6
```