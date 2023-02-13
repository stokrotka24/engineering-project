# Comparison of selected recommendation algorithms on the example of a hotel recommendation system

## Overview
Repository for my engineering thesis carried out at Wrocław University of Science and Technology.

The recommendation system consists of mobile app, REST API, database and recommendation engine. The architecture of the created system allows to use and test different recommendation algorithms. A literature review in the subject of recommendation systems was made and the following algorithms were implemented: collaborative filtering algorithm, content based algorithm and hybrid algorithm. Then a comparative analysis of the algorithms for real user ratings for hotels was carried out and results and conclusions were described.

## Content
The `frontend` directory contains the mobile application implementation including the Kotlin source code and the necessary configuration files.

The server application implementation is located in the following subdirectories of the `backend` directory: `authorization`, `hotels` and `server`.

The source code of the recommendation engine is located in the `backend/algorithms` directory. The `backend/algorithms/test` directory contains the data of the experiments performed, divided into the following subdirectories: 
* `filtered_results` – directory containing text files with algorithm results for a set of active users.
* `results` – directory containing text files with algorithm results for the entire test set.
* `graphs` – directory containing graphs of the test statistics based on the performed tests.

The algorithm tests were performed on [Yelp academic dataset](https://www.yelp.com/dataset).

The `backend/data` directory contains scripts that generate command text files for inserting data from the Yelp academic dataset into the database. For the scripts to work correctly, the Yelp dataset must be placed in the `backend/data/yelp-academic-dataset` directory. 

The `backend/config-scripts` directory contains scripts that insert data into the database based on the command text files mentioned above.

## Technologies

![Python](https://img.shields.io/badge/python-v3.10.5-green.svg)
![Kotlin](https://img.shields.io/badge/kotlin-v1.7.0-orange.svg)
![Retrofit](https://img.shields.io/badge/retrofit-v2.9.0-red.svg)

[<img target="_blanket" src="https://www.django-rest-framework.org/img/logo.png" height=150>](https://www.django-rest-framework.org/)
[<img target="_blanket" src="https://numpy.org/doc/stable/_static/numpylogo.svg" height=150>](https://numpy.org/doc/stable/index.html)
[<img target="_blanket" src="https://docs.scipy.org/doc/scipy/_static/logo.svg" height=150>](https://docs.scipy.org/doc/scipy/getting_started.html)
[<img target="_blanket" src="https://matplotlib.org/_static/images/logo2.svg" height=100>](https://matplotlib.org/)
[<img target="_blanket" src="https://webimages.mongodb.com/_com_assets/cms/kuyjf3vea2hg34taa-horizontal_default_slate_blue.svg?auto=format%252Ccompress" height=100>](https://www.mongodb.com/)

