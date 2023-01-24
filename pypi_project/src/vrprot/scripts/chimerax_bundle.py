# Author: Till Pascal Oblau
import argparse
import os
import sys

from chimerax.core.commands import run


class Bundle:
    """
    Object to be run as python script during chimeraX runtime.
    """

    def __init__(self, session, path, target, images=None):
        """
        Initialization of the Bundle Class. Will define the chimeraX session
        which is needed by the ChimeraX api and will define the colors for the
        color coding.

        Args:
            session (chimerax.session): Defines ChimeraX process
            colors (list, string): List of strings. Contains which colors each selection will be colored.
        """
        self.session = session
        self.wd = os.path.abspath(".")
        self.target = target
        self.images = images
        self.pipeline = ["N/A"]
        run(self.session, f"cd {path}")

    ## Utility
    def open_file(self, structure):
        "Open structure"
        self.pipeline[0] = f"open {structure}"

    def run_pipeline(self, structure):
        """
        Function to executed the pipeline and save the file as glb
        """
        file_name = structure[:-3]
        save_loc = f"{self.target}/{file_name}glb"
        if self.images:
            self.take_screenshot(file_name)
        self.pipeline[-2] = f"save {save_loc}"
        for command in self.pipeline:
            run(self.session, f"echo {command}")
            run(self.session, command)

    ## display modes
    def change_display_to(self, mode: str):
        """
        Changes display mode to only show the desired display.
        Possible display modes: "atoms", "cartoons", or "surface".
        """
        modes = ["atoms", "cartoons", "surface"]
        # TODO: cartoons translates to show sel\xa0cartoons dunno why tho.
        for m in modes:
            if m == mode:
                self.pipeline.extend(["sel", f"show sel {m}"])
            else:
                self.pipeline.extend(["sel", f"hide sel {m}"])

    def change_style_to(self, style):
        """
        Changes style mode to only show the desired style.
        Possible style modes: "stick", "sphere", or "ball".
        """
        styles = ["stick", "sphere", "ball"]
        self.change_display_to("atoms")
        for s in styles:
            if s == style:
                self.pipeline.extend([f"style sel {s}"])

    ## Coloring modes
    def ss_coloring(self, colors):
        """
        Add color coding of secondary structures.
        """
        if colors is None:
            colors = ["red", "green", "blue"]
        self.pipeline.extend(
            [
                "select coil",
                "color sel " + colors[0],
                "select helix",
                "color sel " + colors[1],
                "select strand",
                "color sel " + colors[2],
            ]
        )

    def rainbow_coloring(self):
        """
        Add rainbow coloring.
        """
        self.pipeline.extend(["sel", "rainbow sel"])

    def heteroatom_coloring(self):
        """
        Add heteroatom coloring.
        """
        self.pipeline.extend(["sel", "color sel byhetero"])

    def chain_coloring(self):
        """
        Add chain coloring.
        """
        self.pipeline.extend(["sel", "color sel bychain"])

    def polymer_coloring(self):
        """
        Add polymer coloring.
        """
        self.pipeline.extend(["sel", "color sel bypolymer"])

    def electrostatic_coloring(self):
        """
        Add electrostatic coloring.
        """
        self.pipeline.extend(["sel", "coulombic sel"])
        self.change_display_to("surface")

    def hydrophobic_coloring(self):
        """
        Add hydrophobic coloring.
        """
        self.pipeline.extend(["sel", "mlp sel"])
        self.change_display_to("surface")

    def bFactor_coloring(self):
        """
        Add hydrophobic coloring.
        """
        self.pipeline.extend(["sel", "color bfactor sel"])

    def nucleotide_coloring(self):
        """
        Add hydrophobic coloring.
        """
        self.pipeline.extend(["sel", "color sel bynucleotide"])

    def mfpl_coloring(self):
        """
        Add Max F Perutz Lab coloring.
        """
        self.pipeline.extend(["sel", "color sel #00cac0"])

    ## Complete processes
    def mode_ss_coloring(self, colors, mode):
        """
        Will color the secondary structures of the protein according to the specified colors, if colors are None, colors will be red, green, blue for coil, helix, and strand respectivley. Desired display mode is set.
        """
        self.change_display_to(mode)
        self.ss_coloring(colors)

    def mode_rainbow_coloring(self, mode):
        """
        Will color the protein structure using the rainbow coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.rainbow_coloring()

    def mode_heteroatom_coloring(self, mode):
        """
        Will color the protein structure using the heteroatom coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.heteroatom_coloring()

    def mode_chain_coloring(self, mode):
        """
        Will color the protein structure using the chain coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.chain_coloring()

    def mode_polymer_coloring(self, mode):
        """
        Will color the protein structure using the polymer coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.polymer_coloring()

    def mode_electrostatic_coloring(self, mode):
        """
        Will color the protein structure using the electrostatic coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.electrostatic_coloring()

    def mode_bFactor_coloring(self, mode):
        """
        Will color the protein structure using the b-factor coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.bFactor_coloring()

    def mode_nucleotide_coloring(self, mode):
        """
        Will color the protein structure using the nucleotide coloring of chimeraX and the desired display mode.
        """
        self.change_display_to(mode)
        self.nucleotide_coloring()

    def mode_mfpl_coloring(self, mode):
        """Will color the protein structures in the Max Ferdinand Perutz Labs turquoise.
        Args:
            mode (str): Display mode to use.
        """
        self.change_display_to(mode)
        self.mfpl_coloring()

    def take_screenshot(self, structure):
        """
        Takes a screenshot of the current scene and saves it to the specified path.
        """
        unselect = "~select"
        view = "view"
        save = f"save {self.images}/{structure}png width 512 height 512 supersample 3 transparentBackground true"
        select = f"select"
        self.pipeline = (
            self.pipeline[:-2] + [unselect, view, save, select] + self.pipeline[-2:]
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--source",
        help="Path to the directory containing the protein files.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-d",
        "--dest",
        help="Path to the directory where the glbs will be saved.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-i",
        "--images",
        help="Path to the directory where the images will be saved.",
        required=False,
        default=None,
        type=str,
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Mode to use for coloring the protein.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-fn",
        "--filenames",
        help="Names of the files to be processed.",
        required=False,
        type=str,
    )
    parser.add_argument(
        "-cl",
        "--colors",
        help="Colors to use for coloring the protein.",
        required=False,
        nargs="*",
        type=str,
    )
    args = parser.parse_args()
    path = args.source
    file_names = args.filenames.split(",")
    bundle = Bundle(session, args.source, args.dest, args.images)
    cases = {
        "ss": bundle.mode_ss_coloring,
        "rainbow": bundle.mode_rainbow_coloring,
        "heteroatom": bundle.mode_heteroatom_coloring,
        "polymer": bundle.mode_polymer_coloring,
        "chain": bundle.mode_chain_coloring,
        "electrostatic": bundle.electrostatic_coloring,
        "hydrophobic": bundle.hydrophobic_coloring,
        "bFactor": bundle.mode_bFactor_coloring,
        "nucleotide": bundle.mode_nucleotide_coloring,
        "mfpl": bundle.mode_mfpl_coloring,
    }
    mode, coloring, _ = args.mode.split("_")
    style = None
    if mode in ["stick", "sphere", "ball"]:
        style = mode
        mode = "atoms"

    if coloring == "ss":
        """
        This part will be executed, if the argument is ss_coloring, i.e. coloring the secondary structures.
        """
        colors = args.colors
        cases[coloring](colors, mode)
        if style is not None:
            bundle.change_style_to(style)
    elif coloring in ["electrostatic", "hydrophobic"]:
        cases[coloring]()

    else:
        # General coloring cases
        cases[coloring](mode)
        if style is not None:
            # if mode was ["stick", "sphere", "ball"] atoms is the new mode and style is one out of ["stick", "sphere", "ball"]
            bundle.change_style_to(style)
    if args.images is not None:
        run(session, "lighting soft")
        run(session, "lighting shadows false")
    bundle.pipeline.extend(["save", "close"])

    for structure in list(file_names):
        run(session, f"echo {structure}")
        bundle.open_file(os.path.join(path, structure))
        bundle.run_pipeline(structure)
    # Close ChimeraX
    run(bundle.session, "exit")


# "ChimeraX_sandbox_1" seems to be the default name for a script but did not work
# if __name__ == "ChimeraX_sandbox_1":


main()
