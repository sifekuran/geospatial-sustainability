"""
GSP 535 FINAL PROJECT - TASK ONE
Author: Sife Kuran

Task:
The City of Orlando Fire Department needs a count of single family and multi family
homes for all 44 fire response zones.

"""

import arcpy    # Imports ArcGIS Toolbox
from final_functions import (FieldExists, CountBuildings, WriteBuildingCount) # Imports functions from final_functions

# Sets up workspace environment
arcpy.env.workspace = r"C:\Users\sifek\OneDrive - Northern Arizona University\GSP-535 Class\FireDepartment.gdb"
arcpy.env.overwriteOutput = True

# Name of the building footprint feature class
bldg_fc = "BldgFootprints"

# Print statements provided for an easier user interface
print("Starting Task One: Counting single-family and multi-family buildings in all fire boxes...")
print("Workspace:", arcpy.env.workspace)
print("Building footprints feature class:", bldg_fc)
print(" - " * 40)

# List all fire box feature classes: FireBoxMap_0 - FireBoxMap_43
box_list = arcpy.ListFeatureClasses("FireBoxMap_*")

if not box_list:
    print("No fire box feature classes were found. Please check the workspace.")
else:
    # Sort box names so they go in numerical order
    box_list.sort()

    # Loop through each fire box
    for box_fc in box_list:
        print(f"Processing fire box: {box_fc}")

        # Ensure SFCount and MFCount fields exist in the fire box
        for fld in ["SFCount", "MFCount"]:
            if not FieldExists(box_fc, fld):
                arcpy.AddField_management(box_fc, fld, "LONG")
                print(f"  Field '{fld}' did not exist and was added.")
            else:
                print(f"  Field '{fld}' already exists.")

        # Count buildings by UseCode in the current fire box
        # UseCode 1 = Single family, UseCode 2 = Multi family
        sf_count = CountBuildings(bldg_fc, 1, box_fc)
        mf_count = CountBuildings(bldg_fc, 2, box_fc)

        # Write the counts back into the fire box fields
        WriteBuildingCount(box_fc, "SFCount", sf_count)
        WriteBuildingCount(box_fc, "MFCount", mf_count)

        # Print a summary for this box
        print(f"  Single family (SFCount): {sf_count}")
        print(f"  Multi family (MFCount): {mf_count}")
        print(" - " * 40)

print("Task One completed. All fire boxes have SFCount and MFCount populated.")


