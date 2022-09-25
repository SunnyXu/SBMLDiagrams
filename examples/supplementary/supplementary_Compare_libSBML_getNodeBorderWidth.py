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

print("Get node border width by SBMLDiagrams:", sd.getNodeBorderWidth("x_0"))



#### use libSBML only ###

import libsbml
import pandas as pd


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
                    ### from here for render ###
                    rPlugin = layout.getPlugin("render")
                    if (rPlugin != None and rPlugin.getNumLocalRenderInformationObjects() > 0):
                        info = rPlugin.getRenderInformation(0)
                        color_list = []
                        for  j in range(0, info.getNumColorDefinitions()):
                            color = info.getColorDefinition(j)
                            color_list.append([color.getId(),color.createValueString()])
                        for j in range (0, info.getNumStyles()):
                            style = info.getStyle(j)
                            group = style.getGroup()
                            typeList = style.createTypeString()
                            idList = style.createIdString()
                            if 'SPECIESGLYPH' in typeList:
                                for k in range(len(color_list)):
                                    if color_list[k][0] == group.getStroke():
                                        spec_border_color = hex_to_rgb(color_list[k][1])
                                spec_border_width = group.getStrokeWidth()
                                self.spec_render.append([idList, spec_border_width, spec_border_color])
                        
        except Exception as e:
            raise Exception (e) 
      

    def getNodeBorderWidth(self, id, alias = 0):
        """
        Get the border width of a node with a given node id.

        Args: 
            id: str-the id of the node.
            
            alias: int-alias node index: 0 to number of alias nodes -1.

        Returns:
            border_width: float-node border line width.

        """

        border_width_list = []  
        for i in range(len(self.spec_render)):
            if id == self.spec_render[i][0]:
                spec_border_width = self.spec_render[i][1]
                border_width_list.append(spec_border_width)
        
        if len(border_width_list) == 0:
            raise Exception("This is not a valid id.")
        if alias < len(border_width_list) and alias >= 0:
            return border_width_list[alias]
        else:
            raise Exception("Alias index is beyond number of alias nodes.")
          

ls = Load(sbmlStr)
print("Get node border width by libSBML:", ls.getNodeBorderWidth("x_0"))


    
