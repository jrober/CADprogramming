import adsk.core, adsk.fusion, traceback, adsk.cam, os

app = adsk.core.Application.get()


importManager = app.importManager
rootComp = app.activeProduct.rootComponent
joints = rootComp.joints

def importPart( filename ):
    filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),filename)
        
    importOptions = importManager.createFusionArchiveImportOptions(filename)
    importManager.importToTarget(importOptions,rootComp)
    
    occurance = rootComp.occurrences.item(rootComp.occurrences.count-1)

    return occurance
    
def changePulley(numTeeth, diam, occur):
    parameters = occur.component.parentDesign.allParameters
    teethNumParam = parameters.itemByName('teethNum')
    shaftDiamParam = parameters.itemByName('shaftDiameter')
    teethNumParam.expression = str(numTeeth)
    shaftDiamParam.expression = str(diam) + 'cm'
    
    
def makeJoint(geo1,geo2):
    
    jointInput = joints.createInput(geo1,geo2)
    jointInput.setAsRigidJointMotion()
    joint1 = joints.add(jointInput)
    return joint1


def run(context):
    ui = None
    try:
        #variables
        radius1 = 2
        radius2 = 0.156

        numberOfTeeth = 18
        shaftDiameter = 0.5

        pulleyOccurance = importPart('squaretoothpulley.f3d')
        
        changePulley(numberOfTeeth,shaftDiameter,pulleyOccurance)
        
        cylinder = importPart('longCylinder.f3d')
        
        pulleyComp = pulleyOccurance.component
        pulleyFace = pulleyComp.features.holeFeatures.item(0).faces.item(0)
        faceProxy = pulleyFace.createForAssemblyContext(pulleyOccurance)

        
        ui = app.userInterface
        ui.messageBox('Select a Cylinder')
        item1 = ui.selectEntity("Select a cylinder","CylindricalFaces")
        baseObj1 = item1.entity 
        selectedFace = adsk.fusion.BRepFace.cast(baseObj1)

        geo1 = adsk.fusion.JointGeometry.createByNonPlanarFace(faceProxy,adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)
        geo2 = adsk.fusion.JointGeometry.createByNonPlanarFace(selectedFace,adsk.fusion.JointKeyPointTypes.MiddleKeyPoint)

        makeJoint(geo1,geo2)

        #parameters = cylinder.component.parentDesign.allParameters
        #extrudeLen = parameters.itemByName('d2')
        #extrudeLen.expression = str(10) + 'cm'
        
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
