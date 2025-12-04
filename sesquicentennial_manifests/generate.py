from csv import DictReader
from manifest import TamuManifest

all_data = []
with open('sesq-merged-and-based.csv', 'r') as data_csv:
    csv_reader = DictReader(data_csv)
    for row in csv_reader:
        if row['Building Name'] != "":
            if row["Photograph Date"] != "":
                all_data.append(
                    {
                        "label": row['Building Name'],
                        "filename": row['Filename'],
                        "coords": row['Coordinates'],
                        "date": row['Photograph Date'],
                        'caption': row['Our Description / Notes'],
                        'based': row['based']
                    }
                )
for row in all_data:
    x = TamuManifest(row, ["navPlace.json"])
    x.write()
