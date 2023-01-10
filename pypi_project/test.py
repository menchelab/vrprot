from sys import argv

from src.vrprot.pointcloud2map_8bit import pcd_to_png
from src.vrprot.sample_pointcloud import sample_pcd
from src.vrprot.util import (
    ColoringModes,
    convert_glb_to_ply,
    fetch_pdb_from_alphafold,
    run_chimerax_coloring_script,
    search_for_chimerax,
)


def test_alphafold_fetch():
    protein = "A0A0A0MRZ8"
    output = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/pdbs/"
    fetch_pdb_from_alphafold(protein, output, "v2")


def test_chimerax_process():
    src = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/pdbs"
    output = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/glbs"
    chimerax = search_for_chimerax()
    run_chimerax_coloring_script(
        chimerax,
        src,
        ["AF-A0A0A0MRZ8-F1-model_v2.pdb"],
        output,
        ColoringModes.cartoons_ss_coloring.value,
        ["red,green,blue"],
    )


def test_glb_ply_convert():
    src = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/glbs/AF-A0A0A0MRZ8-F1-model_v2.glb"
    output = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/plys/AF-A0A0A0MRZ8-F1-model_v2.ply"
    print("testing convert")
    convert_glb_to_ply(src, output)


def text_sample_pcd(debug=False):
    source = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/plys/AF-A0A0A0MRZ8-F1-model_v2.ply"
    output = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/ASCII_clouds/AF-A0A0A0MRZ8-F1-model_v2.xyzrgb"
    sample_pcd(source, output=output, SAMPLE_POINTS=256 * 256, debug=debug)


def test_ascii_to_png():
    src = "/Users/till/Documents/Playground/VRNetzer_Backend/extensions/ProteinStructureFetch/processing_files/ASCII_clouds/AF-A0A0A0MRZ8-F1-model_v2.xyzrgb"
    png = "AF-A0A0A0MRZ8-F1-model_v2.png"
    bmp = png.replace("png", "bmp")
    rgb = "/Users/till/Documents/Playground/VRNetzer_Backend/static/NewMaps/rgb/" + png
    xyz_high = (
        "/Users/till/Documents/Playground/VRNetzer_Backend/static/NewMaps/xyz/high/"
        + bmp
    )
    xyz_low = (
        "/Users/till/Documents/Playground/VRNetzer_Backend/static/NewMaps/xyz/low/"
        + bmp
    )

    pcd_to_png(src, rgb, xyz_low, xyz_high, img_size=256)


test_alphafold_fetch()
test_chimerax_process()
test_glb_ply_convert()
text_sample_pcd()
test_ascii_to_png()
