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
open3d

An installtion of ChimeraX

An installation of Blender

You can import the class ChimeraX_processing from pdb_parser.py to parse a pdb file.

## Quickstart
### Use the easy_pipeline.py script
You can use the easy pipeline script to use the pdb parser and blender converter to generate .ply files from a UniprotID. Simply start the script with the -p operator:

`python3 easy_pipeline.py -p <your list of proteins you want to process>`

A little Example:

`python3 easy_pipeline.py -p P08590,P38606,Q9W3H5`

### Run modul_Test.py

This will fetch the some pdbs from the AlphaFold DB, colorcode the secondary structure and output an .glb file cotaining the 3D model with vertexcolors.

If it cannot find you Chimerax insalltion you can use the "ch_path=" argument if you start the script, e.g.

`python3 modul_Test.py ch_path="\"<path to your Chimerax.exe>\""`

`python3 modul_Test.py ch_path="\"F:/Program Files/ChimeraX 1.2.5/bin/ChimeraX.exe\""`

Same for the Blender installtion, you can use the "bl_path=" argument if you start the script, e.g.

`python3 modul_Test.py bl_path="\"<path to your Blender.exe>\""`

## Create a Protein object with:

```
from pdb_parser import ChimeraX_processing

pdb_parser = ChimeraX_processing(protein={"P38606":"P38606"}, keepFiles = True/False)

```
The protein dict contains all the protein structures you want to process. You can addd a new structure by using:
```
pdb_parser.add_protein(<UniProtID>)
```

The keepFiles argument can be used to tell the program to not delete pdb and glb file after the proccessing is accomplished.

## Fetch the pdb

```
pdb_parser.fetch_pdb(protein)
```

This will download the pdb file from the AlphaFold DB if available. This will be saved in a subfolder called "./pdbs/".

If the structure is not available on the AlphaFold DB it will try to download it from the RCSB database. If the strucutre is also not available here, it will report it to you.

## Color the secondary structures

You can define the Installtion Path to you ChimeraX installtion by using:

```
# For Linux (standard)
pdb_parser.ChimeraX = "chimerax"
# For Windows
pdb_parser.ChimeraX = "\"<Path to ChimeraX.exe\""
# For Mac
pdb_parser.ChimeraX = "<Path to your ChimeraX application>"
```

Than you should be able to use:

```
pdb_parser.color_ss_chimerax(portein,colors=["red", "green", "blue"]) # color argument is optional (Coil = "red", Helix = "green", Strand = "blue")
```

This will open Chimerax, select the secondary structures and color them as ask.

It will save the results as a .glb file and a .png file containing the texture.

## Bake .glb with texture file to .ply file

```
from blender_converter import BlenderCovert

blender_parser = BlenderConvert(
                strucutres={"P04439":"P04439.glb"},
                keepFiles=self.keepFiles)

```
The structure dict contains all the .glb files protein you want to process. You can addd a new structure with texture by using:

```
blender_parser.add_structure(<UniProtID>, <Path to Structure>)
```

The keepFiles argument can be used to tell the program to not delete .glb and other
source files after the proccessing is accomplished.

## Bake the .ply file

The .ply file can be baked by using:

```
blender_parser.combineBake(protein)
```
The Output can than be found in the ./pdb/ directory.

## Create the PointCloud
run sample_pcd.py (specify name of input .ply object in code). To normalize coordinates, import "Cube.ply" and Cube_no_lines.ply (.ply format of cube based on cube.fbx)
This will sample a point cloud from .ply mesh and store it as .xyzrgb file. Scaling of protein may fail (exceed cube) for very unsymmetric proteins.

## Create .png files
The resulting point cloud from previous script is in xyzrgb format, rbg values are stored as float value between [0,1].
To create the .png files, run run_pointcloud2map_xyzrgb.py.

