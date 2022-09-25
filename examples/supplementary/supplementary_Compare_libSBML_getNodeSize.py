#### read an SBML file ###
import os

DIR = os.path.dirname(os.path.abspath(__file__))

filename = "rectangle.xml"

f = open(os.path.join(DIR, filename), 'r')
sbmlStr = f.read()
f.close()

#### use SBMLDiagrams ###
import SBMLDiagrams

sd = SBMLDiagrams.load(sbmlStr)

print("Get node size by SBMLDiagrams (width, hight):", sd.getNodeSize("x_0").x, sd.getNodeSize("x_0").y)


#### use libSBML only ###

import libsbml
import pandas as pd

class Point:
    def __init__(self,x_init=0,y_init=0):
        """
        Define a Point object with attributes x and y.

        """
        self.x = x_init
        self.y = y_init

class Load:
    def __init__(self, sbmlStr = ''):
        """
        Load the SBML string.

        Args: 
            sbmlStr: str-the SBML string.
        """
        self.sbmlStr = sbmlStr

        def hex_to_rgb(value):
            """
            Change color format from hex string to rgb. 
            """
            value = value.lstrip('#')
            if len(value) == 6:
                value = value + 'ff'
            return [int(value[i:i+2], 16) for i in (0, 2, 4, 6)]

        self.spec_specGlyph_id_list = []
        self.spec_dimension_list = []
        self.spec_render = []

        mplugin = None
        try: 
            #check the validity of the sbml files.
            document = libsbml.readSBMLFromString(self.sbmlStr)
            if document.getNumErrors() != 0:
                errMsgRead = document.getErrorLog().toString()
                raise Exception("Errors in SBML Model: ", errMsgRead)
            ### from here for layout ###
            model_layout = document.getModel()
            try:
                mplugin = model_layout.getPlugin("layout")
            except:
                raise Exception("There is no layout.")
            if mplugin is not None:
                layout = mplugin.getLayout(0)    
                if layout is not None:
                    self.numSpecGlyphs = layout.getNumSpeciesGlyphs()
                    for i in range(self.numSpecGlyphs):
                        specGlyph = layout.getSpeciesGlyph(i)
                        specGlyph_id = specGlyph.getId()
                        spec_id = specGlyph.getSpeciesId()
                        self.spec_specGlyph_id_list.append([spec_id,specGlyph_id])
                        boundingbox = specGlyph.getBoundingBox()
                        height = boundingbox.getHeight()
                        width = boundingbox.getWidth()
                        self.spec_dimension_list.append([width,height])

        except Exception as e:
            raise Exception (e) 
    
    def getNodeSize(self, id, alias = 0):
        """
        Get the size of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            size: a Point object with attributes x and y representing
            the width and height of the node.

        Examples: 
            p =  Load(sbmlStr).getNodeSize('ATP')
            
            print ('Width = ', p.x, 'Height = ', p.y)

        """
        size_list = []  
        for i in range(self.numSpecGlyphs):
            if id == self.spec_specGlyph_id_list[i][0]:
                s = self.spec_dimension_list[i]
                size = Point(s[0], s[1])
                size_list.append(size)
        
        if len(size_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(size_list) and alias >= 0:
            return size_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias nodes.")
        


ls = Load(sbmlStr)
print("Get node size by libSBML (width, height):", ls.getNodeSize("x_0").x, ls.getNodeSize("x_0").y)



    
