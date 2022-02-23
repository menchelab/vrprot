# alphafold_to_vrnetzer

Bringing structures predicted by AlphaFold (or .pdb files in general) to the VR Netzer visualization platform.

# our miro board

https://miro.com/app/board/o9J_lrYlqHM=/

# the ars electronica repository

https://github.com/menchelab/ArsE_Blender_Python/
Here you can find a python notebook which we used for converting ASCII files with coordinates to RGB (color) and XYZ (positions) images for the game engine
Folder with examples: https://github.com/menchelab/ArsE_Blender_Python/tree/main/ptclouds

# the project board in here

https://github.com/menchelab/alphafold_to_vrnetzer/projects/1
Here we can all add to dos, issues and things that would be nice to have. I already filled in a few, but of course everyone can add more if needed.

# getting started with git

In general I recommend getting a graphical git client like https://desktop.github.com/ or https://www.sourcetreeapp.com/ and then you can just clone this repository and always "commit, push, pull" until you run into merge conflicts or similar.

In case you are using visual studio code, git integration is also very well done there.

Gere is a cheat sheet by git if you want to know more
https://education.github.com/git-cheat-sheet-education.pdf

And of course, you can always send a mail if you have questions or issues.

And since I have now told you exactly what the comic says,
I will include it for reference: https://xkcd.com/1597/

# PDB Parser
#### Author: Till Pascal Oblau
## Requirements:
requests

pandas - only to read out excel sheet for testing

openpyxl - only to read out excel sheet for testing

An installation of ChimeraX

An installation of Blender

Operating systems: Linux and macOS.

You can import the class ChimeraXProcessing from pdb_parser.py
to parse a pdb file.

## Quickstart
### Use the easy_pipeline.py script
You can use the easy pipeline script to use the pdb parser and blender converter to generate .ply files from a UniprotID.
You have to start the script with the "-p" flag:

`python3 easy_pipeline.py -p <your list of proteins you want to process>`

A little Example:

`python3 easy_pipeline.py -p P08590,P38606,Q9W3H5`

If your ChimeraX or Blender installation can not be found, you can define 
the execution paths for your system. With the use of the "-ch_path="
flag you can define your ChimeraX execution path. 

Example:

`python3 easy_pipeline.py -p P08590,P38606,Q9W3H5 -ch_path="<path to your ChimeraX executable>"`

`python3 easy_pipeline.py -p P08590,P38606,Q9W3H5 -ch_path="/Applications/ChimeraX-1.3-rc2021.12.01.app/Contents/MacOS/ChimeraX"`

With the "-bl_path=" flag you can define your Blender
execution path.

Example:

`python3 easy_pipeline.py -p P08590,P38606,Q9W3H5 -bl_path="<path to your Blender executable>"`

`python3 easy_pipeline.py -p P08590,P38606,Q9W3H5 -bl_path="/Applications/Blender.app/Contents/MacOS/Blender"`

### Run modul_test.py

This will fetch some pdbs from the AlphaFold DB, color code the secondary structure 
and output .ply file containing the 3D model with vertex colors. 
Warning: It will process all .glb files contained in the glbs directory!

If it cannot find your ChimeraX installation, you can use the 
"ch_path=" argument if you start the script, e.g.

`python3 modul_test.py -ch_path="<path to your ChimeraX executable>"`

`python3 modul_test.py -ch_path="/Applications/ChimeraX-1.3-rc2021.12.01.app/Contents/MacOS/ChimeraX"`

Same for the Blender installation, you can use the "bl_path=" argument if you start the script, e.g.

`python3 modul_Test.py -bl_path="<path to your Blender executable>"`

`python3 modul_test.py -bl_path="/Applications/Blender.app/Contents/MacOS/Blender"`

## Create a Protein object with:
```
from pdb_parser import ChimeraXProcessing

pdb_parser = ChimeraXProcessing(protein={"P38606":"P38606"}, keepFiles = True/False)

```
The protein dictionary contains all the protein structures you want to process.
You can add a new structure by using:
```
pdb_parser.add_protein(<UniProtID>)
```

The keepFiles argument can be used, to tell the program, to not delete pdb and 
glb file after the proccessing is accomplished.

## Fetch the pdb
```
pdb_parser.fetch_pdb(protein)
```

This will download the pdb file from the AlphaFold DB if available. This will be saved in a subfolder called "./pdbs/".

If the structure is not available on the AlphaFold DB it will try to download it from the RCSB database. If the strucutre is also not available here, it will report it to you.

## Color the secondary structures
You can define the installtion Path to you ChimeraX installtion by using:

```
# For Linux (default))
pdb_parser.ChimeraX = "chimerax"
# For Mac
pdb_parser.ChimeraX = "/Applications/<ChimeraX_Version>.app/Contents/MacOS/ChimeraX"
```

Then you should be able to use:

```
pdb_parser.color_ss_chimerax(portein,colors=["red", "green", "blue"]) # color argument is optional (Coil = "red", Helix = "green", Strand = "blue")
```

This will open Chimerax, select the secondary structures and color them as asked.

It will save the results as a .glb file.

## Convert .glb with colors to .ply file
```
from blender_converter import BlenderConverter

blender_parser = BlenderConverter(
                structures={"P04439":"P04439.glb"},
                keepFiles=self.keepFiles)

```
The structure dictionary called "structures" contains all the path to the .glb files of the proteins you want to process.
You can add a new structure (as path to a .glb file ) by using:

```
blender_parser.add_structure(<UniProtID>, <Path to Structure>)
```

The "keepFiles" argument can be used, to tell the program to not delete .glb and other source files after the proccessing is accomplished.

## Export the .ply file
You can define the installtion Path to your blender installtion by using:

```
# For Linux (default))
blender_parser.blender = "blender"
# For Mac
blender_parser.blender = "/Applications/Blender.app/Contents/MacOS/Blender"
```

The .ply file can be converted and exported by using:

```
blender_parser.convertToPly(protein)
```
The Output can then be found in the ./plys/ directory.

# Create the PointCloud
#### Author: Felix Fischer
## Requires python library open3d
run sample_pcd.py (specify name of input .ply object in code). To normalize coordinates, import "Cube.ply" and Cube_no_lines.ply (.ply format of cube based on cube.fbx)
This will sample a point cloud from .ply mesh and store it as .xyzrgb file. Scaling of protein may fail (exceed cube) for very unsymmetric proteins.

# Create .png files
#### Author: Felix Fischer
The resulting point cloud from previous script is in xyzrgb format, rbg values are stored as float value between [0,1].
To create the .png files, run run_pointcloud2map_xyzrgb.py.

