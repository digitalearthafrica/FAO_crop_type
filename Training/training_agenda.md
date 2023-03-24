# FAO EOSTAT: calculating cropo acreage using Earth Observations data for the modernization of National Statistics Offices.

Earth Observations (EO) data has been early recognized by the UN Statistical as key source of Big Data that can be used as an integration and/or alternative to traditional statistical methods to produce crop statistics, and therefore support the modernization of national statistical systems. In particular, EO data can be used to produce crop type maps that are accurate, timely and granular, allowing for the calculation of crop acreage, and crop yield when coupled with crop growth models. Furthemore EO data allow for the early estimates of crop acreage and yield.

Despite the advances in technology and the unprecedented abundance , the of EO data into national operational contexts is still low due to the technical and administrative barriers that are still found. As a result crop type maps, crop yield maps and crop boundary maps are rare to find in countries, and when available they are not regularly kept up-to-date. 

To increase the uptake of EO data for official statistics in countries, FAO has launched the EOSTAT project in 2019 with the scope of developing a novel, simplified and standardized EO approach and to use it to build technical capacity in countries through the implementation of pilot projects. EOSTAT outputs are typically national land cover maps, crop masks, crop type maps, crop yield maps and crop field boundary maps, which in turn feed into the FAO Hand in Hand Initiative. Mozambique is a beneficiary of the EOSTAT project and is participating to the HiH initiative. 

To amplify the outreach of the EOSTAT project,  FAO has established a collaboration with Digital Earth Africa (DE Africa) and with Frontier SI who will is the implementing partner in Rwanda and Mozambique.   

## Digital Earth Africa platform

The workflow developed in this project uses the Earth observation data available from the DE Africa platform. The scripts are designed to operate in the [Digital Earth Africa sandbox](https://sandbox.digitalearth.africa/).

Support on using DE Africa platform is available through the [DE Africa Help Desk](https://docs.digitalearthafrica.org/en/latest/about/contact.html).

## Crop type mapping

The crop type mapping workflow implements a supervised machine learning (ML) approach with the following main components:

* Training data cleaning and inspection
* Extraction of input features and feature engineering
* Building a ML classifier
* Generation of a crop type map

**Add a flowchat**

Each of these components can be tuned and refined based on type of training data available and the climate and cropping characteristics of the region of interest.

## Training sessions

The first training session explores how to inspect and clean the training data for building a machine learning model using Earth observations.

1. [Training data inspection](../1_Training_data_inspection.ipynb) - inspection of crop labels and preprocessing of training labels
2. [Phenology exploration](../2_Phenology_exploration.ipynb) - inspection of NDVI phenology curves for different crop classes
3. [Training feature extraction](../3_Training_feature_extraction.ipynb) - extraction of relevant EO measurements over training data locations
4. [Feature selection](../4_Training_feature_selection.ipynb) - inspection of training features for correlation and selection of features

The second training session covers how to use the training data and Earth observations from the DE Africa platform to build a machine learning model, and apply it to produce a crop type map.

5. [Fit, optimise and evaluate classifier](../5_Fit_classifier.ipynb) - model fitting and cross validation
6. [Model prediction and post-processing](../6_Create_test_map.ipynb) - generation of test maps over a small areas for visual inspection
7. [Country-wide crop type map](../7_Create_country_map.ipynb) - generation of a country-wide crop type map
8. [Crop area statistics](../8_Calculate_crop_statistics.ipynb) - generation of crop area statistics
