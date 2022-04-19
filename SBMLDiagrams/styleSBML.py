"""
@author: Jessie Jiang
"""
class Style:
    '''
    class describing the style for the ploting and drawing
    '''
    def __init__(self, style_name=None,
                 compartment_fill_color=None,
                 compartment_border_color=None,
                 species_fill_color=None,
                 species_border_color=None,
                 reaction_line_color=None,
                 font_color=None,
                 progress_bar_fill_color=None,
                 progress_bar_full_fill_color=None,
                 progress_bar_border_color=None,
                 reaction_line_width=None,
                 species_border_width=None,
                 compartment_border_width=None):
        '''

        Args:
            style_name: name for the style
            compartment_fill_color: compartment filled color
            compartment_border_color: compartment border color
            species_fill_color: species nodes filled color
            species_border_color: species nodes border color
            reaction_line_color: reaction line color
            font_color: font color
            progress_bar_fill_color: progress bar filled color
            progress_bar_full_fill_color: progress bar full filled color
            progress_bar_border_color: progress bar border color
        '''
        self.style_name = style_name
        self.compartment_fill_color = compartment_fill_color
        self.compartment_border_color = compartment_border_color
        self.species_fill_color = species_fill_color
        self.species_border_color = species_border_color
        self.reaction_line_color = reaction_line_color
        self.font_color = font_color

        self.progress_bar_fill_color = progress_bar_fill_color
        self.progress_bar_full_fill_color = progress_bar_full_fill_color
        self.progress_bar_border_color = progress_bar_border_color

        self.image_size = [1000,1000]
        self.node_dimension = [40,60]

        self.reaction_line_width = reaction_line_width
        self.species_border_width = species_border_width
        self.compartment_border_width = compartment_border_width

        if style_name == 'default':
            self.style_name = 'default'
            # for compartment's color
            self.compartment_fill_color = (255, 255, 255, 255)
            self.compartment_border_color = (255, 255, 255, 255)

            # for node's color
            self.species_fill_color = (255, 204, 153, 200)
            self.species_border_color = (255, 108, 9, 255)
            self.reaction_line_color = (91, 176, 253, 255)
            self.font_color = (0, 0, 0, 255)

            # for node's dimension
            self.node_dimension = [40,60]
            self.image_size = [1000,1000]

            # for progress bar's color
            self.progress_bar_fill_color = (255, 108, 9, 200)
            self.progress_bar_full_fill_color = (91, 176, 253, 200)
            self.progress_bar_border_color = (255, 204, 153, 200)

            # width
            self.reaction_line_width = 3.0
            self.species_border_width = 2.0
            self.compartment_border_width = 2.0

    def getCompBorderWidth(self):
        """

        Returns: the compartment border width

        """
        if self.compartment_border_width == 0.0: #makes border with to zero readable
           return self.compartment_border_width
        else:
            return self.compartment_border_width if self.compartment_border_width else 2.0
        

    def setCompBorderWidth(self, width):
        """

        Args:
            width: border width

        Returns:

        """
        self.compartment_border_width = width

    def getReactionLineWidth(self):
        """

        Returns: the reaction line width

        """
        return self.reaction_line_width if self.reaction_line_width else 3.0

    def setReactionLineWidth(self, width):
        """

        Args:
            width: the reaction line width

        Returns:

        """
        self.reaction_line_width = width

    def getSpecBorderWidth(self):
        """

        Returns: the species border width

        """
        if self.species_border_width == 0.0: #makes border with to zero possible
            return self.species_border_width
        else:
            return self.species_border_width if self.species_border_width else 2.0
        

    def setSpecBorderWidth(self, width):
        """

        Args:
            width: the species border width

        Returns:

        """
        self.species_border_width = width

    def getStyleName(self):
        '''

        Returns: the style name

        '''
        return self.style_name

    def setStyleName(self, style_name):
        '''
        set the style name

        Args:
            style_name: the style name

        '''
        self.style_name = style_name

    def getImageSize(self):
        '''

        Returns: image size

        '''
        return self.image_size

    def setImageSize(self, imageSize):
        '''
        set the image size

        Args:
            imageSize: size of the image drew

        '''
        self.image_size = imageSize

    def getNodeDimension(self):
        '''

        Returns: node dimension

        '''
        return self.node_dimension

    def setNodeDimension(self, dimension):
        '''
        set the node dimension

        Args:
            dimension: dimension of the node

        '''
        self.node_dimension = dimension

    def getProcessFillColor(self):
        '''

        Returns: the progress bar filled color or the default progress bar filled color

        '''
        return self.progress_bar_fill_color if self.progress_bar_fill_color else (255, 108, 9, 200)

    def getProcessBorderColor(self):
        '''

        Returns: the progress bar border color or the default the progress bar border

        '''
        return self.progress_bar_border_color if self.progress_bar_border_color else (255, 204, 153, 200)

    def getFullFillColor(self):
        '''

        Returns: progress bar full filled color or the default progress bar full filled color

        '''
        return self.progress_bar_full_fill_color if self.progress_bar_full_fill_color else (91, 176, 253, 200)

    def getCompFillColor(self):
        '''

        Returns: compartment filled color or the default compartment filled color

        '''
        return self.compartment_fill_color if self.compartment_fill_color else (255, 255, 255, 255)
        
    def getCompBorderColor(self):
        '''

        Returns: compartment border color or the default compartment border color

        '''
        return self.compartment_border_color if self.compartment_border_color else (255, 255, 255, 255)
        
    def getSpecFillColor(self):
        '''

        Returns: species nodes filled color or the default species nodes filled color

        '''
        return self.species_fill_color if self.species_fill_color else (255, 204, 153, 200)
        
    def getSpecBorderColor(self):
        '''

        Returns: species nodes border color or the default species nodes border color

        '''
        return self.species_border_color if self.species_border_color else (255, 108, 9, 255)
        
    def getReactionLineColor(self):
        '''

        Returns: reaction line color or the default reaction line color

        '''
        return self.reaction_line_color if self.reaction_line_color else (91, 176, 253, 255)
        
    def getTextLineColor(self):
        '''

        Returns: font color or the default font color

        '''
        return self.font_color if self.font_color else (0, 0, 0, 255)

    def setCompFillColor(self, color):
        '''
        set compartment filled color

        Args:
            color: color

        '''
        self.compartment_fill_color = color

    def setCompBorderColor(self, color):
        '''
        set compartment border color

        Args:
            color: color

        '''
        self.compartment_border_color = color

    def setSpecFillColor(self, color):
        '''
        set species nodes filled color

        Args:
            color: color

        '''
        self.species_fill_color = color

    def setSpecBorderColor(self, color):
        '''
        set species nodes border color

        Args:
            color: color

        '''
        self.species_border_color = color

    def setReactionLineColor(self, color):
        '''
        set reaction line color

        Args:
            color: color

        '''
        self.reaction_line_color = color

    def setTextLineColor(self, color):
        '''
        set font color

        Args:
            color:

        '''
        self.font_color = color



