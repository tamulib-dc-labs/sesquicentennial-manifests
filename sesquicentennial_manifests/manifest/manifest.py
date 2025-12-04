from iiif_prezi3 import Manifest, config, KeyValueString, load_bundled_extensions
import json
from datetime import datetime, timezone
from urllib.parse import quote

config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
base_url = "https://tamulib-dc-labs.github.io/sesquicentennial_manifests/building_history"


class TamuManifest:
    def __init__(self, data, extensions=()):
        self.extensions = load_bundled_extensions(
            extensions=extensions
        )
        self.data = data
        self.output = f"{quote(self.data.get('label').split('.')[0].strip())}.json"
        self.manifest = self.build()

    def build(self):
        manifest_id = f"{base_url}/{quote(self.data.get('label').split('.')[0].strip())}"
        features = self.get_navPlace(self.data.get('coordinates'))
        summary = self.data.get('summary', "") if self.data.get('summary', "") != "" else " "
        nav_date = self.get_nav_date(self.data.get('date'))
        if len(features) > 0 and nav_date:
            manifest = Manifest(
                id=f"{manifest_id}.json",
                label=self.data.get('label'),
                summary=summary,
                metadata=self.get_metadata(self.data.get('metadata')),
                navPlace={"features": self.get_navPlace(self.data.get('coordinates'))},
                navDate=nav_date,
            )
        elif len(features) > 0:
            manifest = Manifest(
                id=f"{manifest_id}.json",
                label=self.data.get('label'),
                summary=summary,
                metadata=self.get_metadata(self.data.get('metadata')),
                navPlace={"features": self.get_navPlace(self.data.get('coordinates'))}
            )
        else:
            manifest = Manifest(
                id=f"{manifest_id}.json",
                label=self.data.get('label'),
                summary=summary,
                metadata=self.get_metadata(self.data.get('metadata')),
                navPlace={"features": self.get_navPlace(self.data.get('coordinates'))}
            )
        if self.data.get('canvases')[0].get('Image').strip() != "":
            manifest.create_thumbnail_from_iiif(
                self.data.get('canvases')[0].get('Image')
            )
        i = 1
        for canvas in self.data.get('canvases'):
            manifest.make_canvas_from_iiif(
                url=canvas.get('Image'),
                id=f"{manifest_id}/canvas/{i}",
                label=canvas.get('Filename'),
                metadata=self.get_metadata(
                    {
                        "Photograph Date": canvas.get("Photograph Date"),
                        "Filename": canvas.get("Filename"),
                        "Photo Description": canvas.get("Photo Description"),
                        "Ark": canvas.get("Ark"),
                    }
                ),
                anno_id=f"{manifest_id}/annotation/{i}",
                anno_page_id=f"{base_url}/page/{i}",
            )
            i += 1
        x = manifest.json(indent=2)
        manifest_as_json = json.loads(x)
        manifest_as_json['@context'] = [
            "http://iiif.io/api/extension/navplace/context.json",
            "http://iiif.io/api/presentation/3/context.json"
        ]
        return manifest_as_json

    def write(self):
        with open(f'building_history/{self.output}', 'w') as outfile:
            outfile.write(
                json.dumps(
                    self.manifest, indent=2
                )
            )

    def get_metadata(self, all_metadata):
        data = []
        for k, v in all_metadata.items():
            if v.strip() != "":
                data.append(
                    KeyValueString(
                        label=k,
                        value=v,
                    )
                )
        return data

    def get_nav_date(self, value):
        cleaned = value.replace("circa", "").strip().split("-")
        if len(cleaned) == 1 and len(cleaned[0]) == 4:
            return datetime(int(cleaned[0].strip()), 1, 1, tzinfo=timezone.utc)
        else:
            return None

    def get_navPlace(self, coords):
        if self.data.get('label', '') != self.data.get('caption', '') and self.data.get('caption', '') != "" and self.data.get('date', '') != "":
            text_value = f"{self.data.get('label', '')} -- {self.data.get('date', '')} -- {self.data.get('caption', '')}"
        elif self.data.get('label', '') != self.data.get('caption', '') and self.data.get('caption', '') != "":
            text_value = f"{self.data.get('label', '')} -- {self.data.get('caption', '')}"
        else:
            text_value = f"{self.data.get('label', '')}"
        try:
            return [
                {
                    "id": f"{base_url}/{quote(self.data.get('label').split('.')[0].strip())}/notdereferenceable/feature/1",
                    "type": "Feature",
                    "properties": {
                        "label": {
                            "en": [
                                text_value
                            ]
                        }
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            float(coords.split(',')[-1].strip()),
                            float(coords.split(',')[0].strip())
                        ]
                    }
                }
            ]
        except ValueError:
            print(f"No navPlace on: {self.data.get('label')}")
            return []

