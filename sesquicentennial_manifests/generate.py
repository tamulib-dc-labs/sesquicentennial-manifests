from csv import DictReader
from manifest import TamuManifest
import json

all_data = []
manifest_data = {}
with open("updated_data.csv", 'r') as my_data:
    reader = DictReader(my_data)
    for row in reader:
        if row["Mark Note"].strip() == "":
            if row["Building Name"].strip() not in manifest_data.keys():
                manifest_data[row["Building Name"].strip()] = {
                    "label": row["Building Name"].strip(),
                    "coordinates": row["Coordinates"].strip(),
                    "summary": row["Building Facts"].strip(),
                    "date": row["Built"].strip(),
                    "metadata": {
                        "Alternative Name": row["Alternative Name"].strip(),
                        "Built": row["Built"].strip(),
                        "Razed": row["Razed"].strip(),
                        "Building Facts": row["Building Facts"].strip(),
                        "Sources": row["Sources"].strip(),
                    },
                    "canvases": [
                        {
                            "Photograph Date": row["Photograph Date"].strip(),
                            "Filename": row["Filename"].strip(),
                            "Photo Description": row["Photo Description"].strip(),
                            "Ark": row["Ark"].strip(),
                            "Image": row["Originating Image"].replace('/full/full/0/default.jpg', '/info.json'),
                        }
                    ]
                }
            else:
                manifest_data[row["Building Name"].strip()]["canvases"].append(
                    {
                        "Photograph Date": row["Photograph Date"].strip(),
                        "Filename": row["Filename"].strip(),
                        "Photo Description": row["Photo Description"].strip(),
                        "Ark": row["Ark"].strip(),
                        "Image": row["Originating Image"].replace('/full/full/0/default.jpg', '/info.json'),
                    }
                )
for k, v in manifest_data.items():
    all_data.append(v)

for item in all_data:
    x = TamuManifest(item, ["navPlace.json"])
    x.write()
