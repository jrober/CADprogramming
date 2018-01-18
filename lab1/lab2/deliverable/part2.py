import adsk.core, adsk.fusion, traceback, adsk.cam


def run(context):
    ui = None
    try:
        #variables
        numberofTeeth = 40
        circumference = numberofTeeth * .5
        radius1 = circumference / (2*3.1415)
        radius2 = 0.156
        radius3 = radius1 + .25
        radius4 = .5

        app = adsk.core.Application.get()
        ui = app.userInterface
        
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        
        design = app.activeProduct

        # Get the root component of the active design.
        rootComp = adsk.fusion.Component.cast(design.rootComponent)

        # Create a new sketch on the xy plane.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Draw some circles.
        circles = sketch.sketchCurves.sketchCircles
        extrudes = rootComp.features.extrudeFeatures

        circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius3)
        
        profile = sketch.profiles.item(0)

        # flange
        extrudeInput = extrudes.createInput(profile,3)#adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(-.2)
        extrudeInput.setDistanceExtent(False,dist)
        extrudes.add(extrudeInput)
        
        
        
        circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius1)
        
        '''
        ui.messageBox("select two sketches")
        item1 = ui.selectEntity("select a sketch","Profiles")
        point1 = item1.point
        item2 = ui.selectEntity("select a second sketch","Profiles")
        point2 = item2.point
        dist = point1.distanceTo(point2)
        ui.messageBox("lenght= " + str(dist))
        '''
        
        # main extrude
        profile1 = sketch.profiles.item(1)

        extrudeInput = extrudes.createInput(profile1,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(1.5)
        extrudeInput.setDistanceExtent(False,dist)
        extrude = extrudes.add(extrudeInput)
        
        circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(radius1, 0, 0), radius2)
        
        profile2 = sketch.profiles.item(2)
        #teeth Extrude
        extrudeInput = extrudes.createInput(profile2,1)#adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(1.5)
        extrudeInput.setDistanceExtent(False,dist)
        extrude2 = extrudes.add(extrudeInput)
        
       
        circularPatterns = rootComp.features.circularPatternFeatures
       
        inputCol = adsk.core.ObjectCollection.create()
        inputCol.add(extrude2)
        inputAxis = rootComp.zConstructionAxis
       
        circularPatternInput = circularPatterns.createInput(inputCol,inputAxis)
        circularPatternInput.quantity = adsk.core.ValueInput.createByReal(numberofTeeth)
        circularPatternInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        circularPatternInput.isSymmectric = True
       
        circularPattern = circularPatterns.add(circularPatternInput)
        #hole cut
        circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius4)
        
        profile = sketch.profiles.item(3)

        extrudeInput = extrudes.createInput(profile,1)#adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(1.5)
        extrudeInput.setDistanceExtent(False,dist)
        extrudes.add(extrudeInput)
        
        extrudeInput = extrudes.createInput(profile,1)#adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        dist = adsk.core.ValueInput.createByReal(-.5)
        extrudeInput.setDistanceExtent(False,dist)
        extrudes.add(extrudeInput)
        
        
        
        
        
        

        # Add a circle at the center of one of the existing circles.
        #circle3 = circles.addByCenterRadius(circle2.centerSketchPoint, 4)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))