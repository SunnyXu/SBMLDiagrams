.. _Tutorial:
 

Tutorial
=============

1) Load and visualize an SBML file.

.. code-block:: python

   import SBMLDiagrams
   import tellurium as te

   r = te.loada ('''
   A -> B; v; B -> C; v; C -> D; v;
   v = 0
   ''')

   df = SBMLDiagrams.load(r.getSBML())
   df.autolayout()
   df.draw()


2) Load, read, edit and export to an SBML file.

.. code-block:: python

   import SBMLDiagrams
   import os

   dirname = "path//to"
   filename = "SBML_file.xml"

   with open(os.path.join(dirname, filename), 'r', encoding="utf8") as f:
        sbmlStr = f.read()      

   df = SBMLDiagrams.load(sbmlStr)

   #get layout
   print(df.getCompartmentPosition("compartment_id"))
   print(df.getNodeSize("node_id"))
   print(df.getReactionCenterPosition("reaction_id"))

   #get render
   print(df.getCompartmentFillColor("compartment_id"))
   print(df.getNodeShape("node_id"))
   print(df.getReactionFillColor("reaction_id"))

   #set layout
   df.setCompartmentSize(("compartment_id", [100, 100])
   df.setNodeTextPosition(("node_id", [30, 30])

   #set render
   # There are three ways to set colors and the opacity is optional:
   # 1) list-decimal rgb 1*3 matrix, i.e. [255, 255, 255];
   # 2) str-html name, i.e. "white";
   # 3) str-hex string (6-digit), i.e. "#000000";
   df.setCompartmentBorderColor("compartment_id", [255, 255, 255])
   df.setNodeFillColor("node_id", "red", opacity = 0.5)
   df.setNodeTextFontColor("node_id", "#000000", opacity = 1.)
   df.setReactionLineThickness("reaction_id", 3.)

   sbmlStr_layout_render = df.export()
   f = open("output.xml", "w")
   f.write(sbmlStr_layout_render)
   f.close()

3) Load the color style information from a JSON file..

.. code-block:: python

   import SBMLDiagrams
   import tellurium as te

   colors = SBMLDiagrams.loadColorStyle("style.json")
   r = te.loada('''
      A -> B; k1*A
      B -> C; k2*B
      k1 = 0.1; k2 = 0.2; A = 10
   ''')

   sbmlStr = r.getSBML()
   df = SBMLDiagrams.load(sbmlStr)

   df.setColorStyle(colors["simplicity"])
   df.draw(output_fileName="load_json_style/simplicity-color.png")

   df.setColorStyle(colors["skyblue"])
   df.draw(output_fileName="load_json_style/skyblue-color.png")
   

The file style.json:

.. code-block:: python

   {
   "colorStyle": [
      {
         "style_name": "simplicity",
         "compartment_fill_color": "255, 255, 255, 255",
         "compartment_border_color": "255, 255, 255, 255",
         "species_fill_color": "255, 255, 255, 255",
         "species_border_color": "0, 0, 0, 255",
         "reaction_line_color": "0, 0, 0, 255",
         "font_color": "0, 0, 0, 255",
         "progress_bar_fill_color": "255, 108, 9, 200",
         "progress_bar_full_fill_color": "91, 176, 253, 200",
         "progress_bar_border_color": "255, 204, 153, 200"
      },

      {
         "style_name": "skyblue",
         "compartment_fill_color": "3, 219, 252, 255",
         "compartment_border_color": "3, 219, 252, 255",
         "species_fill_color": "23, 107, 252, 255",
         "species_border_color": "119, 3, 252, 255",
         "reaction_line_color": "3, 252, 157, 255",
         "font_color": "0, 0, 0, 255",
         "progress_bar_fill_color": "255, 108, 9, 200",
         "progress_bar_full_fill_color": "91, 176, 253, 200",
         "progress_bar_border_color": "255, 204, 153, 200"
      }
   ]   
   }
