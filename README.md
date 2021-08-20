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

0. cubic
1. linear (recomended)
2. nearest

---
## Notes

- This program works best on GPX files with similar heights and widths
- This is my first time publishing any code so sorry in advance if anything goes wrong.
- Hope this program helps you as much as it helped me!
