import adsk.core, adsk.fusion, traceback, adsk.cam, math


def run(context):
    ui = None
    try:
        #variables
        radius1 = 2
        radius2 = 1

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

        circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), radius1)
        circles.addByCenterRadius(adsk.core.Point3D.create(7, 0, 0), radius2)
        
        ui.messageBox("select two center points for the belt")
        item1 = ui.selectEntity("select first center point","SketchPoints,Vertices,ConstructionPoints")
        point1 = item1.point
        item2 = ui.selectEntity("select second center point","SketchPoints,Vertices,ConstructionPoints")
        point2 = item2.point
        dist = point1.distanceTo(point2)
        ui.messageBox("lenght= " + str(dist))
        
  
        C = dist
        pi = 3.1415
        B = math.acos((radius1*2 - radius2*2)/(2 * C))
        beltLength = 2 * C * math.sin(B/2) + pi/2*(radius1 * 2 + radius2 * 2) + pi/180*(90-B/2)*(radius1 * 2 - radius2 * 2)
        ui.messageBox("lenght= " + str(beltLength))
        
        
        
        

        # Add a circle at the center of one of the existing circles.
        #circle3 = circles.addByCenterRadius(circle2.centerSketchPoint, 4)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))