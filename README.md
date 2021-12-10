# alphafold_to_vrnetzer

bringing structures created with alphafold (or .pdb files in general) to the vrnetzer visualisation platform

# our miro board

https://miro.com/app/board/o9J_lrYlqHM=/

# the ars electronica repository

https://github.com/menchelab/ArsE_Blender_Python/
Here you can find a pyhton notebook which we used for converting ascii files with coordinates to rgb (color) and xyz (postions) images for the game engine
Folder with examples: https://github.com/menchelab/ArsE_Blender_Python/tree/main/ptclouds

# the project board in here

https://github.com/menchelab/alphafold_to_vrnetzer/projects/1
Here we can all add to dos, issues and things that would be nice to have. I already filled in a few but of course everyone can add more if needed.

# getting started with git

in general I recommend getting a graphical git client like https://desktop.github.com/ or https://www.sourcetreeapp.com/ and then you can just clone this repository and always "commit, push, pull" until you run into merge conflicts or similar.

In case you are using visual studio code, git integration is also very well done there.

here is a cheat sheet by git if you want to know more
https://education.github.com/git-cheat-sheet-education.pdf

And of course you can always send a mail if you have questions or issues.

And since I have now told you exactly what the comic says I will include it for reference: https://xkcd.com/1597/

# PDB Parser

### Requirements:

requests

pandas - only to read out excel sheet for testing

openpyxl

An installtion of ChimeraX


You can import the class Protein_structure from pdb_parser to parse a pdb file.

## Qucikstart

Run pdb_parser.py

This will fetch the pdb for P04439 from the AlphaFold DB, colorcode the secondary structure and output an .obj file cotaining the 3D model and a .png texture file.

If it cannot find you Chimerax insalltion you can use the "path=" argument if you start the script, i.e.

`python3 pdb_parser.py path="\"<path to your Chimerax.exe>\""`

`python3 pdb_parser.py path="\"F:/Program Files/ChimeraX 1.2.5/bin/ChimeraX.exe\""`

### Create a Protein object with:

```
from pdb_parser import Protein_structure

protein = Protein_structure("<UniProt ID of the Protein", proteinName="<optional: name of the Protein", keepPDB = True/False)

```

The keepPDB argument can be used to tell the program to not delet the PDB file after the proccessing is accomplished.

### You can than fetch the pdb by using:

```
protein.fetch_pdb()
```

This will download the pdb file from the AlphaFold DB if available. This will be saved in a subfolder called "./pdbs".

If the structure is not available on the AlphaFold DB it will return a Error message.

### You can than color the secondary structures by using:

You can define the Installtion Path to you ChimeraX installtion by using:

```
# For Linux (standard)
protein.ChimeraX = "chimerax"
# For Windows
protein.ChimeraX = "\"<Path to ChimeraX.exe\""
# For Mac
protein.ChimeraX = "<Path to your ChimeraX application>"
```

Than you should be able to use:

```
protein.color_ss_chimerax(colors=["red", "green", "blue"]) # color argument is optional (Coil = "red", Helix = "gree", Strand = "blue")
```

This will open Chimerax, select the secondary structures and color them as ask.

It will save the results as a .obj file and a .png file containing the texture.
