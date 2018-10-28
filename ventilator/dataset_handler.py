from os import listdir
from os.path import isfile, join
import re


class DatasetHandler:

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def get_shotlogs(self):
        return [join(self.dataset_dir, f) for f in listdir(self.dataset_dir) if isfile(join(self.dataset_dir, f)) and self._file_is_shotlog(f)]

    def _file_is_shotlog(self, file):
        match = re.search("^shot log [A-Z]{3}.csv$", file)
        return match is not None
