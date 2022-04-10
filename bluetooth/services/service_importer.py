from pathlib import Path
import importlib


class ServiceImporter:
    def __init__(self, helper):
        self.dirs = []
        self.filenames = []
        self.class_names = []
        self.inst_classes = {}
        for path in Path(__file__).parent.iterdir():
            if path.is_dir() and str(path).endswith("_service"):
                path_arr = str(path).split("/")
                dirname = path_arr[-1]
                service_filename = dirname
                self.dirs.append(dirname)
                self.filenames.append(dirname)
                class_name = "".join(list(map(lambda x: x.title(), service_filename.split("_"))))
                self.class_names.append(class_name)
                temp = importlib.import_module(f'services.{dirname}.{service_filename}')
                class_ = getattr(temp, class_name)
                class_inst = class_(helper)
                self.inst_classes[class_name] = class_inst
