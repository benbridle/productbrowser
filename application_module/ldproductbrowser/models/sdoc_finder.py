import os
import glob


class SdocFinder:
    def __init__(self, sdoc_folder_path):
        if not os.path.isdir(sdoc_folder_path):
            raise FileNotFoundError(f"No folder at '{sdoc_folder_path}'")
        self.sdoc_folder_path = sdoc_folder_path
        self._sku_lookup = self._generate_sku_lookup()

    def _generate_sku_lookup(self):
        sku_lookup = {}
        file_paths = sorted(glob.glob(os.path.join(self.sdoc_folder_path, "*")))
        for file_path in file_paths:
            file_name = os.path.splitext(os.path.basename(file_path))[0]
            skus = file_name.split(" ")
            for sku in skus:
                try:
                    sku_lookup[int(sku)] = file_path
                except ValueError:
                    pass
        return sku_lookup

    def get_sdoc_path(self, sku):
        try:
            return self._sku_lookup[sku]
        except KeyError:
            return None
