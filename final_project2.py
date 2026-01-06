"""
GSP 535 FINAL PROJECT - TASK TWO
Author: Sife Kuran

Task:
The Fire Department wants to periodically update building counts for a specific
fire box and a specific building type.

"""

import arcpy     # Imports ArcGIS Toolbox
import sys       # Imports sys module
from final_functions import (   # Imports functions from final_functions
    FieldExists,
    CountBuildings,
    WriteBuildingCount,
    ValidateInputs,
    GetFieldName,
    GetBuildingType
)

# Sets up workspace environment
arcpy.env.workspace = r"C:\Users\sifek\OneDrive - Northern Arizona University\GSP-535 Class\FireDepartment.gdb"
arcpy.env.overwriteOutput = True

# Name of the building footprint feature class
bldg_fc = "BldgFootprints"

# Print statements provided for an easier user interface
print("Task Two: On demand building count for a single fire box")
print("Workspace:", arcpy.env.workspace)
print("Building footprints feature class:", bldg_fc)
print(" - " * 40)

# Get user input for box number and building code
box_input = input("Enter a fire box number (0–43): ")
bcode_input = input("Enter a building UseCode (1–8): ")

# Validate inputs using shared function
if not ValidateInputs(box_input, bcode_input):
    print("Input validation failed. Please fix the inputs and run the script again.")
    sys.exit()

# Convert validated inputs to integers
box_number = int(box_input)
bcode = int(bcode_input)

# Build the fire box feature class name
box_fc = f"FireBoxMap_{box_number}"

# Get the correct field name for this building type
field_name = GetFieldName(bcode)
building_type = GetBuildingType(bcode)

if field_name is None or building_type is None:
    print("Could not find a valid field name or building type for UseCode:", bcode)
    sys.exit()

print(f"Working on {box_fc} for building type: {building_type} (UseCode {bcode})")

# Make sure the count field exists. If they dont, add it
if not FieldExists(box_fc, field_name):
    arcpy.AddField_management(box_fc, field_name, "LONG")
    print(f"Field '{field_name}' did not exist in {box_fc} and was added.")
else:
    print(f"Field '{field_name}' already exists in {box_fc}.")

# Count buildings and write back to fire box
count = CountBuildings(bldg_fc, bcode, box_fc)
WriteBuildingCount(box_fc, field_name, count)

# Print summary result to the console
print(" - " * 40)
print(f"RESULT:")
print(f"{count} {building_type} buildings (UseCode {bcode}) have their center inside {box_fc}.")
print(f"The value {count} was written into field '{field_name}' of {box_fc}.")
print(" - " * 40)
print("Task Two completed.")
