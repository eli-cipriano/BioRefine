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

## How to Run This Code
Example run code: 

```python biorefine.py --product ethanol --file J1```
