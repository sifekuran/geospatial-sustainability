"""
GSP 535 FINAL PROJECT - STORED FUNCTIONS MODULE
Author: Sife Kuran

Purpose:
This module stores helper functions used by both final_project1.py and final_project2.py
for the Orlando Fire Department structure count project.

"""

import arcpy    #Imports ArcGIS toolbox

# Checks if a given field exists in a feature class.
def FieldExists(fcname, fieldname):
    fields = arcpy.ListFields(fcname)
    for fld in fields:
        if fld.name.lower() == fieldname.lower():
            return True
    return False    #Returns True if the field exists, otherwise False

# Counts buildings of a specific UseCode that have their center inside a fire box
def CountBuildings(bldgfc, bldgcode, boxfc):
    # Make sure the building code is an integer
    code = int(bldgcode)

    # Build a where clause using the UseCode field
    where_clause = f"UseCode = {code}"

    # Temporary layer name for this selection
    bldg_layer = "bldg_layer_UseCode_" + str(code)

    # Create a feature layer filtered by UseCode
    arcpy.MakeFeatureLayer_management(bldgfc, bldg_layer, where_clause)

    # Select buildings whose center falls in the fire box
    arcpy.SelectLayerByLocation_management(
        bldg_layer,
        "HAVE_THEIR_CENTER_IN",
        boxfc,
        selection_type="NEW_SELECTION"
    )

    # Get the count of selected buildings
    result = arcpy.GetCount_management(bldg_layer)
    count = int(result[0])

    # Clean up the temporary layer
    arcpy.Delete_management(bldg_layer)

    return count

# Writes a building count into a specific field of a fire box
def WriteBuildingCount(fcname, fieldname, count):
    with arcpy.da.UpdateCursor(fcname, [fieldname]) as cursor:
        for row in cursor:
            row[0] = int(count)
            cursor.updateRow(row)
            # Only need to update the first row
            break

# Validate the user inputs for box number and building code.
def ValidateInputs(boxnumber, buildingcode):

    # Checks if box number is an integer
    try:
        boxnum = int(boxnumber)
    except ValueError:
        print("Box number must be an integer between 0 and 43.")
        return False

    if boxnum < 0 or boxnum > 43:
        print("Box number is out of range. It must be between 0 and 43.")
        return False

    # Checks if building code is an integer
    try:
        bcode = int(buildingcode)
    except ValueError:
        print("Building code must be an integer between 1 and 8.")
        return False

    if bcode < 1 or bcode > 8:
        print("Building code is out of range. It must be between 1 and 8.")
        return False

    # Checks if the fire box feature class exists in the current workspace
    fcname = f"FireBoxMap_{boxnum}"
    if not arcpy.Exists(fcname):
        print(f"Feature class {fcname} does not exist in workspace: {arcpy.env.workspace}")
        return False

    # All checks passed
    return True

# Returns the correct count field name based on building UseCode
def GetFieldName(buildingcode):
    code = int(buildingcode)
    mapping = {
        1: "SFCount",
        2: "MFCount",
        3: "ComCount",
        4: "IndCount",
        5: "CityCount",
        6: "ShedCount",
        7: "SchCount",
        8: "ChurCount"
    }
    return mapping.get(code)

# Returns a building type string for printing results
def GetBuildingType(buildingcode):
    code = int(buildingcode)
    mapping = {
        1: "Single family",
        2: "Multi-family",
        3: "Commercial",
        4: "Industrial",
        5: "City Property",
        6: "Storage Sheds",
        7: "Schools",
        8: "Church"
    }
    return mapping.get(code)

print("Completed successfully.")
