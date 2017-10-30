from ase.io import read
from aiida.orm.data.structure import StructureData

cif = StructureData(ase=read('TiO2.cif'))
print(cif.get_formula())
