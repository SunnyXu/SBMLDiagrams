"""
@author: Jessie Jiang
"""
class Style:
    def __init__(self, styleName):
        if styleName == 'default':
            # for compartment's color
            self.comp_fill_color = (255, 255, 255, 255)
            self.comp_border_color = (255, 255, 255, 255)

            # for node's color
            self.spec_fill_color = (255, 204, 153, 200)
            self.spec_border_color = (255, 108, 9, 255)
            self.reaction_line_color = (91, 176, 253, 255)
            self.text_line_color = (0, 0, 0, 255)

            # for node's dimension
            self.node_dimension = [40,60]

            # for progress bar's color
            self.process_fill_color = (255, 108, 9, 255)
            self.full_fill_color = (91, 176, 253, 255)
            self.process_border_color = (255, 204, 153, 200)

        elif styleName == "simplicity":
            self.comp_fill_color = (0, 0, 0, 0)
            self.comp_border_color = (0, 0, 0, 255)
            self.spec_fill_color = (0, 0, 0, 0)
            self.spec_border_color = (0, 0, 0, 255)
            self.reaction_line_color = (0, 0, 0, 255)
            self.text_line_color = (0, 0, 0, 255)

    def getNodeDimension(self):
        return self.node_dimension

    def setNodeDimension(self, dimension):
        self.node_dimension = dimension

    def getProcessFillColor(self):
        return self.process_fill_color

    def getProcessBorderColor(self):
        return self.process_border_color

    def getFullFillColor(self):
        return self.full_fill_color

    def getCompFillColor(self):
        return self.comp_fill_color
        
    def getCompBorderColor(self):
        return self.comp_border_color
        
    def getSpecFillColor(self):
        return self.spec_fill_color
        
    def getSpecBorderColor(self):
        return self.spec_border_color
        
    def getReactionLineColor(self):
        return self.reaction_line_color
        
    def getTextLineColor(self):
        return self.text_line_color

    def setCompFillColor(self, color):
        self.comp_fill_color = color

    def setCompBorderColor(self, color):
        self.comp_border_color = color

    def setSpecFillColor(self, color):
        self.spec_fill_color = color

    def setSpecBorderColor(self, color):
        self.spec_border_color = color

    def setReactionLineColor(self, color):
        self.reaction_line_color = color

    def setTextLineColor(self, color):
        self.text_line_color = color



