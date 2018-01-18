import adsk.core, adsk.fusion, traceback, adsk.cam, os

def run(context):
    ui = None
    try:
        #variables
        radius1 = 2
        radius2 = 0.156

        numberOfTeeth = 18
        shaftDiameter = 0.5

        app = adsk.core.Application.get()
        ui = app.userInterface
        
        importManager = app.importManager
        rootComp = app.activeProduct.rootComponent

        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)),'squaretoothpulley.f3d')
        
        importOptions = importManager.createFusionArchiveImportOptions(filename)
        importManager.importToTarget(importOptions,rootComp)
        
        pulleyOccurance = rootComp.occurrences.item(rootComp.occurrences.count-1)
        

        parameters = pulleyOccurance.component.parentDesign.allParameters
        teethNumParam = parameters.itemByName('teethNum')
        shaftDiamParam = parameters.itemByName('shaftDiameter')
        teethNumParam.expression = str(numberOfTeeth)
        shaftDiamParam.expression = str(shaftDiameter) + 'cm'
        # Add a circle at the center of one of the existing circles.
        #circle3 = circles.addByCenterRadius(circle2.centerSketchPoint, 4)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))