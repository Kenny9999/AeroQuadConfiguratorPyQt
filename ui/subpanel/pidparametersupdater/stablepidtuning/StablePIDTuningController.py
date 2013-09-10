
from ui.subpanel.BasePanelController import BasePanelController

from PyQt4 import QtGui
from ui.subpanel.pidparametersupdater.pidtuningpanel.PIDTuningPanel import Ui_PIDTuningPanel
from ui.subpanel.pidparametersupdater.pidwidget.PIDWidgetController import PIDWidgetController
from ui.subpanel.pidparametersupdater.PIDUpdateMode import PIDUpdateMode
from model.PIDData import PIDData
from ui.UIEventDispatcher import UIEventDispatcher
from model.VehicleEventDispatcher import VehicleEventDispatcher


class StablePIDTuningController(QtGui.QWidget, BasePanelController):

    def __init__(self, vehicle_event_dispatcher, ui_event_dispatcher):

        QtGui.QWidget.__init__(self)
        BasePanelController.__init__(self)
        
        self.ui = Ui_PIDTuningPanel()
        self.ui.setupUi(self)
        
        self._current_accel_roll_pid = PIDData(3.5,0,0)
        self._current_gyro_roll_pid = PIDData(100,0,-350)
        self._current_accel_pitch_pid = PIDData(3.5,0,0)
        self._current_gyro_pitch_pid = PIDData(100,0,-350)
        
        self._user_update_mode = PIDUpdateMode.BEGINNER_MODE
        self._is_starting = False
        self._cpt_before_send = 5

        self._accel_roll_pid_controller = PIDWidgetController()
        self.ui.main_layout.addWidget(self._accel_roll_pid_controller)
        self._accel_roll_pid_controller.set_title('Accel')
        self._accel_roll_pid_controller.set_default(PIDData(3.5,0,0))
        self._accel_roll_pid_controller.p_line.ui.title_label.setText('Gain')
        self._accel_roll_pid_controller.set_p_bounds(2,6)
        self._accel_roll_pid_controller.i_line.ui.title_label.setText('Error Correction')
        self._accel_roll_pid_controller.set_i_bounds(0,5)
        self._accel_roll_pid_controller.d_line.ui.title_label.setText('Set Point Adjustment')
        self._accel_roll_pid_controller.set_d_bounds(-10,0)
        
        self._gyro_roll_pid_controller = PIDWidgetController()
        self.ui.main_layout.addWidget(self._gyro_roll_pid_controller)
        self._gyro_roll_pid_controller.set_title('Gyro')
        self._gyro_roll_pid_controller.set_default(PIDData(100,0,-350))
        self._gyro_roll_pid_controller.p_line.ui.title_label.setText('Gain')
        self._gyro_roll_pid_controller.set_p_bounds(50,200)
        self._gyro_roll_pid_controller.i_line.ui.title_label.setText('Error Correction')
        self._gyro_roll_pid_controller.set_i_bounds(0,300)
        self._gyro_roll_pid_controller.d_line.ui.title_label.setText('Set Point Adjustment')
        self._gyro_roll_pid_controller.set_d_bounds(-1000,-100)
        
        self._accel_pitch_pid_controller = PIDWidgetController()
        self.ui.main_layout.addWidget(self._accel_pitch_pid_controller)
        self._accel_pitch_pid_controller.set_title('Accel Pitch')
        self._accel_pitch_pid_controller.set_default(PIDData(3.5,0,0))
        self._accel_pitch_pid_controller.p_line.ui.title_label.setText('Gain')
        self._accel_pitch_pid_controller.set_p_bounds(2,6)
        self._accel_pitch_pid_controller.i_line.ui.title_label.setText('Error Correction')
        self._accel_pitch_pid_controller.set_i_bounds(0,5)
        self._accel_pitch_pid_controller.d_line.ui.title_label.setText('Set Point Adjustment')
        self._accel_pitch_pid_controller.set_d_bounds(-10,0)
        
        self._gyro_pitch_pid_controller = PIDWidgetController()
        self.ui.main_layout.addWidget(self._gyro_pitch_pid_controller)
        self._gyro_pitch_pid_controller.set_title('Gyro Pitch')
        self._gyro_pitch_pid_controller.set_default(PIDData(100,0,-350))
        self._gyro_pitch_pid_controller.p_line.ui.title_label.setText('Gain')
        self._gyro_pitch_pid_controller.set_p_bounds(50,200)
        self._gyro_pitch_pid_controller.i_line.ui.title_label.setText('Error Correction')
        self._gyro_pitch_pid_controller.set_i_bounds(0,300)
        self._gyro_pitch_pid_controller.d_line.ui.title_label.setText('Set Point Adjustment')
        self._gyro_pitch_pid_controller.set_d_bounds(-1000,-100)
        
        ui_event_dispatcher.register(self._protocol_handler_changed_event, UIEventDispatcher.PROTOCOL_HANDLER_EVENT)
        vehicle_event_dispatcher.register(self._accel_roll_pid_received, VehicleEventDispatcher.PID_STABLE_ACCEL_ROLL)
        vehicle_event_dispatcher.register(self._gyro_roll_pid_received, VehicleEventDispatcher.PID_STABLE_GYRO_ROLL)
        vehicle_event_dispatcher.register(self._accel_pitch_pid_received, VehicleEventDispatcher.PID_STABLE_ACCEL_PITCH)
        vehicle_event_dispatcher.register(self._gyro_pitch_pid_received, VehicleEventDispatcher.PID_STABLE_GYRO_PITCH)
        
        self.set_beginner_mode()
        
    def _protocol_handler_changed_event(self, event, protocol_handler):
        self._protocol_handler = protocol_handler;        
    
    def set_beginner_mode(self):
        self._user_update_mode = PIDUpdateMode.BEGINNER_MODE
        self._accel_roll_pid_controller.set_title('Accel')
        self._accel_roll_pid_controller.hide_i_line()
        self._accel_roll_pid_controller.hide_d_line()
        self._gyro_roll_pid_controller.set_title('Gyro')
        self._gyro_roll_pid_controller.hide_i_line()
        self._accel_pitch_pid_controller.hide()
        self._gyro_pitch_pid_controller.hide()
        self._accel_roll_pid_controller.set_edit_box_enabled(False)
        self._gyro_roll_pid_controller.set_edit_box_enabled(False)
        
    def set_intermediate_mode(self):
        self._user_update_mode = PIDUpdateMode.INTERMEDIATE_MODE
        self._accel_roll_pid_controller.set_title('Accel Roll')
        self._accel_roll_pid_controller.hide_i_line()
        self._accel_roll_pid_controller.hide_d_line()
        self._gyro_roll_pid_controller.set_title('Gyro Roll')
        self._gyro_roll_pid_controller.hide_i_line()
        self._accel_pitch_pid_controller.show()
        self._gyro_pitch_pid_controller.show()
        self._accel_pitch_pid_controller.hide_i_line()
        self._accel_pitch_pid_controller.hide_d_line()
        self._gyro_pitch_pid_controller.hide_i_line()
        self._accel_roll_pid_controller.set_edit_box_enabled(False)
        self._gyro_roll_pid_controller.set_edit_box_enabled(False)
        self._accel_pitch_pid_controller.set_edit_box_enabled(False)
        self._gyro_pitch_pid_controller.set_edit_box_enabled(False)
            
    def set_advanced_mode(self):
        self._user_update_mode = PIDUpdateMode.ADVANCED_MODE
        self._accel_roll_pid_controller.set_title('Accel Roll')
        self._accel_roll_pid_controller.show_i_line()
        self._accel_roll_pid_controller.show_d_line()
        self._gyro_roll_pid_controller.set_title('Gyro Roll')
        self._gyro_roll_pid_controller.show_i_line()
        self._accel_pitch_pid_controller.show()
        self._gyro_pitch_pid_controller.show()
        self._accel_pitch_pid_controller.show_i_line()
        self._accel_pitch_pid_controller.show_d_line()
        self._gyro_pitch_pid_controller.show_i_line()
        self._accel_roll_pid_controller.set_edit_box_enabled(True)
        self._gyro_roll_pid_controller.set_edit_box_enabled(True)
        self._accel_pitch_pid_controller.set_edit_box_enabled(True)
        self._gyro_pitch_pid_controller.set_edit_box_enabled(True)
        
    def _accel_roll_pid_received(self, event, accel_roll_pid):
        self._current_accel_roll_pid = accel_roll_pid
        if self._is_starting :
            self._accel_roll_pid_controller.set_current_pid(accel_roll_pid)
    
    def _gyro_roll_pid_received(self, event, gyro_roll_pid):
        self._current_gyro_roll_pid = gyro_roll_pid
        if self._is_starting :
            self._gyro_roll_pid_controller.set_current_pid(gyro_roll_pid)
    
    def _accel_pitch_pid_received(self, event, accel_pitch_pid):
        self._current_accel_pitch_pid = accel_pitch_pid
        if self._is_starting :
            self._accel_pitch_pid_controller.set_current_pid(accel_pitch_pid)
        
    def _gyro_pitch_pid_received(self, event, gyro_pitch_pid):
        self._current_gyro_pitch_pid = gyro_pitch_pid
        if self._is_starting :
            self._gyro_pitch_pid_controller.set_current_pid(gyro_pitch_pid)

    def start(self):
        self._is_starting = True
        self._sync_in_progress = True
        self._protocol_handler.get_stable_pid();
    
    def stop(self):
        self._protocol_handler.unsubscribe_command()
        
    def sync_with_board(self):
        if self._is_starting:
            if not self.is_synched():
                self._protocol_handler.send_command_wihout_subscription(self._protocol_handler.COMMANDS['GetAttitudePID']);
                return
            self._is_starting = False
            return

        if self.is_synched() :
            self._protocol_handler.unsubscribe_command()
            self._set_synched()
            return
        
        if self._cpt_before_send == 5 :
            self._protocol_handler.unsubscribe_command()
            self._send_pid_to_board()
            self._cpt_before_send = 0
            self._protocol_handler.get_stable_pid();
        else:
            self._protocol_handler.send_command_wihout_subscription(self._protocol_handler.COMMANDS['GetAttitudePID']);
            self._cpt_before_send = self._cpt_before_send + 1

    def is_synched(self):
        try:
            if not self._current_accel_roll_pid.is_equals(self._accel_roll_pid_controller.get_current_pid()) :
                return False
            elif not self._current_gyro_roll_pid.is_equals(self._gyro_roll_pid_controller.get_current_pid()) :
                return False
            elif not self._current_accel_pitch_pid.is_equals(self._accel_pitch_pid_controller.get_current_pid()) :
                return False
            elif not self._current_gyro_pitch_pid.is_equals(self._gyro_pitch_pid_controller.get_current_pid()) :
                return False
        except:
            return False
        return True
    
    def _set_synched(self):
        self._accel_roll_pid_controller.set_same()
        self._gyro_roll_pid_controller.set_same()
        self._accel_pitch_pid_controller.set_same()
        self._gyro_pitch_pid_controller.set_same()
        
    def _send_pid_to_board(self):
        accel_roll_pid = self._accel_roll_pid_controller.get_current_pid()
        gyro_roll_pid = self._gyro_roll_pid_controller.get_current_pid()
        accel_pitch_pid = self._accel_roll_pid_controller.get_current_pid()
        gyro_pitch_pid = self._gyro_roll_pid_controller.get_current_pid()
        if self._user_update_mode != PIDUpdateMode.BEGINNER_MODE :
            accel_pitch_pid = self._accel_pitch_pid_controller.get_current_pid()
            gyro_pitch_pid = self._gyro_pitch_pid_controller.get_current_pid()
        
        self._protocol_handler.set_stable_pid(accel_roll_pid, gyro_roll_pid, accel_pitch_pid, gyro_pitch_pid)

    
    def reset_default(self):
        self._accel_roll_pid_controller.reset_default()
        self._gyro_roll_pid_controller.reset_default()
        self._accel_pitch_pid_controller.reset_default()
        self._gyro_pitch_pid_controller.reset_default()
        