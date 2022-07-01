# alphafold_to_vrnetzer

# Quickstart
#### Authors: Felix Fischer and Till Pascal Oblau
## Requirements:
### Python modules
 - requests

 - pypng

 - open3d

 - numpy

 - trimesh

#### Other requirments
 - An installation of ChimeraX

 - Operating systems: Linux and macOS.
### Process a single structure
```./main.py fetch O95352```<br>
This will fetch the structure of O95352 from the AlphaFold database and
processes it using the pipeline. As coloring the secondary structures are
colored in red, green and blue.

### Get help
To get an overview of the available commands, use the `--help` command.<br>
```./main.py --help```

# PDB Parser
#### Author: Till Pascal Oblau

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

To convert a GLB file to PLY you can use the convertGLBToPLY function of the
ChimeraXProcessing class. You can simply call the function together with the
UniProtID of the respective protein. You can then use:
```
pdb_parser.convertGLPToPly(<UniProtID>)
```
This will convert the GLB file, which has been processed beforehand,
to a PLY file.
#### TODO Remove this part as Blender is not used anymore in the easy pipeline 
You can import the class BlenderCoverter from blender_converter.py
to parse a convert .glb files to .ply files.

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
# sample_pointcloud.py
#### Author: Felix Fischer
## Requires python library open3d
## Requires "Cube_no_lines.ply" in base folder of script.
This script will import the protein mesh (requires uniport ID of protein as input) and the mesh "Cube_no_lines.ply". The cube mesh (based on "Cube.fbx") is used for normalization of coordinate space of protein-mesh. The protein-mesh will be translated to the center coordinates of the cube-mesh and scaled to approximately the size of the cube-mesh. The two meshes will then be merged and a point cloud is sampled (1048576 points sampled) and stored as ASCII file in /ASCII_clouds (will create folder if it does not exist).

# Create .png files
# pointcloud2map
#### Author: Felix Fischer
## Requires python library PyPNG, numpy
This script opens the ASCII cloud of protein (requires uniport ID of protein as input) from ASCII_clouds foler, reads and stores the xyz coordinates and rgb value for each point in the point cloud in a seperate matrix, which is then converted in to two PNG files of size 1024x1024. The resulting PNG maps are stored in /MAPS/xyz and /MAPS/rgb (will create folder if it does not exist).
