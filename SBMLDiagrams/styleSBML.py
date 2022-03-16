"""
@author: Jessie Jiang
"""
class Style:
    def __init__(self, styleName=None,
                 comp_fill_color=None,
                 comp_border_color=None,
                 spec_fill_color=None,
                 spec_border_color=None,
                 reaction_line_color=None,
                 text_line_color=None,
                 process_fill_color=None,
                 full_fill_color=None,
                 process_border_color=None):
        self.styleName = styleName
        self.comp_fill_color = None
        self.comp_border_color = None
        self.spec_fill_color = None
        self.spec_border_color = None
        self.reaction_line_color = None
        self.text_line_color = None

        self.process_fill_color = None
        self.full_fill_color = None
        self.process_border_color = None

        self.image_size = None
        self.node_dimension = None

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
            self.image_size = [1000,1000]

            # for progress bar's color
            self.process_fill_color = (255, 108, 9, 200)
            self.full_fill_color = (91, 176, 253, 200)
            self.process_border_color = (255, 204, 153, 200)

        elif styleName == "simplicity":
            self.comp_fill_color = (255, 255, 255, 255) # white
            self.comp_border_color = (255, 255, 255, 255)
            self.spec_fill_color = (255, 255, 255, 255)
            self.spec_border_color = (0, 0, 0, 255) # black
            self.reaction_line_color = (0, 0, 0, 255)
            self.text_line_color = (0, 0, 0, 255)

            self.process_fill_color = (255, 108, 9, 200)
            self.full_fill_color = (91, 176, 253, 200)
            self.process_border_color = (255, 204, 153, 200)

            self.image_size = [1000, 1000]
            self.node_dimension = [40, 60]

    def getStyleName(self):
        return self.styleName

    def setStyleName(self, styleName):
        self.styleName = styleName

    def getImageSize(self):
        return self.image_size

    def setImageSize(self, imageSize):
        self.image_size = imageSize

    def getNodeDimension(self):
        return self.node_dimension

    def setNodeDimension(self, dimension):
        self.node_dimension = dimension

    def getProcessFillColor(self):
        return self.process_fill_color if self.process_fill_color else (255, 108, 9, 200)

    def getProcessBorderColor(self):
        return self.process_border_color if self.process_border_color else (255, 204, 153, 200)

    def getFullFillColor(self):
        return self.full_fill_color if self.full_fill_color else (91, 176, 253, 200)

    def getCompFillColor(self):
        return self.comp_fill_color if self.comp_fill_color else (255, 255, 255, 255)
        
    def getCompBorderColor(self):
        return self.comp_border_color if self.comp_border_color else (255, 255, 255, 255)
        
    def getSpecFillColor(self):
        return self.spec_fill_color if self.spec_fill_color else (255, 204, 153, 200)
        
    def getSpecBorderColor(self):
        return self.spec_border_color if self.spec_border_color else (255, 108, 9, 255)
        
    def getReactionLineColor(self):
        return self.reaction_line_color if self.reaction_line_color else (91, 176, 253, 255)
        
    def getTextLineColor(self):
        return self.text_line_color if self.text_line_color else (0, 0, 0, 255)

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



