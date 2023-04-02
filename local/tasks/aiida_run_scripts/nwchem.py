"""Simple aiida-nwchem calculation script,
intended to be run with ``verdi run``.

The script attempts to be idempotent,
by checking if the calculation has already been run,
based on the label of the calculation node.
"""
import sys
import typing as t

from aiida import common, engine, orm
from ase.build import molecule

DEFAULT_CALC_LABEL = "nwchem.main.mpi.h20"


def h2o():
    """Return a ``StructureData`` representing a water molecule."""
    atoms = molecule("H2O", vacuum=10)
    atoms.pbc = (True, True, True)
    structure = orm.StructureData(ase=atoms)
    return structure


def run(args: t.List[str]) -> None:
    """Run a simple calculation."""
    label = args[0] if args else DEFAULT_CALC_LABEL
    try:
        node = orm.load_node(label=label)
        print(node)
        sys.exit(node.exit_status)
    except common.NotExistent:
        pass

    code = orm.Code.objects.get(label="nwchem.main")
    builder = code.get_builder()
    builder.metadata.options.resources = {"num_machines": 1}
    builder.metadata.options.withmpi = True
    builder.structure = h2o()
    builder.parameters = orm.Dict(
        dict=dict(task="dft", basis={"H": "library sto-3g", "O": "library sto-3g"})
    )
    builder.add_cell = orm.Bool(True)

    _, node = engine.run_get_node(builder)
    node.label = label
    print(node)
    sys.exit(node.exit_status)


if __name__ == "__main__":
    run(sys.argv[1:])
