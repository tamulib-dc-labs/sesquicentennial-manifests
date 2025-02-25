from csv import DictReader
from manifest import TamuManifest

all_data = []
with open('sesquicentennial_images.csv', 'r') as data_csv:
    csv_reader = DictReader(data_csv)
    for row in csv_reader:
        if row['Building Name'] != "":
            all_data.append(
                {
                    "label": row['Building Name'],
                    "filename": row['Filename'],
                    "coords": row['Coordinates'],
                    "date": row['Date'],
                    'caption': row['Notes/Description/Caption']
                }
            )
for row in all_data:
    x = TamuManifest(row, ["navPlace.json"])
    x.write()
