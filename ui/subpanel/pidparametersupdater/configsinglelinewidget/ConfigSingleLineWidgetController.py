
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
        self.ui.slider.sliderReleased.connect(self._slider_released)
        self.ui.slider.sliderMoved.connect(self._slider_move)
        self.ui.slider.valueChanged.connect(self._slider_move)
        self.ui.edit_box.valueChanged.connect(self._edit_box_value_changed)
        
        self._block_listener = False
        
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
        self.ui.slider.setMinimum(self._min_bound*100)
        self.ui.slider.setMaximum(self._max_bound*100)
        self.ui.edit_box.setMinimum(self._min_bound)
        self.ui.edit_box.setMaximum(self._max_bound)
    
    def set_value(self,value):
        self._block_listener = True
        floatValue = float(value)
        self.ui.slider.setValue(floatValue*100)
        self.ui.edit_box.setValue(floatValue)
        self._block_listener = False
    
    def get_value(self):
        return self.ui.edit_box.value()
        
    def _slider_released(self):
        if self._block_listener:
            return
        value = self.ui.slider.value()/100
        self.ui.edit_box.setValue(value)
        self.set_different()
        
    def _slider_move(self):
        if self._block_listener:
            return
        value = self.ui.slider.value()/100
        self.ui.edit_box.setValue(value)
        self.set_different()
        
    def _edit_box_value_changed(self):
        if self._block_listener:
            return
        value = self.ui.edit_box.value()
        self.ui.slider.setValue(value*100)
        self.set_different()
     
    def set_edit_box_enabled(self,enabled):
        self.ui.edit_box.setEnabled(enabled)
        
    def reset_default(self):
        self.ui.slider.setValue(float(self.ui.default_label.text())*100)
        self.ui.edit_box.setValue(float(self.ui.default_label.text()))
        self.set_different()
        
        
        