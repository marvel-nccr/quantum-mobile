"""Simple aiida-quantumespresso calculation script,
intended to be run with ``verdi run``.

The script attempts to be idempotent,
by checking if the calculation has already been run,
based on the label of the calculation node.
"""
import sys
import typing as t

from aiida import common, engine, orm
from ase.spacegroup import crystal

DEFAULT_CALC_LABEL = "qe.pw.mpi.si"


def si():
    """Return a ``StructureData`` representing an Si crystal."""
    alat = 5.43
    atoms = crystal(
        "Si",
        [(0, 0, 0)],
        spacegroup=227,
        cellpar=[alat, alat, alat, 90, 90, 90],
        primitive_cell=True,
    )
    return orm.StructureData(ase=atoms)


def run(args: t.List[str]) -> None:
    """Run a simple calculation."""
    label = args[0] if args else DEFAULT_CALC_LABEL
    try:
        node = orm.load_node(label=label)
        print(node)
        sys.exit(node.exit_status)
    except common.NotExistent:
        pass

    code = orm.Code.objects.get(label="qe.pw")
    structure = si()
    pseudo_family = orm.load_group("SSSP/1.1/PBE/efficiency")
    cutoff_wfc, cutoff_rho = pseudo_family.get_recommended_cutoffs(
        structure=structure, unit="Ry"
    )
    kpoints = orm.KpointsData()
    kpoints.set_kpoints_mesh([2, 2, 2])

    builder = code.get_builder()
    builder.metadata.options.resources = {"num_machines": 1}
    builder.metadata.options.withmpi = True
    builder.structure = structure
    builder.pseudos = pseudo_family.get_pseudos(structure=structure)
    builder.kpoints = kpoints
    builder.parameters = orm.Dict(
        {
            "CONTROL": {
                "calculation": "scf",
            },
            "SYSTEM": {
                "ecutwfc": cutoff_wfc,
                "ecutrho": cutoff_rho,
            },
        }
    )

    _, node = engine.run_get_node(builder)
    node.label = label
    print(node)
    sys.exit(node.exit_status)


if __name__ == "__main__":
    run(sys.argv[1:])
