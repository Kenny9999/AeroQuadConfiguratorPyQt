
from PyQt4 import QtGui
from ui.subpanel.pidparametersupdater.configsinglelinewidget.ConfigSingleLineWidgetUI import Ui_PIDSingleLineWidget

class ConfigSingleLineWidgetController(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        
        self.ui = Ui_PIDSingleLineWidget()
        self.ui.setupUi(self)
        
        self._min_bound = 0
        self._max_bound = 1000
        
        self.set_different()
        
        self.ui.slider.setSingleStep(1)
        self.ui.slider.sliderReleased.connect(self._slider_event)
        self.ui.slider.sliderMoved.connect(self._slider_event)
        self.ui.slider.valueChanged.connect(self._slider_event)
        self.ui.edit_box.valueChanged.connect(self._edit_box_value_changed)
        
    def set_different(self):
        self.ui.sync_feedback_label.setStyleSheet("background-color: rgb(255, 255, 0);")
        
    def set_same(self):
        self.ui.sync_feedback_label.setStyleSheet("background-color: rgb(0, 255, 0);")
        
    def set_title(self,title):
        self.ui.title_label.setText(title)
        
    def set_default(self, default):
        self.ui.default_label.setText(str(default))
        
    def set_bounds(self, min_value, max_value):
        self._min_bound = min_value
        self._max_bound = max_value
        self.ui.slider.setMinimum(int(self._min_bound)*100)
        self.ui.slider.setMaximum(int(self._max_bound)*100)
        self.ui.edit_box.setMinimum(float(self._min_bound))
        self.ui.edit_box.setMaximum(float(self._max_bound))
    
    def set_value(self,value):
        floatValue = float(value)
        self.ui.slider.setValue(floatValue*100.0)
        self.ui.edit_box.setValue(floatValue)
    
    def get_value(self):
        return self.ui.edit_box.value()
        
    def _slider_event(self):
        value = self.ui.slider.value()
        floatValue = float(float(value)/100.0)
        self.ui.edit_box.setValue(floatValue)
        self.set_different()
        
    def _edit_box_value_changed(self):
        value = self.ui.edit_box.value()
        self.ui.slider.setValue(value*100)
        self.set_different()
     
    def set_edit_box_enabled(self,enabled):
        self.ui.edit_box.setEnabled(enabled)
        
    def reset_default(self):
        self.ui.slider.setValue(int(float(self.ui.default_label.text())*100))
        self.ui.edit_box.setValue(float(self.ui.default_label.text()))
        self.set_different()
        
        
        