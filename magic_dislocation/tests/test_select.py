"""Test operations's select module.

In this module, we will test the functions in io module with multiple cases.

Typical usage example:
"""

# import os
# import sys

# import ase

# sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from magic_dislocation.io.ase_io import ase_read, ase_write

class BaseIOTester:
    def __init__(self):
        pass

    def test_read(self):
        pass

    def test_write(self):
        pass

class AseIOTester(BaseIOTester):
    """
    A class for testing input/output operations using the ASE library.
    """

    def __init__(self, config):
        self.config = config

    def test_read(self, reader="ase"):
        """
        Test the read operation using the specified reader.

        Args:
            reader (str, optional): The reader to use. Defaults to "ase".
        """
        if reader == "ase":
            results = ase_read(**self.config) # Atoms type
        else:
            raise ValueError("Reader not supported")
        self.config["images"] = results

    def test_write(self, writer="ase"):
        """
        Test the write operation using the specified writer.

        Args:
            writer (str, optional): The writer to use. Defaults to "ase".
        """
        self.config["filename"] += ".test"
        self.config["masses"] = True
        self.config["velocities"] = True
        ase_write(**self.config)        
        if writer == "ase":
            ase_write(**self.config)
        else:
            raise ValueError("Writer not supported")

    def run(self):
        """
        Run the test by calling the test_read and test_write methods.
        """
        self.test_read()
        self.test_write()

config = {}
file_name = r'/Users/shaowei/Desktop/Codes4Shihuama/MagicDislocation_v1/examples/fcc/s350_16_112/model.data'
config = {"filename": file_name,
          "format": "lammps-data",
          "atom_style": "atomic",
          }
tester = AseIOTester(config)
tester.run()