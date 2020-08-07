import os
from datetime import datetime
from Luna.core.loggingFn import Logger
from Luna.utils import environFn
from Luna.utils import fileFn
from Luna.interface.hud import LunaHud
from PySide2 import QtWidgets


class Asset:
    def __init__(self, name, typ):
        self.name = name
        self.type = typ.lower()

        current_workspace = environFn.get_workspace_var()
        if not current_workspace:
            raise Exception("Workspace is not set")

        # Define paths
        self.path = os.path.join(current_workspace.path, self.type.lower() + "s", self.name)  # type:str
        self.meta_path = os.path.join(self.path, "asset.meta")  # type:str
        Logger.debug("Asset: {0} Type: {1} Path: {2}".format(self.name, self.type, self.path))

        # Meta updates
        self.meta = self.get_meta()

        # # Create directories
        fileFn.create_missing_dir(self.path)
        self.save_meta()
        self.controls = fileFn.create_missing_dir(os.path.join(self.path, "controls"))
        self.components = fileFn.create_missing_dir(os.path.join(self.path, "components"))
        self.rig = fileFn.create_missing_dir(os.path.join(self.path, "rig"))
        self.settings = fileFn.create_missing_dir(os.path.join(self.path, "settings"))
        self.weights = _weightsDirectorySctruct(self.path)
        self.data = _dataDirectoryStruct(self.path)

        # Set env variables and update hud
        environFn.set_asset_var(self)
        LunaHud.refresh()
        # Logger.debug("TODO: Update HUD")

    def get_meta(self):
        meta_dict = {}
        if os.path.isfile(self.meta_path):
            meta_dict = fileFn.load_json(self.meta_path)

        meta_dict["name"] = self.name
        meta_dict["type"] = self.type
        meta_dict["modified"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        meta_dict["model"] = meta_dict.get("model", "")
        if not meta_dict.get("created", ""):
            meta_dict["created"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        Logger.debug("{0} meta: {1}".format(self.name, meta_dict))
        return meta_dict

    def save_meta(self):
        if not self.meta.get("model", ""):
            self.meta["model"] = self.find_model()
        fileFn.write_json(self.meta_path, self.meta)

    def find_model(self):
        file_filters = "Maya (*.ma *mb);;Maya ASCII (*.ma);;Maya Binary(*.mb);;All Files (*.*)"
        selected_filter = "Maya (*.ma *mb)"
        model_path = QtWidgets.QFileDialog.getOpenFileName(None, "Select model file", self.path, file_filters, selected_filter)[0]
        if not model_path:
            return ""

        return model_path

    def set_model(self, path):
        self.meta["model"] = path
        self.save_meta()

        return path


class _weightsDirectorySctruct:
    """Directory scruct with folder per weight type"""

    def __init__(self, root):
        # DEFINE RIGGING DIRECTORIES
        self.blendShape = fileFn.create_missing_dir(os.path.join(root, "weights", "blendShape"))
        self.deltaMush = fileFn.create_missing_dir(os.path.join(root, "weights", "deltaMush"))
        self.ffd = fileFn.create_missing_dir(os.path.join(root, "weights", "ffd"))
        self.nCloth = fileFn.create_missing_dir(os.path.join(root, "weights", "nCloth"))
        self.skinCluster = fileFn.create_missing_dir(os.path.join(root, "weights", "skinCluster"))
        self.nonLinear = fileFn.create_missing_dir(os.path.join(root, "weights", "nonLinear"))
        self.tension = fileFn.create_missing_dir(os.path.join(root, "weights", "tension"))
        self.softMod = fileFn.create_missing_dir(os.path.join(root, "weights", "softMod"))
        self.dsAttract = fileFn.create_missing_dir(os.path.join(root, "weights", "dsAttract"))
        self.ngLayers = fileFn.create_missing_dir(os.path.join(root, "weights", "ngSkinLayers"))


class _dataDirectoryStruct:
    """Directory struct with folder per data type."""

    def __init__(self, root):
        self.blendShapes = fileFn.create_missing_dir(os.path.join(root, "data", "blendShapes"))
        self.poses = fileFn.create_missing_dir(os.path.join(root, "data", "poses"))
        self.xgen = fileFn.create_missing_dir(os.path.join(root, "data", "xgen"))
        self.mocap = fileFn.create_missing_dir(os.path.join(root, "data", "mocap"))
