import adsk.core, adsk.fusion, traceback, adsk.cam

def run(context):
    ui = None
    try:
        #variables
        radius1 = 2
        radius2 = 0.156

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
        circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius1)
        circle2 = circles.addByCenterRadius(adsk.core.Point3D.create(radius1, 0, 0), radius2)

        ui.messageBox("select two sketches")
        item1 = ui.selectEntity("select a sketch","SketchCircles")
        point1 = item1.point
        item2 = ui.selectEntity("select a second sketch","SketchCircles")
        point2 = item2.point
        dist = point1.distanceTo(point2)
        ui.messageBox("lenght= " + str(dist))
       
        

        # Add a circle at the center of one of the existing circles.
        #circle3 = circles.addByCenterRadius(circle2.centerSketchPoint, 4)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))