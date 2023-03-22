# About this resource

This archive contains the processed human proteome in two visualizations styles:

1. Cartoon style with the secondary structures colored (loop regions red, helices green, β-sheets blue)
2. Surface style with the electrostatic potential colored (red negative, white neutral, blue positive electrostatic potential).

Currently only one of these packages can be used at a time. The scale of each structure and the respective visualization is listed in the `overview.csv` file, however, the scale is currently not used.

# Adding the protein structures to the VRNetzer backend

1. Download one of the two .zip archives
2. extract the "MAPS" directory contained in the archive /<visualization style>/
   to the static directory of the VRNetzer backend (e.g. "/static/MAPS")
3. Place the `overview.csv` file to the "/static/csv/" directory of the VRNetzer backend (e.g. "/static/csv/overview.csv")
4. The respective structure of a protein in a Network which is annotated with UniProt IDs can now be visualized by using the designated tab on the node panel of the VRNetzer UI.

# Annotated a network with UniProt IDs

All STRING networks exported with the VRNetzerApp from Cytoscape are already annotated with UniProt IDs.

To annotate you own network, the respective UniProt IDs have to be added to the `nodes.json` file of the respective VRNetzer project. Each node for which a UniProt ID is know can be annotated like this:

```
{
    "id": 0,
    ...
    "other_annotation": "some_annotation_value",
    "uniprot": ["P08582"],
    ...
 }
```

The UniProt ID has to be in an array of strings, even if only one UniProt ID is known.
Once annotated the respective protein structure can be loaded using the designated tab on the node panel of the VRNetzer UI.

# Additional visualization styles and structures

To produce your own protein structure visualiation you can use the [`vrprot`](https://pypi.org/search/?q=vrprot). The [ProteinStructureFetch](https://github.com/menchelab/ProteinStructureFetch) VRNetzer extension allows to process structures on demand in one of 37 available visualization styles.

# Update to new AlphaFold Version

As soon as a new version of the AlphaFold database is released, the available preprocessed structures will be updated to the newest version. Also the vrprot and ProteinStructureFetch extensions will be updated to the newest version to allow the processing of the newest AlphaFold structures.

# License

MIT License
