# FAO EOSTAT: calculating cropo acreage using Earth Observations data for the modernization of National Statistics Offices.

Earth Observations (EO) data has been early recognized by the UN Statistical as key source of Big Data that can be used as an integration and/or alternative to traditional statistical methods to produce crop statistics, and therefore support the modernization of national statistical systems. In particular, EO data can be used to produce crop type maps that are accurate, timely and granular, allowing for the calculation of crop acreage, and crop yield when coupled with crop growth models. Furthemore EO data allow for the early estimates of crop acreage and yield.

Despite the advances in technology, the unprecedented abundance of free and open EO data, and the availability of extensive machine learnign and AI libraries, still the uptake of EO data by operational contexts in countries is still low due to a series of technical and administrative barriers. As a result crop masks, crop type maps, crop yield maps and crop boundary maps are rare to find in countries, and when available they are often not validated and obsolete.  

In this context, FAO has launched the EOSTAT project in 2019 with the overall scope of supporting National Statistics Offices in countries to uptake EO data for official crop statistics. Througbh EOSTAT, a simplified yet rigorous and standardized  approach has been developed, that overcomes the such challanges commonly found. Through the delivery of a comprehensive technical capacity program EOSTAT ius bmplify its outreach and ansure that the best solutions are made available to the end user, FAO has established collaborations with key international partners under the framework of the EOSTAT project including the European Space Agency, the University of Louvain, the Mighigan State University, the GEO, the UN Big Data Platform and the Digital Earth Africa. 

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
