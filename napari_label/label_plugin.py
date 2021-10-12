import os

import napari
from napari.layers import Image
from napari.layers import Labels
import napari.utils.misc as misc 
import numpy as np
import tifffile

from PyQt5.QtWidgets import QGridLayout, QPushButton, QWidget
from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtWidgets import QFileDialog, QHBoxLayout
from PyQt5.QtCore import QRect

from napari_plugin_engine import napari_hook_implementation

class LabelWidget(QWidget):
    
    def __init__(self, napari_viewer):
        self.viewer = napari_viewer
        super().__init__()
       
        self.savedir = os.getcwd() 
        self.layout = QGridLayout()
        self.name_label = QLabel("Label Image")

        self.hlayout = QHBoxLayout()

        self.brush_label = QLabel("Brush Size", self)
        self.line_edit_brushsize = QLineEdit("10", self)
        self.hlayout.addWidget(self.brush_label)
        self.hlayout.addWidget(self.line_edit_brushsize)

        self.xbutton = QPushButton("Make Label", self)
        self.xbutton.clicked.connect(self.create_label_layer)

        self.savebutton = QPushButton("Save Mask", self)
        self.savebutton.clicked.connect(self.savemask)

        self.savedir_text = QLineEdit(self.savedir, self)
        self.dirbutton = QPushButton("Select Output Folder", self)
        self.dirbutton.clicked.connect(self.pickdir)

        self.layout.setGeometry(QRect(5, 400, 150, 200))
        # self.layout.setSpacing(1)
        self.layout.addLayout(self.hlayout, 1, 0)
        # self.layout.addWidget(self.line_edit_brushsize)
        # self.layout.setSpacing(2)
        self.layout.addWidget(self.dirbutton)
        self.layout.addWidget(self.savedir_text)
        self.layout.addWidget(self.xbutton)
        self.layout.addWidget(self.savebutton)
        self.setLayout(self.layout)
        self.layout.addWidget(self.name_label)
     
    def create_label_layer(self, event):

        brushsize = int(self.line_edit_brushsize.text())
        s = self.viewer.layers.selection.active
        label_name = f"{s.name}_label" 
        shape = s.data.shape
        if s.rgb:
            shape = (shape[0], shape[1])
        else:
            shape = (shape[-2], shape[-1])
        y = self.viewer.add_labels(np.zeros(shape, dtype=np.uint8), name=label_name)
        y.mode = 'paint'
        y.brush_size = brushsize

    def savemask(self, event):
        data = self.viewer.layers.selection.active.data
        name = self.viewer.layers.selection.active.name
        savedir = self.savedir_text.text()
        name = f"{savedir}/{name}.tif"
        tifffile.imwrite(name, data, imagej=True, dtype=np.uint8)

    def pickdir(self, event):
        resdir = QFileDialog.getExistingDirectory(parent=self,
                            caption="Select Mask Folder",
                            options=(
                                QFileDialog.DontUseNativeDialog
                                if misc.in_ipython()
                                else QFileDialog.Options()
                            ),
        )
        
        self.savedir = resdir
        self.savedir_text.setText(resdir)
        
@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return LabelWidget
        