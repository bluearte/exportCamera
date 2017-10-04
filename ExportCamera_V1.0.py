from PySide.QtCore import *
from PySide.QtGui import *

from shiboken import wrapInstance

import maya.OpenMayaUI as omui

import pymel.core as pm
import maya.mel as mel

import sys
import os

def mayaMainWindow():
    pointer = omui.MQtUtil.mainWindow()
    return wrapInstance(long(pointer), QWidget)

class CameraPanel(QWidget):
    def __init__(self, parent=mayaMainWindow()):
        super(CameraPanel, self).__init__(parent)
        
        self.initUI()
    
    def initUI(self):
        self.cam = CameraBake()
        self.export = CameraExport()
        
        self.label = QLabel()
        self.label.setText('Approved Camera Name')
        self.camLine = QLineEdit()
        self.camLine.setText(self.cam.cameraName)
        self.camLine.setEnabled(False)
        
        self.btnBake = QPushButton('Bake Camera')
        self.btnExport = QPushButton('Export Camera as FBX and ABC')
        self.btnFbx = QPushButton('Export as FBX')
        self.btnAbc = QPushButton('Export as ABC')
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.camLine)
        main_layout.addWidget(self.btnBake)
        main_layout.addWidget(self.btnExport)
        main_layout.addWidget(self.btnFbx)
        main_layout.addWidget(self.btnAbc)
        
        self.btnBake.clicked.connect(self.cam.makeCopy)
        self.btnExport.clicked.connect(self.export.export)
        self.btnFbx.clicked.connect(self.export.fbxExport)
        self.btnAbc.clicked.connect(self.export.abcExport)
        
        self.setLayout(main_layout)
        self.setWindowTitle('Camera Exporter')
        self.setWindowFlags(Qt.Tool)
        self.setAttribute(Qt.WA_DeleteOnClose)
        

        
class CameraPath:
    def __init__(self):
        self.fullPath = pm.sceneName()
        self.dirname = os.path.dirname(self.fullPath)
        self.basename = os.path.basename(self.fullPath)

class CameraBake:
    def __init__(self):
        self.cameraName = 'Camera:CAM'
        self.cameraClone = 'CAM_BAKE'
        self.first = pm.playbackOptions(min=True,q=True)
        self.last = pm.playbackOptions(max=True,q=True)
    
    def makeBake(self, cameraName):
        cameraName = cameraName
        cameraClone = pm.PyNode(self.cameraClone)
        
        first = self.first
        last = self.last
        
        for i in range(int(first),int(last)+1):
            pm.currentTime(int(i))
            worldTranslation = pm.xform(cameraName, q=True, worldSpace=True, translation=True)
            tx = worldTranslation[0]
            ty = worldTranslation[1]
            tz = worldTranslation[2]
            worldRotation = pm.xform(cameraName, q=True, worldSpace=True, rotation=True)
            rx = worldRotation[0]
            ry = worldRotation[1]
            rz = worldRotation[2]
            
            cameraClone.translateX.set(tx)
            cameraClone.translateY.set(ty)
            cameraClone.translateZ.set(tz)
            cameraClone.rotateX.set(rx)
            cameraClone.rotateY.set(ry)
            cameraClone.rotateZ.set(rz)
            pm.setKeyframe(cameraClone, breakdown=0, hierarchy="none", controlPoints=0, shape=0)
        
    def makeCopy(self):
        cameraName = self.cameraName
        cameraClone = self.cameraClone
        
        if cameraClone:
            try:
                pm.delete(cameraClone)
            except:
                pass
        
        try:
            self.verifycameraName(cameraName, cameraClone)
            self.makeBake(cameraName)
        except:
            cameraName = pm.ls(sl=True)[0]
            if pm.objectType(cameraName+'Shape', isType='camera'):
                self.verifycameraName(cameraName, cameraClone)
                self.makeBake(cameraName)
            
    def verifycameraName(self, cameraName, cameraClone):
        mel.eval("source channelBoxCommand;")
         
        pm.duplicate(cameraName, rr=True, name=cameraClone)
        pm.parent(cameraClone, w=True)
        
        mel.eval('CBunlockAttr'+' '+'"' +cameraClone+ '.tx";')
        mel.eval('CBunlockAttr'+' '+'"' +cameraClone+ '.ty";')
        mel.eval('CBunlockAttr'+' '+'"' +cameraClone+ '.tz";')
        mel.eval('CBunlockAttr'+' '+'"' +cameraClone+ '.rx";')
        mel.eval('CBunlockAttr'+' '+'"' +cameraClone+ '.ry";')
        mel.eval('CBunlockAttr'+' '+'"' +cameraClone+ '.rz";')

        
class CameraExport:
    def __init__(self):
        self.cam = CameraBake()
        self.path = CameraPath()
        
        self.cameraExportName = self.path.basename.split('.')[-2]
        self.cameraPath = self.path.dirname 
    
    def fbxSetting(self):
        cameraExportName = 'CAM_'+ self.cameraExportName +'_FBX.fbx'
        cameraClone = self.cam.cameraClone
        fbxPath = os.path.join(self.cameraPath, 'CAM', 'FBX')
        if not os.path.isdir(fbxPath):
            os.makedirs(fbxPath)
        camFBXpath = os.path.join(fbxPath, cameraExportName)
        mel.eval('FBXExportFileVersion -v FBX201400;')
        mel.eval('FBXExportConvertUnitString "cm";')
        mel.eval('FBXExportInputConnections -v 0;') 
        pm.select(cameraClone)
        pm.exportSelected( camFBXpath, force=True, options="v=0", type="FBX export", pr=True, es=True)
        
    def abcSetting(self):
        cameraExportName = 'CAM_'+ self.cameraExportName +'_ABC.abc'
        cameraClone = self.cam.cameraClone
        abcPath = os.path.join(self.cameraPath, 'CAM', 'ABC')
        if not os.path.isdir(abcPath):
            os.makedirs(abcPath)
        camABCpath = os.path.join(abcPath, cameraExportName)
        minFrame = self.cam.first
        maxFrame = self.cam.last
        command = "-frameRange" + " " + str(int(minFrame)) + " " + str(int(maxFrame)) + " " + "-root" + " " + "|" + str(cameraClone) + " -file " + str(camABCpath)
        pm.AbcExport(j = command)
    
    def export(self):
        cameraClone = self.cam.cameraClone
        self.cam.makeCopy()
        self.fbxSetting()
        self.abcSetting()
        pm.delete(cameraClone)
    
    def fbxExport(self):
        self.cam.makeCopy()
        self.fbxSetting()
        pm.delete(self.cam.cameraClone)
    
    def abcExport(self):
        self.cam.makeCopy()
        self.abcSetting()
        pm.delete(self.cam.cameraClone)
    
if __name__ == '__main__':  
    try:
        camPanel.close()
    except:
        pass
    camPanel = CameraPanel()
    camPanel.show() 