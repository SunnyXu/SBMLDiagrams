# -*- coding: utf-8 -*-
# This script was written by Jin Xu and available on Github
# https://github.com/SunnyXu/SBMLDiagrams

"""
Created on Mon Aug 23 13:25:34 2021
@author: Jin Xu
"""

#from inspect import Parameter
import os
import libsbml
import re # to process kinetic_law string
import pandas as pd
import math
import sys
from SBMLDiagrams import processSBML

def _DFToSBML(df, compartmentDefaultSize = [1000,1000]):

    """
    Write the information of a set of dataframe to an SBML string. 

    Args:  
        (df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData): tuple.

        df_CompartmentData: DataFrame-Compartment information.

        df_NodeData: DataFrame-Node information.

        df_ReactionData: DataFrame-Reaction information.

        df_ArbitraryTextData: DataFrame-Arbitrary text information.

        df_ArbitrartyShapeData: DataFrame-Arbitrary shape information.

    Returns:
        SBMLStr_layout_render: str-the string of the output sbml file. 
    
    """

    def getSymbols(kinetic_law):
        str = kinetic_law
        str = str.replace(' ', '')  
        list = re.split('[+|\-|*|/|(|)]', str)
        list = [i for i in list if i != '']
        list_update = []
        for i in list:
            x = i.split(',')
            list_update.extend(x)
        res = []
        [res.append(x) for x in list_update if x not in res and not x.isdigit()]
        return res
     
    # if df == None:
    #     sys.exit("There is no valid information to process.")
    # else:

    try:
        try: 
            df_CompartmentData = df[0]
        except:
            df_CompartmentData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_CompartmentData)
        try:
            df_NodeData = df[1]
        except:
            df_NodeData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_NodeData)
        try:
            df_ReactionData = df[2]
        except:
            df_ReactionData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ReactionData)
        try:
            df_TextData = df[3]
        except:
            df_TextData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_TextData)
        try:
            df_ShapeData = df[4]
        except:
            df_ShapeData = pd.DataFrame(columns = processSBML.COLUMN_NAME_df_ShapeData)
    except Exception as err:
        raise Exception (err)

    #isReversible = False
    numNodes = len(df_NodeData)
    numReactions = len(df_ReactionData)
    numArbitraryTexts = len(df_TextData)
    numArbitraryShapes = len(df_ShapeData)

    if numNodes != 0 or numArbitraryTexts != 0 or numArbitraryShapes != 0:
        numCompartments = len(df_CompartmentData)      
    # #######################################

        # Creates an SBMLNamespaces object with the given SBML level, version
        # package name, package version.
        # 
        # (NOTE) By default, the name of package (i.e. "layout") will be used
        # if the argument for the prefix is missing or empty. Thus the argument
        # for the prefix can be added as follows:
        # 
        #    SBMLNamespaces sbmlns(3,1,"layout",1,"LAYOUT")
        # 
        sbmlns = libsbml.SBMLNamespaces(3, 1, "layout", 1)
        # create the document
        document = libsbml.SBMLDocument(sbmlns)
        # set the "required" attribute of layout package  to "true"
        document.setPkgRequired("layout", False)  

        # create the Model
        model = document.createModel()
        model.setId("Model_layout")
        document.setModel(model)

        # create the Compartment and species
        comp_id_list = []
        for i in range(numCompartments):
            comp_id_list.append(df_CompartmentData.iloc[i]['id']) 

        if numCompartments != 0:
            if "_compartment_default_" not in comp_id_list:
                compartment = model.createCompartment()
                comp_id="_compartment_default_"
                compartment.setId(comp_id)
                compartment.setConstant(True)
            for i in range(numCompartments):   
                compartment = model.createCompartment()
                comp_id=df_CompartmentData.iloc[i]['id']
                compartment.setId(comp_id)
                compartment.setConstant(True)
            spec_id_list = []
            for i in range(numNodes):
                original_index = df_NodeData.iloc[i]['original_idx']
                if original_index == -1:
                    spec_id = df_NodeData.iloc[i]['id']
                    if spec_id not in spec_id_list:
                        spec_id_list.append(spec_id)
                    species = model.createSpecies()
                    species.setId(spec_id)
                    comp_idx = df_NodeData.iloc[i]['comp_idx']
                    if comp_idx != -1:
                        comp_id = df_CompartmentData.iloc[comp_idx]['id'] 
                        species.setCompartment(comp_id)  
                    else:
                        species.setCompartment("_compartment_default_") 
                    species.setInitialConcentration(float(df_NodeData.iloc[i]['concentration']))	
                    species.setHasOnlySubstanceUnits(False)
                    species.setBoundaryCondition(False)
                    species.setConstant(False)            
                    if df_NodeData.iloc[i]['floating_node'] == 'FALSE':
                        species.setBoundaryCondition(True)
                        species.setConstant(True)   
        else: #set default compartment
            compartment = model.createCompartment()
            comp_id="_compartment_default_"
            compartment.setId(comp_id)
            compartment.setConstant(True)
            spec_id_list = []
            for i in range(numNodes):
                original_index = df_NodeData.iloc[i]['original_idx']
                if original_index == -1:
                    spec_id = df_NodeData.iloc[i]['id']
                    if spec_id not in spec_id_list:
                        spec_id_list.append(spec_id)
                    species = model.createSpecies()
                    species.setId(spec_id)
                    species.setCompartment(comp_id)
                    species.setInitialConcentration(float(df_NodeData.iloc[i]['concentration']))	
                    species.setHasOnlySubstanceUnits(False)
                    species.setBoundaryCondition(False)
                    species.setConstant(False)             
                    if df_NodeData.iloc[i]['floating_node'] == 'FALSE':
                        species.setBoundaryCondition(True)
                        species.setConstant(True)
        # create reactions:
        for i in range(numReactions):
            reaction_id = df_ReactionData.iloc[i]['id']
            rxn_rev = bool(df_ReactionData.iloc[i]['rxn_reversible'])
            isReversible = rxn_rev
            rct = [] # id list of the rcts
            prd = []
            mod = []
            try: #from excel sheet
                rct_list = list(df_ReactionData.iloc[i]['sources'][1:-1].split(","))
                prd_list = list(df_ReactionData.iloc[i]['targets'][1:-1].split(","))
                mod_list = list(df_ReactionData.iloc[i]['modifiers'][1:-1].split(","))
            except: #from dataFrame
                rct_list = df_ReactionData.iloc[i]['sources']
                prd_list = df_ReactionData.iloc[i]['targets']
                mod_list = df_ReactionData.iloc[i]['modifiers']

            rct_num = len(rct_list)
            prd_num = len(prd_list)
            mod_num = len(mod_list)
            for j in range(rct_num):
                try:
                    rct.append(df_NodeData.iloc[int(rct_list[j])]['id'])
                except:
                    rct_num = 0
            for j in range(prd_num):
                try:
                    prd.append(df_NodeData.iloc[int(prd_list[j])]['id'])
                except:
                    prd_num = 0
            
            for j in range(mod_num):
                try:
                    mod.append(df_NodeData.iloc[int(mod_list[j])]['id'])
                except:
                    mod_num = 0

            kinetic_law_from_user = df_ReactionData.iloc[i]['rate_law']
            flag_nan = 0
            try:
                math.isnan(kinetic_law_from_user)
                flag_nan = 1
            except:
                pass

            if str(kinetic_law_from_user) == '' or flag_nan == 1:
                kinetic_law = ''
                parameter_list = []
                kinetic_law = kinetic_law + 'E' + str (i) + '*(k' + str (i) 
                parameter_list.append('E' + str (i))
                parameter_list.append('k' + str (i))
                for j in range(rct_num):
                    kinetic_law = kinetic_law + '*' + rct[j]
                    
                if isReversible:
                    kinetic_law = kinetic_law + ' - k' + str (i) + 'r'
                    parameter_list.append('k' + str (i) + 'r')
                    for j in range(prd_num):
                        kinetic_law = kinetic_law + '*' + prd[j]
                kinetic_law = kinetic_law + ')'
            else:
                kinetic_law = kinetic_law_from_user
                parameter_spec_list = getSymbols(kinetic_law_from_user) 
                parameter_list = []
                for j in range(len(parameter_spec_list)):
                    if parameter_spec_list[j] not in spec_id_list:
                        parameter_list.append(parameter_spec_list[j])
                if len(parameter_list) == 0: #If the input kinetic law is invalid
                    kinetic_law = ''
                    parameter_list = []
                    kinetic_law = kinetic_law + 'E' + str (i) + '*(k' + str (i) 
                    parameter_list.append('E' + str (i))
                    parameter_list.append('k' + str (i))
                    for j in range(rct_num):
                        kinetic_law = kinetic_law + '*' + rct[j]
                        
                    if isReversible:
                        kinetic_law = kinetic_law + ' - k' + str (i) + 'r'
                        parameter_list.append('k' + str (i) + 'r')
                        for j in range(prd_num):
                            kinetic_law = kinetic_law + '*' + prd[j]
                    kinetic_law = kinetic_law + ')'
        
            reaction = model.createReaction()
            reaction.setId(df_ReactionData.iloc[i]['id'])
            reaction.setReversible(False)
            reaction.setFast(False)
            if isReversible:
                reaction.setReversible(True)
            for j in range(len(parameter_list)):
                parameters = model.createParameter()
                parameters.setId(parameter_list[j])
                parameters.setValue(0.1) # needs to set as the true parameter value.
                parameters.setConstant(True)
            kinetics = reaction.createKineticLaw()
            kinetics.setFormula(kinetic_law)
            
            for j in range(rct_num):
                reference = reaction.createReactant()
                reference.setSpecies(rct[j])
                ref_id = "SpecRef_" + reaction_id + "_rct" + str(j)
                reference.setId(ref_id)
                reference.setStoichiometry(1.)
                reference.setConstant(False)

            for j in range(prd_num):
                reference = reaction.createProduct()
                reference.setSpecies(prd[j])
                ref_id = "SpecRef_" + reaction_id + "_prd" + str(j)
                reference.setId(ref_id)
                reference.setStoichiometry(1.)
                reference.setConstant(False)

            for j in range(mod_num):
                reference = reaction.createModifier()
                reference.setSpecies(mod[j])
                ref_id = "SpecRef_" + reaction_id + "_mod" + str(j)
                reference.setId(ref_id)

        sbmlStr = libsbml.writeSBMLToString(document) #sbmlStr is w/o layout or render info

        # create the Layout

        #
        # set the LayoutPkgNamespaces for Level 3 Version1 Layout Version 1
        #
        layoutns = libsbml.LayoutPkgNamespaces(3, 1, 1)

        renderns = libsbml.RenderPkgNamespaces(3, 1, 1)

        #
        # Get a LayoutModelPlugin object plugged in the model object.
        #
        # The type of the returned value of SBase::getPlugin() function is SBasePlugin, and
        # thus the value needs to be casted for the corresponding derived class.
        #

        mplugin = model.getPlugin("layout")

        # rPlugin = model.getPlugin("render")
        # if rPlugin is None:
        #   print("there is no render outside layout.")
                
        # lolPlugin = mplugin.getListOfLayouts().getPlugin("render")
        # if lolPlugin is None:
        #   print("there is no render info inside layout.")
        
        # if mplugin is None:
            # print(
            #     "[Fatal Error] Layout Extension Level " + layoutns.getLevel() + " Version " + layoutns.getVersion() + " package version " + layoutns.getPackageVersion() + " is not registered.")
            # sys.exit(1)
        #
        # Creates a Layout object via LayoutModelPlugin object.
        #
        layout = mplugin.createLayout()
        layout.setId("Layout_1")
        layout.setDimensions(libsbml.Dimensions(layoutns, 800.0, 800.0))
        # random network (40+800x, 40+800y)

        #create the CompartmentGlyph and SpeciesGlyphs
        if numCompartments != 0:
            for i in range(numCompartments):   
                comp_id=df_CompartmentData.iloc[i]['id']
                if comp_id != "_compartment_default_":
                    compartmentGlyph = layout.createCompartmentGlyph()
                    compG_id = "CompG_" + comp_id
                    compartmentGlyph.setId(compG_id)
                    compartmentGlyph.setCompartmentId(comp_id)
                    bb_id  = "bb_" + comp_id
                    try: 
                        position_list = list(df_CompartmentData.iloc[i]['position'][1:-1].split(","))
                        size_list = list(df_CompartmentData.iloc[i]['size'][1:-1].split(","))
                    except: 
                        position_list = df_CompartmentData.iloc[i]['position']
                        size_list = df_CompartmentData.iloc[i]['size']
                    pos_x  = float(position_list[0])
                    pos_y  = float(position_list[1])
                    width  = float(size_list[0])
                    height = float(size_list[1])
                    compartmentGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))
            for i in range(numNodes): 
                spec_id = df_NodeData.iloc[i]['id']  
                spec_index = df_NodeData.iloc[i]['idx']
                spec_shapeIdx = int(df_NodeData.iloc[i]['shape_idx'])
                spec_shapeType = df_NodeData.iloc[i]['shape_type']
                try:
                    spec_shapeInfo_list_pre = list(df_NodeData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    spec_shapeInfo_list_pre = df_NodeData.iloc[i]['shape_info']
                #from excel sheet
                if spec_shapeInfo_list_pre == ['']:
                    spec_shapeInfo = []
                elif len(spec_shapeInfo_list_pre) == 0:
                    spec_shapeInfo = []
                else:
                    spec_shapeInfo_pre = []
                    spec_shapeInfo = []
                    if type(spec_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(spec_shapeInfo_list_pre)):
                            temp = spec_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            spec_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(spec_shapeInfo_pre),2):
                            spec_shapeInfo.append([spec_shapeInfo_pre[ii], spec_shapeInfo_pre[ii+1]])
                    else:
                        spec_shapeInfo = spec_shapeInfo_list_pre
                speciesGlyph = layout.createSpeciesGlyph()
                specG_id = "SpecG_"  + spec_id + '_idx_' + str(spec_index)
                speciesGlyph.setId(specG_id)
                speciesGlyph.setSpeciesId(spec_id)
                bb_id  = "bb_" + spec_id + '_idx_' + str(spec_index)

                try:
                    position_list = list(df_NodeData.iloc[i]['position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['position']
                    size_list = df_NodeData.iloc[i]['size']
                pos_x  = float(position_list[0])
                pos_y  = float(position_list[1])
                width  = float(size_list[0])
                height = float(size_list[1])
                speciesGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))

                textGlyph = layout.createTextGlyph()
                textG_id = "TextG_" + spec_id + '_idx_' + str(spec_index)
                textGlyph.setId(textG_id)
                #textGlyph.setText(spec_id) # this will merge "setOriginOfTextId"
                bb_id  = "bb_spec_text_" + spec_id + '_idx_' + str(spec_index)
                try:
                    position_list = list(df_NodeData.iloc[i]['txt_position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['txt_size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['txt_position']
                    size_list = df_NodeData.iloc[i]['txt_size']
                pos_x_text  = float(position_list[0])
                pos_y_text  = float(position_list[1])
                width_text  = float(size_list[0])
                height_text = float(size_list[1])
                textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))
                textGlyph.setOriginOfTextId(specG_id)
                textGlyph.setGraphicalObjectId(specG_id)
        else:#there is no compartment  
            comp_id= "_compartment_default_"
            compartmentGlyph = layout.createCompartmentGlyph()
            compG_id = "CompG_" + comp_id
            compartmentGlyph.setId(compG_id)
            compartmentGlyph.setCompartmentId(comp_id)
            bb_id  = "bb_" + comp_id
            pos_x  = 0
            pos_y  = 0
            width  = compartmentDefaultSize[0]
            height = compartmentDefaultSize[1]
            compartmentGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))
        
            for i in range(numNodes):
                spec_id = df_NodeData.iloc[i]['id']  
                spec_index = df_NodeData.iloc[i]['idx']
                spec_shapeIdx = int(df_NodeData.iloc[i]['shape_idx'])
                spec_shapeIdx = df_NodeData.iloc[i]['shape_idx']
                spec_shapeType = df_NodeData.iloc[i]['shape_type']
                try:
                    spec_shapeInfo_list_pre = list(df_NodeData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    spec_shapeInfo_list_pre = df_NodeData.iloc[i]['shape_info']
                if spec_shapeInfo_list_pre == ['']:
                    spec_shapeInfo = []
                elif len(spec_shapeInfo_list_pre) == 0:
                    spec_shapeInfo = []
                else:
                    spec_shapeInfo_pre = []
                    spec_shapeInfo = []
                    if type(spec_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(spec_shapeInfo_list_pre)):
                            temp = spec_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            spec_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(spec_shapeInfo_pre),2):
                            spec_shapeInfo.append([spec_shapeInfo_pre[ii], spec_shapeInfo_pre[ii+1]])
                    else:
                        spec_shapeInfo = spec_shapeInfo_list_pre
                speciesGlyph = layout.createSpeciesGlyph()
                specG_id = "SpecG_"  + spec_id + '_idx_' + str(spec_index)
                speciesGlyph.setId(specG_id)
                speciesGlyph.setSpeciesId(spec_id)
                bb_id  = "bb_" + spec_id + '_idx_' + str(spec_index)
                try:
                    position_list = list(df_NodeData.iloc[i]['position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['position']
                    size_list = df_NodeData.iloc[i]['size']
                pos_x  = float(position_list[0])
                pos_y  = float(position_list[1])
                width  = float(size_list[0])
                height = float(size_list[1])
                speciesGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))

                textGlyph = layout.createTextGlyph()
                textG_id = "TextG_" + spec_id + '_idx_' + str(spec_index)
                textGlyph.setId(textG_id)
                #textGlyph.setText(spec_id) # this will merge "setOriginOfTextId
                try:
                    position_list = list(df_NodeData.iloc[i]['txt_position'][1:-1].split(","))
                    size_list = list(df_NodeData.iloc[i]['txt_size'][1:-1].split(","))
                except:
                    position_list = df_NodeData.iloc[i]['txt_position']
                    size_list = df_NodeData.iloc[i]['txt_size']
                pos_x_text  = float(position_list[0])
                pos_y_text  = float(position_list[1])
                width_text  = float(size_list[0])
                height_text = float(size_list[1])
                bb_id  = "bb_spec_text_" + spec_id + '_idx_' + str(spec_index)
                textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))
                textGlyph.setOriginOfTextId(specG_id)
                textGlyph.setGraphicalObjectId(specG_id)

        # create the ReactionGlyphs and SpeciesReferenceGlyphs
        for i in range(numReactions):
            reaction_id = df_ReactionData.iloc[i]['id']
            
            reactionGlyph = layout.createReactionGlyph()
            reactionG_id = "RectionG_" + reaction_id
            reactionGlyph.setId(reactionG_id)
            reactionGlyph.setReactionId(reaction_id)
            
            rct = [] # id list of the rcts
            prd = []
            mod = []
            try:
                rct_list = list(df_ReactionData.iloc[i]['sources'][1:-1].split(","))
                prd_list = list(df_ReactionData.iloc[i]['targets'][1:-1].split(","))
                mod_list = list(df_ReactionData.iloc[i]['modifiers'][1:-1].split(","))
            except:
                rct_list = df_ReactionData.iloc[i]['sources']
                prd_list = df_ReactionData.iloc[i]['targets']
                mod_list = df_ReactionData.iloc[i]['modifiers']
            rct_index = []
            prd_index = []
            mod_index = []
            rct_num = len(rct_list)
            prd_num = len(prd_list)
            mod_num = len(mod_list)


            for j in range(rct_num):
                try:
                    rct.append(df_NodeData.iloc[int(rct_list[j])]['id'])
                    rct_index.append(df_NodeData.iloc[int(rct_list[j])]['idx'])
                except:
                    rct_num = 0
            for j in range(prd_num):
                try:
                    prd.append(df_NodeData.iloc[int(prd_list[j])]['id'])
                    prd_index.append(df_NodeData.iloc[int(prd_list[j])]['idx'])
                except:
                    prd_num = 0
            for j in range(mod_num):
                try:
                    mod.append(df_NodeData.iloc[int(mod_list[j])]['id'])
                    mod_index.append(df_NodeData.iloc[int(mod_list[j])]['idx'])
                except:
                    mod_num = 0

            #calculate center_position and handles by ourselves
            center_x = 0.
            center_y = 0.
            for j in range(rct_num):
                try:
                    src_position = list(df_NodeData.iloc[int(rct_list[j])]['position'][1:-1].split(","))
                    src_dimension = list(df_NodeData.iloc[int(rct_list[j])]['size'][1:-1].split(",")) 
                except:
                    src_position = df_NodeData.iloc[int(rct_list[j])]['position']
                    src_dimension = df_NodeData.iloc[int(rct_list[j])]['size']
                center_x += float(src_position[0])+.5*float(src_dimension[0])
                center_y += float(src_position[1])+.5*float(src_dimension[1])
            for j in range(prd_num):
                try:
                    dst_position = list(df_NodeData.iloc[int(prd_list[j])]['position'][1:-1].split(","))
                    dst_dimension = list(df_NodeData.iloc[int(prd_list[j])]['size'][1:-1].split(",")) 
                except:
                    dst_position = df_NodeData.iloc[int(prd_list[j])]['position']
                    dst_dimension = df_NodeData.iloc[int(prd_list[j])]['size']
                center_x += float(dst_position[0])+.5*float(dst_dimension[0])
                center_y += float(dst_position[1])+.5*float(dst_dimension[1])
            center_x = center_x/(rct_num + prd_num) 
            center_y = center_y/(rct_num + prd_num)
            center_position = [center_x, center_y]
 
            handles = [center_position] #here should be center_handle_position but it is unknown
            for j in range(rct_num):
                src_handle_x = .5*(center_position[0] + float(src_position[0]) + .5*float(src_dimension[0]))
                src_handle_y = .5*(center_position[1] + float(src_position[1]) + .5*float(src_dimension[1]))
                handles.append([src_handle_x,src_handle_y])
            for j in range(prd_num):
                dst_handle_x = .5*(center_position[0] + float(dst_position[0]) + .5*float(dst_dimension[0]))
                dst_handle_y = .5*(center_position[1] + float(dst_position[1]) + .5*float(dst_dimension[1]))
                handles.append([dst_handle_x,dst_handle_y])

            try:
                try:
                    center_pos = list(df_ReactionData.iloc[i]['center_pos'][1:-1].split(","))
                    handles_list_pre = list(df_ReactionData.iloc[i]['handles'][1:-1].split(","))
                except:
                    center_pos = df_ReactionData.iloc[i]['center_pos']
                    handles_list_pre = df_ReactionData.iloc[i]['handles']
                #from excel sheet
                handles_pre = []
                handles = []
                if type(handles_list_pre[0]) is str:
                    for i in range(len(handles_list_pre)):
                        temp = handles_list_pre[i]
                        if temp.find('[') != -1:
                            temp_update = temp.replace('[', '')
                        elif temp.find(']') != -1:
                            temp_update = temp.replace(']', '')
                        handles_pre.append(float(temp_update))
                    for i in range(0,len(handles_pre),2):
                        handles.append([handles_pre[i], handles_pre[i+1]])
                else:
                    handles = handles_list_pre
                #print("export:", handles)
                center_value = [float(center_pos[0]),float(center_pos[1])]
            except:
                center_value = center_position

            reactionCurve = reactionGlyph.getCurve()
            ls = reactionCurve.createLineSegment()
            ls.setStart(libsbml.Point(layoutns, center_value[0], center_value[1]))
            ls.setEnd(libsbml.Point(layoutns, center_value[0], center_value[1]))

            for j in range(rct_num):
                ref_id = "SpecRef_" + reaction_id + "_rct" + str(j)

                speciesReferenceGlyph = reactionGlyph.createSpeciesReferenceGlyph()
                specsRefG_id = "SpecRefG_" + reaction_id + "_rct" + str(j)
                specG_id = "SpecG_" + rct[j] + '_idx_' + str(rct_index[j])
                speciesReferenceGlyph.setId(specsRefG_id)
                speciesReferenceGlyph.setSpeciesGlyphId(specG_id)
                speciesReferenceGlyph.setSpeciesReferenceId(ref_id)
                speciesReferenceGlyph.setRole(libsbml.SPECIES_ROLE_SUBSTRATE)
                speciesReferenceCurve = speciesReferenceGlyph.getCurve()
                cb = speciesReferenceCurve.createCubicBezier()
                cb.setStart(libsbml.Point(layoutns, center_value[0], center_value[1]))
                handle1 = handles[0]
                handle2 = handles[j+1]
                cb.setBasePoint1(libsbml.Point(layoutns, handle1[0], handle1[1]))
                cb.setBasePoint2(libsbml.Point(layoutns, handle2[0], handle2[1]))

                try:
                    src_position = list(df_NodeData.iloc[int(rct_list[j])]['position'][1:-1].split(","))
                    src_dimension = list(df_NodeData.iloc[int(rct_list[j])]['size'][1:-1].split(",")) 
                except:
                    src_position = df_NodeData.iloc[int(rct_list[j])]['position']
                    src_dimension = df_NodeData.iloc[int(rct_list[j])]['size']
                pos_x = float(src_position[0])
                pos_y = float(src_position[1])
                width = float(src_dimension[0])
                height = float(src_dimension[1])
                cb.setEnd(libsbml.Point(layoutns, pos_x + 0.5*width, pos_y - 0.5*height))

            for j in range(prd_num):
                ref_id = "SpecRef_" + reaction_id + "_prd" + str(j)
                speciesReferenceGlyph = reactionGlyph.createSpeciesReferenceGlyph()
                specsRefG_id = "SpecRefG_" + reaction_id + "_prd" + str(j)
                specG_id = "SpecG_" + prd[j]  + '_idx_' + str(prd_index[j])
                speciesReferenceGlyph.setId(specsRefG_id)
                speciesReferenceGlyph.setSpeciesGlyphId(specG_id)
                speciesReferenceGlyph.setSpeciesReferenceId(ref_id)
                speciesReferenceGlyph.setRole(libsbml.SPECIES_ROLE_PRODUCT)

                speciesReferenceCurve = speciesReferenceGlyph.getCurve()
                cb = speciesReferenceCurve.createCubicBezier()
                cb.setStart(libsbml.Point(layoutns, center_value[0], center_value[1]))
                handle1 = handles[0]
                handle2 = handles[rct_num+1+j]
                cb.setBasePoint1(libsbml.Point(layoutns, handle1[0], handle1[1]))
                cb.setBasePoint2(libsbml.Point(layoutns, handle2[0], handle2[1]))
                

                try:
                    dst_position = list(df_NodeData.iloc[int(prd_list[j])]['position'][1:-1].split(","))
                    dst_dimension = list(df_NodeData.iloc[int(prd_list[j])]['size'][1:-1].split(","))
                except:
                    dst_position = df_NodeData.iloc[int(prd_list[j])]['position']
                    dst_dimension = df_NodeData.iloc[int(prd_list[j])]['size']     

                pos_x = float(dst_position[0])
                pos_y = float(dst_position[1])
                width = float(dst_dimension[0])
                height = float(dst_dimension[1])
                cb.setEnd(libsbml.Point(layoutns, pos_x + 0.5*width, pos_y - 0.5*height))

            for j in range(mod_num):
                ref_id = "SpecRef_" + reaction_id + "_mod" + str(j)
                speciesReferenceGlyph = reactionGlyph.createSpeciesReferenceGlyph()
                specsRefG_id = "SpecRefG_" + reaction_id + "_mod" + str(j)
                specG_id = "SpecG_" + mod[j]  + '_idx_' + str(mod_index[j])
                speciesReferenceGlyph.setId(specsRefG_id)
                speciesReferenceGlyph.setSpeciesGlyphId(specG_id)
                speciesReferenceGlyph.setSpeciesReferenceId(ref_id)
                speciesReferenceGlyph.setRole(libsbml.SPECIES_ROLE_MODIFIER)

        for i in range(numArbitraryTexts):
            txt_content = df_TextData.iloc[i]['txt_content'] 
            try:
                position_list = list(df_TextData.iloc[i]['txt_position'][1:-1].split(","))
                size_list = list(df_TextData.iloc[i]['txt_size'][1:-1].split(","))
            except:
                position_list = df_TextData.iloc[i]['txt_position']
                size_list = df_TextData.iloc[i]['txt_size'] 

            textGlyph = layout.createTextGlyph()
            textG_id = "TextG_" + txt_content + '_idx_' + str(i)
            textGlyph.setId(textG_id)
            textGlyph.setText(txt_content)
            bb_id  = "bb_spec_text_" + txt_content + '_idx_' + str(i)
            pos_x_text  = float(position_list[0])
            pos_y_text  = float(position_list[1])
            width_text  = float(size_list[0])
            height_text = float(size_list[1])
            textGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))

        #arbitrary shape
        for i in range(numArbitraryShapes):
            gen_shape_name = str(df_ShapeData.iloc[i]['shape_name']) 
            try:
                position_list = list(df_ShapeData.iloc[i]['position'][1:-1].split(","))
                size_list = list(df_ShapeData.iloc[i]['size'][1:-1].split(","))
            except:
                position_list = df_ShapeData.iloc[i]['position']
                size_list = df_ShapeData.iloc[i]['size'] 

            genGlyph = layout.createGeneralGlyph()
            genG_id = gen_shape_name
            genGlyph.setId(genG_id)
            bb_id  = "bb_spec_text_" + gen_shape_name + '_idx_' + str(i)
            pos_x_text  = float(position_list[0])
            pos_y_text  = float(position_list[1])
            width_text  = float(size_list[0])
            height_text = float(size_list[1])
            genGlyph.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x_text, pos_y_text, width_text, height_text))


        sbmlStr_layout = libsbml.writeSBMLToString(document) #sbmlStr_layout is w layout info but w/o render info

        doc = libsbml.readSBMLFromString(sbmlStr_layout)
        model_layout = doc.getModel()
        mplugin = model_layout.getPlugin("layout")

        # add render information to the first layout
        layout = mplugin.getLayout(0)

        rPlugin = layout.getPlugin("render")

        uri = libsbml.RenderExtension.getXmlnsL2() if doc.getLevel() == 2 else libsbml.RenderExtension.getXmlnsL3V1V1();

        #enable render package
        doc.enablePackage(uri, "render", True)
        doc.setPackageRequired("render", False)

        rPlugin = layout.getPlugin("render")

        rInfo = rPlugin.createLocalRenderInformation()
        rInfo.setId("info")
        rInfo.setName("Render Information")
        rInfo.setProgramName("RenderInformation")
        rInfo.setProgramVersion("1.0")
        
        if numCompartments != 0:  
            for i in range(numCompartments):
                comp_id = df_CompartmentData.iloc[i]['id']
                if comp_id != '_compartment_default':
                    try:
                        fill_color   = list(df_CompartmentData.iloc[i]['fill_color'][1:-1].split(","))
                        border_color = list(df_CompartmentData.iloc[i]['border_color'][1:-1].split(","))
                    except:    
                        fill_color   = df_CompartmentData.iloc[i]['fill_color']
                        border_color = df_CompartmentData.iloc[i]['border_color']
                    comp_border_width = float(df_CompartmentData.iloc[i]['border_width'])
                    if len(fill_color) == 4:
                        fill_color_str    = '#%02x%02x%02x%02x' % (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]),int(fill_color[3]))
                    elif len(fill_color) == 3:
                        fill_color_str    = '#%02x%02x%02x' % (int(fill_color[0]),int(fill_color[1]),int(fill_color[2]))
                   
                    if len(border_color) == 4:    
                        border_color_str  = '#%02x%02x%02x%02x' % (int(border_color[0]),int(border_color[1]),int(border_color[2]),int(border_color[3]))
                    elif len(border_color) == 3:
                        border_color_str  = '#%02x%02x%02x' % (int(border_color[0]),int(border_color[1]),int(border_color[2]))


                    color = rInfo.createColorDefinition()
                    color.setId("comp_fill_color" + "_" + comp_id)
                    color.setColorValue(fill_color_str)

                    color = rInfo.createColorDefinition()
                    color.setId("comp_border_color" + "_" + comp_id)
                    color.setColorValue(border_color_str)

                    # add a list of styles 
                    style = rInfo.createStyle("compStyle" + "_" + comp_id)
                    style.getGroup().setFillColor("comp_fill_color" + "_" + comp_id)
                    style.getGroup().setStroke("comp_border_color" + "_" + comp_id)
                    style.getGroup().setStrokeWidth(comp_border_width)
                    style.addType("COMPARTMENTGLYPH")
                    style.addId(comp_id)
                    rectangle = style.getGroup().createRectangle()
                    rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                    libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))

        else:
            comp_border_width = 2.
            #set default compartment with white color
            fill_color_str = '#ffffffff'
            border_color_str = '#ffffffff'

            color = rInfo.createColorDefinition()
            color.setId("comp_fill_color")
            color.setColorValue(fill_color_str)

            color = rInfo.createColorDefinition()
            color.setId("comp_border_color")
            color.setColorValue(border_color_str)

            # add a list of styles 
            style = rInfo.createStyle("compStyle")
            style.getGroup().setFillColor("comp_fill_color")
            style.getGroup().setStroke("comp_border_color")
            style.getGroup().setStrokeWidth(comp_border_width)
            style.addType("COMPARTMENTGLYPH")
            style.addId(comp_id)
            rectangle = style.getGroup().createRectangle()
            rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
            libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))

        for i in range(numNodes):
            gradient_type = ''
            spec_id = df_NodeData.iloc[i]['id']  
            spec_shapeIdx = int(df_NodeData.iloc[i]['shape_idx'])
            spec_shapeType = df_NodeData.iloc[i]['shape_type']

            try:
                spec_shapeInfo_list_pre = list(df_NodeData.iloc[i]['shape_info'][1:-1].split(","))
            except:
                spec_shapeInfo_list_pre = df_NodeData.iloc[i]['shape_info']
            if spec_shapeInfo_list_pre == ['']:
                spec_shapeInfo = []
            elif len(spec_shapeInfo_list_pre) == 0:
                spec_shapeInfo = []
            else:
                spec_shapeInfo_pre = []
                spec_shapeInfo = []
                if type(spec_shapeInfo_list_pre[0]) is str:
                    for ii in range(len(spec_shapeInfo_list_pre)):
                        temp = spec_shapeInfo_list_pre[ii]
                        if temp.find('[') != -1:
                            temp_update = temp.replace('[', '')
                        elif temp.find(']') != -1:
                            temp_update = temp.replace(']', '')
                        spec_shapeInfo_pre.append(float(temp_update))
                    for ii in range(0,len(spec_shapeInfo_pre),2):
                        spec_shapeInfo.append([spec_shapeInfo_pre[ii], spec_shapeInfo_pre[ii+1]])
                else:
                    spec_shapeInfo = spec_shapeInfo_list_pre

            try: 
                try:
                    spec_fill_color   = list(df_NodeData.iloc[i]['fill_color'][1:-1].split(","))
                    spec_border_color = list(df_NodeData.iloc[i]['border_color'][1:-1].split(","))
                except:
                    spec_fill_color   = df_NodeData.iloc[i]['fill_color']
                    spec_border_color = df_NodeData.iloc[i]['border_color']
                if len(spec_fill_color) == 4:
                    spec_fill_color_str   = '#%02x%02x%02x%02x' % (int(spec_fill_color[0]),int(spec_fill_color[1]),int(spec_fill_color[2]),int(spec_fill_color[3]))
                elif len(spec_fill_color) == 3 and type(spec_fill_color[0]) != str:
                    spec_fill_color_str   = '#%02x%02x%02x' % (int(spec_fill_color[0]),int(spec_fill_color[1]),int(spec_fill_color[2]))
                elif len(spec_fill_color) and type(spec_fill_color[0]) == str:
                    gradient_type = spec_fill_color[0]
                    gradient_info = spec_fill_color[1]
                    stop_info = spec_fill_color[2]  

                if len(spec_border_color) == 4:    
                    spec_border_color_str = '#%02x%02x%02x%02x' % (int(spec_border_color[0]),int(spec_border_color[1]),int(spec_border_color[2]),int(spec_border_color[3]))
                elif len(spec_border_color) == 3:
                    spec_border_color_str = '#%02x%02x%02x' % (int(spec_border_color[0]),int(spec_border_color[1]),int(spec_border_color[2]))   

                spec_border_width = float(df_NodeData.iloc[i]['border_width'])

                try:
                    font_color = list(df_NodeData.iloc[i]['txt_font_color'][1:-1].split(","))
                except:
                    font_color = df_NodeData.iloc[i]['txt_font_color']
                if len(font_color) == 4:
                    text_line_color_str =  '#%02x%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]),int(font_color[3]))
                elif len(font_color) == 3:
                    text_line_color_str =  '#%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]))
                text_line_width = float(df_NodeData.iloc[i]['txt_line_width'])
                text_font_size = float(df_NodeData.iloc[i]['txt_font_size'])
            except: #text-only: set default species/node with white color
                spec_fill_color_str = '#ffffffff'
                spec_border_color_str = '#ffffffff'
                spec_border_width = 2.
                text_line_color_str = '#000000ff'
                text_line_width = 1.
                text_font_size = 12.

            if gradient_type == '':
                color = rInfo.createColorDefinition()
                color.setId("spec_fill_color" + "_" + spec_id)
                color.setColorValue(spec_fill_color_str)

                color = rInfo.createColorDefinition()
                color.setId("spec_border_color" + "_" + spec_id)
                color.setColorValue(spec_border_color_str)

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + spec_id)
                color.setColorValue(text_line_color_str)

                style = rInfo.createStyle("specStyle" + "_" + spec_id)
                style.getGroup().setFillColor("spec_fill_color" + "_" + spec_id)
                style.getGroup().setStroke("spec_border_color" + "_" + spec_id)
                style.getGroup().setStrokeWidth(spec_border_width)
                style.addType("SPECIESGLYPH")
                style.addId(spec_id)
            elif gradient_type == 'linearGradient':
                color = rInfo.createColorDefinition()
                color.setId("spec_border_color" + "_" + spec_id)
                color.setColorValue(spec_border_color_str)

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + spec_id)
                color.setColorValue(text_line_color_str)

                gradient = rInfo.createLinearGradientDefinition()
                gradient.setId("spec_fill_gradient" + "_" + spec_id)
                gradient.setPoint1(libsbml.RelAbsVector(0, gradient_info[0][0]), libsbml.RelAbsVector(0, gradient_info[0][1]))
                gradient.setPoint2(libsbml.RelAbsVector(0, gradient_info[1][0]), libsbml.RelAbsVector(0, gradient_info[1][1]))

                for ii in range(len(stop_info)):
                    color = rInfo.createColorDefinition()
                    stop_color_id = "spec_fill_stop_color" + "_" + spec_id + '_' + str(ii)
                    color.setId(stop_color_id)
                    stop_color = stop_info[ii][1]
                    spec_fill_stop_color_str = '#%02x%02x%02x%02x' % (int(stop_color[0]),int(stop_color[1]),int(stop_color[2]),int(stop_color[3]))
                    color.setColorValue(spec_fill_stop_color_str)

                    stop = gradient.createGradientStop()
                    stop.setOffset(libsbml.RelAbsVector(0, stop_info[ii][0]))
                    stop.setStopColor(stop_color_id)

                style = rInfo.createStyle("specStyle" + "_" + spec_id)
                style.getGroup().setFillColor("spec_fill_gradient" + "_" + spec_id)
                style.getGroup().setStroke("spec_border_color" + "_" + spec_id)
                style.getGroup().setStrokeWidth(spec_border_width)
                style.addType("SPECIESGLYPH")
                style.addId(spec_id)
            elif gradient_type == 'radialGradient':
                color = rInfo.createColorDefinition()
                color.setId("spec_border_color" + "_" + spec_id)
                color.setColorValue(spec_border_color_str)

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + spec_id)
                color.setColorValue(text_line_color_str)

                gradient = rInfo.createRadialGradientDefinition()
                gradient.setId("spec_fill_gradient" + "_" + spec_id)
                gradient.setCenter(libsbml.RelAbsVector(0, gradient_info[0][0]), libsbml.RelAbsVector(0, gradient_info[0][1]))
                gradient.setRadius(libsbml.RelAbsVector(0, gradient_info[1][0]))

                for ii in range(len(stop_info)):
                    color = rInfo.createColorDefinition()
                    stop_color_id = "spec_fill_stop_color" + "_" + spec_id + '_' + str(ii)
                    color.setId(stop_color_id)
                    stop_color = stop_info[ii][1]
                    spec_fill_stop_color_str = '#%02x%02x%02x%02x' % (int(stop_color[0]),int(stop_color[1]),int(stop_color[2]),int(stop_color[3]))
                    color.setColorValue(spec_fill_stop_color_str)

                    stop = gradient.createGradientStop()
                    stop.setOffset(libsbml.RelAbsVector(0, stop_info[ii][0]))
                    stop.setStopColor(stop_color_id)

                style = rInfo.createStyle("specStyle" + "_" + spec_id)
                style.getGroup().setFillColor("spec_fill_gradient" + "_" + spec_id)
                style.getGroup().setStroke("spec_border_color" + "_" + spec_id)
                style.getGroup().setStrokeWidth(spec_border_width)
                style.addType("SPECIESGLYPH")
                style.addId(spec_id)


            if spec_shapeIdx == 1 or spec_shapeType == 'rectangle': #rectangle
                rectangle = style.getGroup().createRectangle()
                rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))

            elif spec_shapeType == 'polygon':            
                polygon = style.getGroup().createPolygon()
                for pts in range(len(spec_shapeInfo)):
                    renderPoint = polygon.createPoint()
                    renderPoint.setCoordinates(libsbml.RelAbsVector(0,spec_shapeInfo[pts][0]),
                    libsbml.RelAbsVector(0,spec_shapeInfo[pts][1]))

            elif spec_shapeIdx == 2 or spec_shapeType == 'ellipse':
                ellipse = style.getGroup().createEllipse()
                ellipse.setCenter2D(libsbml.RelAbsVector(0, 50.), libsbml.RelAbsVector(0, 50.))
                ellipse.setRadii(libsbml.RelAbsVector(0, 50.),libsbml.RelAbsVector(0, 50.))
                # try: #from dataFrame
                #     ellipse = style.getGroup().createEllipse()
                #     ellipse.setCenter2D(libsbml.RelAbsVector(0, spec_shapeInfo[0][0][0]), 
                #     libsbml.RelAbsVector(0, spec_shapeInfo[0][0][1]))
                #     ellipse.setRadii(libsbml.RelAbsVector(0, spec_shapeInfo[0][1][0]),
                #     libsbml.RelAbsVector(0, spec_shapeInfo[0][1][1]))
                #     #percentage of width
                # except: #from excel sheet
                #     ellipse = style.getGroup().createEllipse()
                #     ellipse.setCenter2D(libsbml.RelAbsVector(0, spec_shapeInfo[0][0]), 
                #     libsbml.RelAbsVector(0, spec_shapeInfo[0][1]))
                #     ellipse.setRadii(libsbml.RelAbsVector(0, spec_shapeInfo[1][0]),
                #     libsbml.RelAbsVector(0, spec_shapeInfo[1][1]))

            
            style = rInfo.createStyle("textStyle")
            style.getGroup().setStroke("text_line_color" + "_" + spec_id)
            style.getGroup().setStrokeWidth(text_line_width)
            style.getGroup().setFontSize(libsbml.RelAbsVector(text_font_size,0))
            style.addType("TEXTGLYPH")
            style.addId(spec_id)

        if numReactions != 0:
            for i in range(numReactions):
                rxn_id = df_ReactionData.iloc[i]['id']
                try:
                    reaction_fill_color = list(df_ReactionData.iloc[i]['fill_color'][1:-1].split(","))
                except:
                    reaction_fill_color = df_ReactionData.iloc[i]['fill_color']
                
                if len(reaction_fill_color) == 4:
                    reaction_fill_color_str = '#%02x%02x%02x%02x' % (int(reaction_fill_color[0]),int(reaction_fill_color[1]),int(reaction_fill_color[2]),int(reaction_fill_color[3]))           
                elif len(reaction_fill_color) == 3:
                    reaction_fill_color_str = '#%02x%02x%02x' % (int(reaction_fill_color[0]),int(reaction_fill_color[1]),int(reaction_fill_color[2]))           
                reaction_line_thickness = float(df_ReactionData.iloc[i]['line_thickness'])
                try:
                    reaction_arrow_head_size = list(df_ReactionData.iloc[i]['arrow_head_size'][1:-1].split(","))
                except:
                    reaction_arrow_head_size = df_ReactionData.iloc[i]['arrow_head_size']

                try:
                    reaction_dash = list(df_ReactionData.iloc[i]['rxn_dash'][1:-1].split(","))
                except:
                    reaction_dash = list(df_ReactionData.iloc[i]['rxn_dash'])

                color = rInfo.createColorDefinition()
                color.setId("reaction_fill_color" + "_" + rxn_id)
                color.setColorValue(reaction_fill_color_str)

                style = rInfo.createStyle("reactionStyle" + "_" + rxn_id)
                style.getGroup().setStroke("reaction_fill_color" + "_" + rxn_id)
                style.getGroup().setStrokeWidth(reaction_line_thickness)
                if len(reaction_dash) != 0:
                    for pt in range(len(reaction_dash)):
                        try:
                            style.getGroup().addDash(int(reaction_dash[pt]))
                        except:
                            pass
                style.addType("REACTIONGLYPH SPECIESREFERENCEGLYPH")
                style.addId(rxn_id)

                #arrowHead
                lineEnding = rInfo.createLineEnding()
                lineEnding.setId("reaction_arrow_head" + "_" + rxn_id)
                lineEnding.setEnableRotationalMapping(True)
                bb_id = "bb_" + rxn_id
                pos_x = 0
                pos_y = 0
                width = float(reaction_arrow_head_size[0])
                height = float(reaction_arrow_head_size[1])
                lineEnding.setBoundingBox(libsbml.BoundingBox(layoutns, bb_id, pos_x, pos_y, width, height))

                # polygon = lineEnding.getGroup().createPolygon()
                # renderPoint1 = polygon.createPoint()
                # renderPoint1.setCoordinates(libsbml.RelAbsVector(0,100), libsbml.RelAbsVector(0,50))
                # renderPoint2 = polygon.createPoint()
                # renderPoint2.setCoordinates(libsbml.RelAbsVector(0,0), libsbml.RelAbsVector(0,0))
                # renderPoint3 = polygon.createPoint()
                # renderPoint3.setCoordinates(libsbml.RelAbsVector(0,0), libsbml.RelAbsVector(0,50))
                # renderPoint4 = polygon.createPoint()
                # renderPoint4.setCoordinates(libsbml.RelAbsVector(0,0), libsbml.RelAbsVector(0,100))

                style.getGroup().setEndHead("reaction_arrow_head" + "_" + rxn_id)

        if numArbitraryTexts != 0:
            for i in range(numArbitraryTexts):
                text_content = df_TextData.iloc[i]['txt_content']  

                try: 
                    try:
                        font_color = list(df_TextData.iloc[i]['txt_font_color'][1:-1].split(","))
                    except:
                        font_color = df_TextData.iloc[i]['txt_font_color']
                    if len(font_color) == 4:
                        text_line_color_str =  '#%02x%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]),int(font_color[3]))
                    elif len(font_color) == 3:
                        text_line_color_str =  '#%02x%02x%02x' % (int(font_color[0]),int(font_color[1]),int(font_color[2]))
                    text_line_width = float(df_TextData.iloc[i]['txt_line_width'])
                    text_font_size = float(df_TextData.iloc[i]['txt_font_size'])
                except: #text-only: set default species/node with white color
                    text_line_color_str = '#000000ff'
                    text_line_width = 1.
                    text_font_size = 12.

                color = rInfo.createColorDefinition()
                color.setId("text_line_color" + "_" + text_content)
                color.setColorValue(text_line_color_str)
                
                style = rInfo.createStyle("textStyle")
                style.getGroup().setStroke("text_line_color" + "_" + text_content)
                style.getGroup().setStrokeWidth(text_line_width)
                style.getGroup().setFontSize(libsbml.RelAbsVector(text_font_size,0))
                style.addType("TEXTGLYPH")
                style.addId(text_content)

        #arbitrary shape
        if numArbitraryShapes != 0:
            for i in range(numArbitraryShapes):
                gen_shape_name = str(df_ShapeData.iloc[i]['shape_name'])   
                gen_shape_type = df_ShapeData.iloc[i]['shape_type']

                try:
                    gen_shapeInfo_list_pre = list(df_ShapeData.iloc[i]['shape_info'][1:-1].split(","))
                except:
                    gen_shapeInfo_list_pre = df_ShapeData.iloc[i]['shape_info']
                if gen_shapeInfo_list_pre == ['']:
                    gen_shapeInfo = []
                elif len(gen_shapeInfo_list_pre) == 0:
                    gen_shapeInfo = []
                else:
                    gen_shapeInfo_pre = []
                    gen_shapeInfo = []
                    if type(gen_shapeInfo_list_pre[0]) is str:
                        for ii in range(len(gen_shapeInfo_list_pre)):
                            temp = gen_shapeInfo_list_pre[ii]
                            if temp.find('[') != -1:
                                temp_update = temp.replace('[', '')
                            elif temp.find(']') != -1:
                                temp_update = temp.replace(']', '')
                            gen_shapeInfo_pre.append(float(temp_update))
                        for ii in range(0,len(gen_shapeInfo_pre),2):
                            gen_shapeInfo.append([gen_shapeInfo_pre[ii], gen_shapeInfo_pre[ii+1]])
                    else:
                        gen_shapeInfo = gen_shapeInfo_list_pre

                try: 
                    try:
                        gen_fill_color   = list(df_ShapeData.iloc[i]['fill_color'][1:-1].split(","))
                        gen_border_color = list(df_ShapeData.iloc[i]['border_color'][1:-1].split(","))
                    except:
                        gen_fill_color   = df_ShapeData.iloc[i]['fill_color']
                        gen_border_color = df_ShapeData.iloc[i]['border_color']
                    if len(gen_fill_color) == 4:
                        gen_fill_color_str   = '#%02x%02x%02x%02x' % (int(gen_fill_color[0]),
                        int(gen_fill_color[1]),int(gen_fill_color[2]),int(gen_fill_color[3]))
                    elif len(gen_fill_color) == 3:
                        gen_fill_color_str   = '#%02x%02x%02x' % (int(gen_fill_color[0]),
                        int(gen_fill_color[1]),int(gen_fill_color[2]))
                
                    if len(gen_border_color) == 4:    
                        gen_border_color_str = '#%02x%02x%02x%02x' % (int(gen_border_color[0]),
                        int(gen_border_color[1]),int(gen_border_color[2]),int(gen_border_color[3]))
                    elif len(gen_border_color) == 3:
                        gen_border_color_str = '#%02x%02x%02x' % (int(gen_border_color[0]),
                        int(gen_border_color[1]),int(gen_border_color[2]))   

                    gen_border_width = float(df_ShapeData.iloc[i]['border_width'])

                # print(gen_fill_color_str)
                # print(gen_border_color_str)
                # print(gen_border_width)

                except: #set default shape border color as black, fill color as white
                    gen_fill_color_str = '#ffffffff'
                    gen_border_color_str = '#000000ff'
                    gen_border_width = 2.


                color = rInfo.createColorDefinition()
                color.setId("gen_fill_color" + "_" + gen_shape_name)
                color.setColorValue(gen_fill_color_str)

                color = rInfo.createColorDefinition()
                color.setId("gen_border_color" + "_" + gen_shape_name)
                color.setColorValue(gen_border_color_str)


                style = rInfo.createStyle("genStyle" + "_" + gen_shape_name)
                style.getGroup().setFillColor("gen_fill_color" + "_" + gen_shape_name)
                style.getGroup().setStroke("gen_border_color" + "_" + gen_shape_name)
                style.getGroup().setStrokeWidth(gen_border_width)
                style.addType("GENERALGLYPH")
                style.addId(gen_shape_name)

                if gen_shape_type == 'rectangle': #rectangle
                    rectangle = style.getGroup().createRectangle()
                    rectangle.setCoordinatesAndSize(libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,0),
                    libsbml.RelAbsVector(0,0),libsbml.RelAbsVector(0,100),libsbml.RelAbsVector(0,100))

                elif gen_shape_type == 'polygon':            
                    polygon = style.getGroup().createPolygon()
                    for pts in range(len(gen_shapeInfo)):
                        renderPoint = polygon.createPoint()
                        renderPoint.setCoordinates(libsbml.RelAbsVector(0,gen_shapeInfo[pts][0]),
                        libsbml.RelAbsVector(0,gen_shapeInfo[pts][1]))

                elif gen_shape_type == 'ellipse':
                    ellipse = style.getGroup().createEllipse()
                    ellipse.setCenter2D(libsbml.RelAbsVector(0, 50.), libsbml.RelAbsVector(0, 50.))
                    ellipse.setRadii(libsbml.RelAbsVector(0, 50.),libsbml.RelAbsVector(0, 50.))

        sbmlStr_layout_render = libsbml.writeSBMLToString(doc) #sbmlStr_layout_render includes both layout and render
    
        return sbmlStr_layout_render
    else:
        raise ValueError('There is no node or arbitrary text or arbitrary shape!')



if __name__ == '__main__':

    DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FOLDER = os.path.join(DIR, "initiate_excel_files")

#     # df_CompartmentData = pd.read_csv(os.path.join(TEST_FOLDER, 'CompartmentData.csv')) 
#     # df_NodeData = pd.read_csv(os.path.join(TEST_FOLDER, 'NodeData.csv'))
#     # df_ReactionData = pd.read_csv(os.path.join(TEST_FOLDER, 'ReactionData.csv'))

    xls = pd.ExcelFile(os.path.join(TEST_FOLDER, 'output.xlsx'))
    df_CompartmentData = pd.read_excel(xls, 'CompartmentData')
    df_NodeData = pd.read_excel(xls, 'NodeData')
    df_ReactionData = pd.read_excel(xls, 'ReactionData')
    df_ArbitraryTextData = pd.read_excel(xls, "ArbitraryTextData")
    df_ArbitraryShapeData = pd.read_excel(xls, "ArbitraryShapeData")

    df = (df_CompartmentData, df_NodeData, df_ReactionData, df_ArbitraryTextData, df_ArbitraryShapeData)

    sbmlStr_layout_render = _DFToSBML(df)

    f = open("output.xml", "w")
    f.write(sbmlStr_layout_render)
    f.close()
        
