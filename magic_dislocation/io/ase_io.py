"""A io module based on ase.

In this module, we define a io module based on ase, containing necessay configs, 
functions for reading data, parsing data and writing data.

  Typical usage example:

"""


from ase.io import read, write


def ase_read(filename, **kwrags):
    """Read data from a file.

    Args:
        filename (str): The name of the file.

    Returns:
        atoms: An ase.Atoms object.

    """
    atoms = read(filename, **kwrags)
    return atoms


def ase_write(filename, **kwargs):
    """Write data to a file.

    Args:
        file_name: The name of the file.
        atoms: An ase.Atoms object.

    Returns:
        writen atoms

    """
    atoms = write(filename, **kwargs)
    return atoms