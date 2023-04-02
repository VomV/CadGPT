from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Ax2
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal

L, W, H = 10, 5, 2
radius = 0.5 / 2

# Create the base block
block = BRepPrimAPI_MakeBox(L, W, H).Shape()

# Create and subtract holes at each corner
corner_points = [(0.5, 0.5), (L-0.5, 0.5), (L-0.5, W-0.5), (0.5, W-0.5)]
for x, y in corner_points:
    cylinder = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x, y, 0), gp_Dir(0, 0, 1)), radius, H).Shape()
    block = BRepAlgoAPI_Cut(block, cylinder).Shape()

# Export the 3D model to a STEP file
step_writer = STEPControl_Writer()
Interface_Static_SetCVal("write.step.schema", "AP203")

step_writer.Transfer(block, STEPControl_AsIs)
step_writer.Write("rectangle_with_corner_holes.step")
