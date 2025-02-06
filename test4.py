from dataclasses import dataclass
from ctypes import c_int32, c_int16

@dataclass
class MyClass:
    field1: c_int32
    field2: c_int16

# Create an instance of MyClass
obj = MyClass(42, 300)

# Print the object, which automatically calls __repr__
print(obj)