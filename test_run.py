from napari_label import label_plugin
import napari

if __name__ == '__main__':
    v = napari.Viewer()
    v.window.add_dock_widget(label_plugin.LabelWidget)
