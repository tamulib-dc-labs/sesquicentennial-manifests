from iiif_prezi3 import Manifest, config
import base64
import httpx
import json

config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
base_url = "https://markpbaggett.github.io/static_iiif/manifests/sesquicentennial"


class TamuManifest:
    def __init__(self, data):
        self.data = data
        self.info = self.get_based(self.data.get('filename'))
        self.thumbnail = self.get_thumbnail(self.info)
        self.output = f"sesquicentennial/{self.data.get('filename').split('.')[0]}.json"
        self.manifest = self.build()

    def build(self):
        manifest_id = f"{base_url}/{self.data.get('filename').split('.')[0]}"
        manifest = Manifest(
            id=f"{manifest_id}.json",
            label=self.data.get('label'),
            summary=self.data.get('summary'),
            thumbnail=self.thumbnail,
        )
        manifest.make_canvas_from_iiif(
            url=self.info,
            id=f"{manifest_id}/canvas/1",
            label="image 1",
            anno_id=f"{manifest_id}/annotation/1",
            anno_page_id=f"{base_url}/page/1",
            thumbnail=self.thumbnail,
        )
        x = manifest.json(indent=2)
        manifest_as_json = json.loads(x)
        return manifest_as_json

    @staticmethod
    def get_based(identifier):
        uri = f"https://live.staticflickr.com/4028/{identifier}"
        encoded = base64.urlsafe_b64encode(bytes(uri, "utf-8"))
        decoded = encoded.decode("utf-8")
        return f"https://api-pre.library.tamu.edu/iiif/2/{decoded}"

    @staticmethod
    def get_thumbnail(base_uri):
        print(f"{base_uri}/info.json")
        image_response = httpx.get(f"{base_uri}/info.json", timeout=60).json()
        size = image_response['sizes'][-2]
        return {
            "id": f"{base_uri}/full/{size['width']},/0/default.jpg",
            "width": size['width'],
            "height": size['height'],
            "type": "Image",
            "format": "image/jpeg",
            "service": [
                {
                    "id": base_uri,
                    "type": "ImageService3",
                    "profile": "level2"
                }
            ]
        }

    def write(self):
        with open(f'manifests/{self.output}', 'w') as outfile:
            outfile.write(
                json.dumps(
                    self.manifest, indent=2
                )
            )




