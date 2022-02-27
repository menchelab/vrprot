# alphafold_to_vrnetzer

# Quickstart
#### Authors: Felix Fischer and Till Pascal Oblau
### Use the easy_pipeline.py script
You can use the easy pipeline script to use the PDB parser and Blender Converter
to generate .ply files from a UniProtID. These PLY files will then be used to
sample a Point Cloud. As final output two PNG files are generated, containing
the RGB and XYZ values of the points in the Point cloud.

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

The Easy pipeline will not delete the temporal files generated during the process.
### Run modul_test.py
#### Author: Till Pascal Oblau
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

# PDB Parser
#### Author: Till Pascal Oblau
## Requirements:
### Python modules
 - requests

 - pypng

 - pandas - only to read out excel sheet for testing

 - openpyxl - only to read out excel sheet for testing

#### Other requirments
 - An installation of ChimeraX

 - An installation of Blender

 - Operating systems: Linux and macOS.

You can import the class ChimeraXProcessing from pdb_parser.py
to parse a PDB file.

## Create a Protein object with:
```
from pdb_parser import ChimeraXProcessing

pdb_parser = ChimeraXProcessing(protein={"P38606":"P38606"}, keepFiles = <True/False>)

```
The protein dictionary contains all the protein structures you want to process.
You can add a new structure by using:
```
pdb_parser.add_protein(<UniProtID>)
```

The keepFiles argument can be used, to tell the program, to not delete PDB and 
GLB file after the proccessing is accomplished.

## Fetch the PDB
```
pdb_parser.fetch_pdb(protein)
```

This will download the PDB file from the AlphaFold DB if available. This will be saved in a subfolder called "./pdbs/".

If the structure is not available on the AlphaFold DB it will try to download it from the RCSB database. If the structure is also not available here, it will report it to you.

## Color the secondary structures
You can define the installation Path to your ChimeraX installation by using:

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

The "keepFiles" argument can be used, to tell the program to not delete .glb and other source files after the proccessing is accomplished.<br>
The output can then be found in the "./glbs/ "directory.

## Export the .ply file
You can define the installation Path to your blender installation by using:

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
The output can then be found in the ./plys/ directory.

# Create the PointCloud
#### Author: Felix Fischer
## Requires python library open3d
run sample_pcd.py (specify name of input .ply object in code). To normalize coordinates, import "Cube.ply" and Cube_no_lines.ply (.ply format of cube based on cube.fbx)
This will sample a point cloud from .ply mesh and store it as .xyzrgb file. Scaling of protein may fail (exceed cube) for very unsymmetric proteins.

# Create .png files
#### Author: Felix Fischer
The resulting point cloud from previous script is in xyzrgb format, rbg values are stored as float value between [0,1].
To create the .png files, run run_pointcloud2map_xyzrgb.py.

