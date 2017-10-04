import pymel.core as pm
import maya.cmds as mc
import functools

def createWindow(*args):

    windowID = 'myWindowID'
    
    if pm.window( windowID, exists=True ):
        pm.deleteUI( windowID )
    
    listNameLayer = []
    listAttribLayer = []
    
    for x in [ x for x in mc.ls( type='renderLayer' ) if not x.startswith( 'defaultRenderLayer' ) ]:
        attribLayer = mc.getAttr( x + '.identification' )
        listNameLayer.append( x )
        listAttribLayer.append( attribLayer )
        
    listNameLayer.sort( key=(dict(zip(listNameLayer, listAttribLayer)).get), reverse=True )
    
    pm.window( windowID, title='Window Demo', sizeable=False, resizeToFitChildren=True )
    pm.columnLayout( adjustableColumn=True )
    pm.textScrollList( 'renderLayer', allowMultiSelection=True, append=listNameLayer )
    pm.rowColumnLayout( numberOfColumns=3, columnOffset=[ (1,'right',3) ] )
    pm.button( label='Visible On / Off', command=toggleRenderLayer )
    pm.button( label='Delete', command=deleteRenderLayer )
    pm.button( label='Refresh', command=createWindow )
    pm.button( label='Add Selected Mesh to Selected Layer', command=addSelectedMeshToLayer )
    pm.button( label='Remove Selected Mesh from Selected Layer', command=removeSelectedMeshFromLayer )
    pm.showWindow()
    
def toggleRenderLayer(*args):
    layer = mc.ls( type='renderLayer' )
    renderLayerName = pm.textScrollList( 'renderLayer', query=True, selectItem=True, allowMultiSelection=True )
    for eachLayer in renderLayerName:
        if mc.getAttr( eachLayer + '.renderable' ) == False:
            mc.setAttr( eachLayer + '.renderable', 1 )
        elif mc.getAttr( eachLayer + '.renderable' ) == True:
            mc.setAttr( eachLayer + '.renderable', 0 )

def deleteRenderLayer(*args):
    layer = mc.ls( type='renderLayer' )
    renderLayerName = pm.textScrollList( 'renderLayer', query=True, selectItem=True, allowMultiSelection=True )
    mc.editRenderLayerGlobals( crl='defaultRenderLayer' )
    for eachLayer in renderLayerName:
        mc.delete( eachLayer )
        createWindow()

def addSelectedMeshToLayer(*args):
    layer = mc.ls( type='renderLayer' )
    renderLayerName = pm.textScrollList( 'renderLayer', query=True, selectItem=True, allowMultiSelection=True )
    selectedMesh = mc.ls(sl=True)
    for eachLayer in renderLayerName:
        mc.editRenderLayerMembers(eachLayer, selectedMesh, nr=True)

def removeSelectedMeshFromLayer(*args):
    layer = mc.ls( type='renderLayer' )
    renderLayerName = pm.textScrollList( 'renderLayer', query=True, selectItem=True, allowMultiSelection=True )
    selectedMesh = mc.ls(sl=True)
    for eachLayer in renderLayerName:
        mc.editRenderLayerMembers(eachLayer, selectedMesh, remove=True)

def main():
    createWindow()

if __name__ == '__main__':
    main()
