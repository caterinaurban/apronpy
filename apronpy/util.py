from ctypes import CDLL
from os import environ
from pathlib import Path


ENV_VAR = 'APRON_LD_PATH'

def find_apron_library(name: str) -> str:
	"""
	Find the Apron library with the given name.

	Usually, calling CDLL(name) is enough to find the library, but sometimes
	there are issues with the library path. This function tries to find the
	library in the directory specified by ENV_VAR
	variable.

	Args:
		name (str): The name of the Apron library, e.g. "libapron.so".

	Returns:
		str: The path to the found Apron library. CDLL(path) should work
		then.

	Raises:
		OSError: If the Apron library cannot be found in the specified paths.
		The original OSError is re-raised as well.
	"""
	try:
		CDLL(name)
		return name
	except OSError as e:
		if environ.get(ENV_VAR) is None:
			raise OSError(f'Environment variable {ENV_VAR} is not set.\n') from e
		# Try to find the library in the paths specified by ENV_VAR
		potential_paths = environ.get(ENV_VAR, default='')
		for base_path in potential_paths.split(':'):
			try:
				lib_path = str(Path(base_path) / name)
				CDLL(lib_path)
				return lib_path
			except OSError:
				pass
		raise OSError(f'Could not find "{name}" in {potential_paths}.\n') from e
