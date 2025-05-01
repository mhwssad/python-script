from pathlib import Path

fp = Path("E:\myproject\git\python-script\main.py")

print(fp.stem)
print(fp.stem.split(".")[0])
print(fp.name)
print(fp.parent)
print(fp.suffix)
print(fp.parts)
print(fp.root)
print(fp.anchor)
print(fp.drive)
print(fp.parents)
print(fp.suffixes)
