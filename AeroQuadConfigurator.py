'''
AeroQuad Configurator v4.0
Created on Nov 6, 2012

@author: Ted Carancho
'''
import sys

from PyQt4 import QtCore, QtGui
from mainWindow import Ui_MainWindow
from communication.serialCom import AQSerial

import xml.etree.ElementTree as ET
xml = ET.parse('AeroQuadConfigurator.xml')

from splashScreen import Ui_splashScreen
#from subCommMonitor.subCommMonitor import Ui_commMonitor

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class AQMain(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # TODO: figure out way to configure for different comm types (TCP, MAVLINK, etc) 
        self.comm = AQSerial()
        
        # Default main window conditions
        self.ui.buttonDisconnect.setEnabled(False)
        self.ui.buttonConnect.setEnabled(True)
        self.ui.comPort.setEnabled(True)
        self.ui.baudRate.setEnabled(True)
        self.ui.status.setText("Not connected to the AeroQuad")
        self.availablePorts = []
        self.updateComPortSelection()
        self.updateBaudRates()
        
        # Update comm port combo box to use last used comm port
        defaultComPort = xml.find("./Settings/DefaultComPort").text
        commIndex = self.ui.comPort.findText(defaultComPort)
        if commIndex == -1:
            commIndex = 0
        self.ui.comPort.setCurrentIndex(commIndex)
        
        # Load splash screen
        self.subPanel = Ui_splashScreen()
        self.subPanel.setupUi(self.subPanel)
        self.ui.subPanel.addWidget(self.subPanel)
        
        # Dynamically configure board type menu and subPanel menu from XML configuration file
        self.selectedBoardType = self.configureBoardTypeMenu()
        self.configureSubPanelMenu(self.selectedBoardType)
        self.activeSubPanel = None

        # Connect GUI slots and signals
        self.ui.buttonConnect.clicked.connect(self.connect)
        self.ui.buttonDisconnect.clicked.connect(self.disconnect)
        self.ui.actionExit.triggered.connect(QtGui.qApp.quit)
        self.ui.comPort.currentIndexChanged.connect(self.updateDetectedPorts)
        self.ui.actionBootUpDelay.triggered.connect(self.updateBootUpDelay)
        self.ui.actionCommTimeout.triggered.connect(self.updateCommTimeOut)


    '''Communication Methods'''        
    def connect(self):
        '''Initiates communication with the AeroQuad'''
        # Setup GUI
        self.ui.status.setText("Connecting to the " + self.selectedBoardType + "...")
        self.ui.buttonDisconnect.setEnabled(True)
        self.ui.buttonConnect.setEnabled(False)
        self.ui.comPort.setEnabled(False)
        self.ui.baudRate.setEnabled(False)
        # Update the GUI
        app.processEvents()
        
        # Setup serial port
        bootupDelay = float(xml.find("./Settings/BootUpDelay").text)
        commTimeOut = float(xml.find("./Settings/CommTimeOut").text)
        self.comm.connect(str(self.ui.comPort.currentText()), int(self.ui.baudRate.currentText()), bootupDelay, commTimeOut)
        self.comm.write("!")
        version = self.comm.read()
        if version != "":
            self.storeComPortSelection()
            self.ui.status.setText("Connected to the " + self.selectedBoardType + " using Flight Software v" + version)
            self.restartSubPanel()
        else:
            self.disconnect()
            self.ui.status.setText("Not connected to the " + self.selectedBoardType)
        
    def disconnect(self):
        '''Disconnect from the AeroQuad'''
        self.comm.write("X")
        self.comm.disconnect()
        # Update GUI
        self.ui.buttonDisconnect.setEnabled(False)
        self.ui.buttonConnect.setEnabled(True)
        self.ui.comPort.setEnabled(True)
        self.ui.baudRate.setEnabled(True)
        self.ui.status.setText("Disconnected from the " + self.selectedBoardType)
        self.restartSubPanel()

    def updateDetectedPorts(self):
        '''Cycles through 256 ports and checks if there is a response from them.'''
        selection = self.ui.comPort.currentText()
        if selection == "Refresh":
            self.updateComPortSelection
            self.ui.comPort.setCurrentIndex(0)
            self.ui.status.setText("Updated list of available COM ports")
        elif selection == "Autoconnect":
            self.ui.comPort.setCurrentIndex(0)
            self.ui.status.setText("This feature still under construction")
        elif selection == "-------":
            self.ui.comPort.setCurrentIndex(0)
    
    def updateBootUpDelay(self):
        '''Creates dialog box to ask user for desired boot up delay.
        This delay waits for Arduino based boards to finish booting up before sending commands.
        '''
        bootUpDelay = float(xml.find("./Settings/BootUpDelay").text)
        data, ok = QtGui.QInputDialog.getDouble(self, "Boot Up Delay", "Boot Up Delay:", bootUpDelay, 0, 60, 3)
        if ok:
            xml.find("./Settings/BootUpDelay").text = str(data)
            xml.write("AeroQuadConfigurator.xml")
 
    def updateCommTimeOut(self):
        '''Creates dialog box to ask user for desired comm timeout.
        This is timeout value used by serial drivers to wait for response from device
        '''
        commTimeOut = float(xml.find("./Settings/CommTimeOut").text)
        data, ok = QtGui.QInputDialog.getDouble(self, "Comm Time Out", "Comm Time Out:", commTimeOut, 0, 60, 3)
        if ok:
            xml.find("./Settings/CommTimeOut").text = str(data)
            xml.write("AeroQuadConfigurator.xml")

    def updateComPortSelection(self):
        '''Look for available comm ports and updates combo box'''
        self.ui.comPort.clear()
        for n in self.comm.detectPorts():
            self.ui.comPort.addItem(n)
        self.ui.comPort.addItem("-------")
        self.ui.comPort.addItem("Autoconnect")
        self.ui.comPort.addItem("Refresh")
        
    def storeComPortSelection(self):
        '''Stores comm port selection to xml file for later recall'''
        xml.find("./Settings/DefaultBaudRate").text = str(self.ui.baudRate.currentText())
        xml.find("./Settings/DefaultComPort").text = str(self.ui.comPort.currentText())
        xml.write("AeroQuadConfigurator.xml")
               
    def updateBaudRates(self):
        '''Reads baud rates from xml and displays in combo box.
        Updates the xml file to display different baud rates
        '''
        defaultBaudRate = xml.find("./Settings/DefaultBaudRate").text
        baudRates = xml.find("./Settings/AvailableBaudRates").text
        baudRate = baudRates.split(',')
        for i in baudRate:
            self.ui.baudRate.addItem(i)
        self.ui.baudRate.setCurrentIndex(baudRate.index(defaultBaudRate))     
 
    
    '''Board Selection Methods'''            
    def configureBoardTypeMenu(self):
        '''Dynamically add board types to menu bar'''
        boardNames = xml.findall("./Boards/Type")
        self.boardTypes = []
        self.boardMenu = []
        for board in boardNames:
            self.boardTypes.append(board.text)
        self.boardTypeMapper = QtCore.QSignalMapper(self)
        for boardType in self.boardTypes:
            self.ui.board = self.ui.menuBoard.addAction(boardType)
            self.boardMenu.append(self.ui.board) # Need to store this separately because Python only binds stuff at runtime
            self.boardTypeMapper.setMapping(self.ui.board, boardType)
            self.ui.board.triggered.connect(self.boardTypeMapper.map)
            self.ui.board.setCheckable(True)
        self.boardTypeMapper.mapped[str].connect(self.selectBoardType)
        selectedBoardType = xml.find("./Boards/Selected").text
        self.checkmarkBoardType(selectedBoardType)
        return selectedBoardType

    def selectBoardType(self, boardType):
        '''Places check mark beside selected board type
        Menu item instances stored in dedicated list because Python only updates during runtime making everything point to the last item in the list
        '''
        types = len(self.boardTypes)
        for name in range(types):
            self.boardMenu[name].setChecked(False)
        self.checkmarkBoardType(boardType)
        selected = self.boardTypes.index(boardType)
        self.boardMenu[selected].setChecked(True)
        xml.find("./Boards/Selected").text = str(boardType)
        xml.write("AeroQuadConfigurator.xml")
        self.selectedBoardType = boardType
        self.clearSubPanelMenu()
        self.configureSubPanelMenu(boardType)
        self.ui.subPanel.setCurrentIndex(0)

    def checkmarkBoardType(self, boardType):
        '''Place checkmark next to selected board type'''
        selected = self.boardTypes.index(boardType)
        self.boardMenu[selected].setChecked(True)

  
    ''' SubPanel Methods '''
    def configureSubPanelMenu(self, boardType):
        '''Dynamically add subpanels to View menu based on selected board type'''
        boardSubPanelName = "./Board/[@Type='" + str(boardType) + "']/Subpanels/Subpanel"
        subPanels = xml.findall(boardSubPanelName)
        subPanelCount = 1
        self.subPanelList = []
        self.subPanelClasses = []
        for subPanel in subPanels:
            self.subPanelList.append(subPanel.get("Name"))
            pathName = xml.find(boardSubPanelName + "/[@Name='" + subPanel.get("Name") +"']/Path").text
            className = xml.find(boardSubPanelName + "/[@Name='" + subPanel.get("Name") +"']/Class").text
            packageList = pathName.split('.')
            packageString = packageList[0] + '.' + packageList[1]
            module = __import__(packageString)
            for package in packageList[1:]:
                module = getattr(module, package)
            module = getattr(module, className)
            tempSubPanel = module()
            tempSubPanel.setupUi(tempSubPanel, self.comm)
            self.ui.subPanel.addWidget(tempSubPanel)
            self.subPanelClasses.append(tempSubPanel)
            subPanelCount += 1
            
        self.subPanelMapper = QtCore.QSignalMapper(self)
        self.subPanelMenu = []
        for subPanelName in self.subPanelList:
            subPanel = self.ui.menuView.addAction(subPanelName)
            self.subPanelMenu.append(subPanel) # Need to store this separately because Python only binds stuff at runtime
            self.subPanelMapper.setMapping(subPanel, subPanelName)
            subPanel.triggered.connect(self.subPanelMapper.map)
            subPanel.setCheckable(True)
        self.subPanelMapper.mapped[str].connect(self.selectSubPanel)
  
    def selectSubPanel(self, subPanelName):
        '''Places check mark beside selected subpanel name
        Menu item instances stored in dedicated list because Python only updates during runtime making everything point to the last item in the list
        '''
        if self.activeSubPanel != None:
            self.activeSubPanel.stop()
        types = len(self.subPanelList)
        for index in range(types):
            self.subPanelMenu[index].setChecked(False)
        selected = self.subPanelList.index(subPanelName)
        self.subPanelMenu[selected].setChecked(True)
        self.ui.subPanel.setCurrentIndex(selected+1) # index 0 is splash screen
        self.activeSubPanel = self.subPanelClasses[selected]
        self.activeSubPanel.start()
        
    def clearSubPanelMenu(self):
        ''' Clear subPanel menu and disconnect subPanel related signals'''
        self.ui.menuView.clear()
        self.subPanelMapper.mapped[str].disconnect(self.selectSubPanel)
        
    def restartSubPanel(self):
        if self.activeSubPanel != None: # Restart any running subpanels
            self.activeSubPanel.stop()
            self.activeSubPanel.start()
            
    ''' Housekeeping Functions'''
    def exit(self):
        self.comm.disconnect()
        sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    app.setStyle("plastique")
    MainWindow = AQMain()
    MainWindow.show()
    sys.exit(app.exec_())