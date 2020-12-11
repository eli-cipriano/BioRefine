# BioRefine


## The Problem:

Biorefine is a tool for exploring the variety of published biotechnology platforms that are available for the renewable production of fuels and chemicals. These platforms, or "bioprocesses", are often presented as linear a sequence of physical and chemical operations applied to some form of carbon to produce a valuable product. 

*For example:*

Corn is often used in the industrial production of ethanol, a potential biofuel. The corn is mechanically processed to extract the fermentable sugar (glucose) from the starchy parts of the plant, and then the sugars are anaerobically fermented by yeast, which have often been genetically modified to produce higher concentrations of ethanol per gram of glucose consumed. This process is **linear** because it has one carbon source (glucose) and one product (ethanol). 

This trend of linear bioprocessing is one of the biggest challenges for achieving a circular economy of resources through the biocatalysis of plant materials. Looking at the fossil fuel industry, one would find that there is nothing linear about it. Crude oil is distilled and separated into dozens of chemical products that are used in the production of fuels, plastics, cosmetics, pharmaceuticals, construction materials, and thousands of extremely high value specialty chemicals. Almost everything in our world is made from petrochemical products, which are more accurately represented as a network of chemicals all originating from a single carbon source: **oil**. 

## What This Program Does:

Our goal with Biorefine is to show how a single crop, such as corn, can be used for the co-production of multiple products. This means that different types of carbon sources from the different parts of the corn plant are all utilized in order to diversify the suite of products available to be made from corn. The terms used to describe these integrated bioprocesses are:

- **material**:   the unrefined resource containing a variety of carbon sources.  
- **side1**:      one carbon source from a material that can be further processed.
- **side2**:      secondary carbon source from a material that can be further processed.
- **substrate**:  a refined carbon source that can be directly fermented or reacted to form a product. *(same for sub1/2)*
- **process**:    a reported organism and fermentation conditions that can convert a specific set of substrates and products. *(same for proc1/2)*
- **product**:    the desired fuel, material, or chemical to be sold, either as a commodity (energy, plastic) or specialty (cosmetic, nutriceutical) product. *(same for prod1/2)*

Considering these terms, which we refer to as "Modular Units" of the bioprocess, our program returns a combination of these Units that can be altered by the user into any possible combination. The available options the user can choose from are selected from a curated list of all the reported biotechnology relating to that specific Unit. For example, if the user were to select "corn" from the ethanol process below, they could change the **material** Modular Unit to be "sugar cane" or "wheat", because these are two other crops that have been reported to produce glucose as their main substrate. Similarly, the list of available values under the **process** Modular Unit only contains classes of biological fermentations that have been reported for the currently selected **product** Modular Unit, which in this case is "ethanol". 

## How to Run:

Make sure all dependencies are installed, which should only be PySimpleGUI. Then just run GUI_biorefine.py from the command line, and you should be good to go. our biorefine.py program was a command-line beta that helped us flesh out our idea. We left it as another option, but it does not have as many features as the GUI and has not been fully debugged.

**tab1: Bioprocess**

Once you are in the GUI window, click a button to set which Modular Unit you would like to change. Then select an option from the drop-down menu. Options will only be available if they are compatible with neighboring Modular Units. You can only change one Modular Unit at a time.

Use the "Load" button to change the current map to a previously saved Bioprocess. Use the "Save & Quit" button to save your current map.

- Files will automatically be saved/loaded to/from the processes/ directory, unless otherwise stated in the file path name.
- The file will save and load JSON files automatically, so do not your own file extension.

When quitting, press OK with no file name to exit without saving. You can also close the window at any point to exit without saving.

**tab2: Details**

Click which Modular Unit you want to see more detailed information about. This information will also be written to a text file upon saving.


**tab3: Custom**

Click which data type you would like to add to. (NOT YET FUNCTIONAL)

- Materials refer to information on converting raw biomass into substrate compounds.
- Sides refer to information on converting by-products of materials into useful substrates as well.
- Substrates refer to information on converting basic compounds into more valuable and refined products.

