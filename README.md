# GPX to OBJ File Converter
**Version 1.0.0**
Converts GPX files into useable OBJ files. 
Useful for mapping areas and visualizing them in any 3d modeling engine.

---
## Usage
To retrieve the code/executable:
```
git clone https://github.com/KaiSomething/GPXtoOBJ.git
cd GPXtoOBJ
GPXtoOBJ.exe <gpx file path> <height> <width> <interpolation type>
```
Height and width refer to the grid size the GPX file will be projected onto, higher numbers will result in higher detail.
Interpolation types are as follows:
1 - cubic
2 - linear (recomended)
3 - nearest
