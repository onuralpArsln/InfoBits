import importlib.util
import sys
import os

module_name = "functions"
module_path = os.path.join(os.path.dirname(__file__), "functions.py")

spec = importlib.util.spec_from_file_location(module_name, module_path)
functions = importlib.util.module_from_spec(spec)
sys.modules[module_name] = functions
spec.loader.exec_module(functions)

# Now you can use functions.my_function()
functions.test()