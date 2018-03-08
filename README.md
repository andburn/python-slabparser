**Archived** This project has been archived. Unity 5.6 or newer files no longer have this text based format.

---

# SlabParser

A python module to parse the metadata from Unity3D shaderlab text files.

## Usage

Use the `shaderlab.parse()` method to create an `shaderlab.Shader` object containing the shader meta data.

```python
import shaderlab

with open(file, "r") as f:
    data = f.read()

slab = shaderlab.parse(data)
```

## Requirements
- Python 3.x
- *ply* package

