
import SBMLDiagrams
import os


dirname = ""
filename = "Jana_WolfGlycolysis.xml"
with open(os.path.join(dirname, filename), 'r', encoding="utf8") as f:
     sbmlStr = f.read()

la = SBMLDiagrams.load(sbmlStr)

def createCircleNode (la, id, alias=0):
    #get center and size of the node
    center_list = la.getNodeCenter(id)

    if len(center_list) == 1:
        # Change the node size and corectly adjust for the new position
        center = center_list[0]
        la.setNodeSize(id, [18, 18])
        la.setNodePosition(id, [center.x-9, center.y-9])

        # get the new position and size
        p = la.getNodePosition(id)[alias]     
        size = la.getNodeSize(id)[alias]

        # Position thetrext just outside the node
        q = [p.x + 1.2*size.x, p.y-5]

        la.setNodeTextPosition(id, q)
        la.setNodeShape(id, 'ellipse')
        la.setNodeBorderWidth (id, 0) 
    else:
        num_alias = len(center_list)
        for alias in range(num_alias):
            # Change the node size and corectly adjust for the new position
            center = center_list[alias]
            la.setNodeSize(id, [18, 18], alias = alias)
            la.setNodePosition(id, [center.x-9, center.y-9], alias = alias)

            # get the new position and size
            p = la.getNodePosition(id)[alias]     
            size = la.getNodeSize(id)[alias]

            # Position thetrext just outside the node
            q = [p.x + 1.2*size.x, p.y-5]

            la.setNodeTextPosition(id, q, alias = alias)
            la.setNodeShape(id, 'ellipse', alias = alias)
            la.setNodeBorderWidth (id, 0, alias = alias) 

sp = la.getNodeIdList()
for s in sp:
    createCircleNode(la, s)

la.draw(output_fileName = 'output.png')
