from iiif_prezi3 import Collection, config
from urllib.parse import quote
import os
import json

config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
base_url = "https://tamulib-dc-labs.github.io/sesquicentennial-manifests/"

collection = Collection(
    id=f"{base_url}collections.json",
    type="Collection",
    label="Building History"
)
for path, directories, files in os.walk("building_history"):
    for filename in files:
        if ".json" in filename:
            with open(os.path.join(path, filename), "r") as f:
                data = json.load(f)
            collection.make_manifest(
                id=data.get("id"),
                type="Manifest",
                label=data.get("label"),
                thumbnail=data.get("thumbnail"),
                summary=data.get("summary"),
            )
with open("collections.json", "w") as f:
    f.write(collection.json(indent=4))