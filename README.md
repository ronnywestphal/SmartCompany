# SmartCompany
This Django web application is part of a school project at the end of the second year in the Electrical Engineering program at KTH Royal Institute of Technology.

The course objective is to create an IoT device that can: 
  - measure "something" in it's environment and process the collected data. 
  - be controlled/monitored/configured by an app via IP or bluetooth.


The goal of this project is to use the current price of electricity to automate the output levels of components in a circuit that simulates a companys energy consumption.

The circuit is powered by solar panels and/or wall outlet.
MQTT is used for wireless communication.
The Django web application is used to: 
  - store and process the data in a database 
  - present the data in graphs and lists
  - automate the output levels of the components
  - manually control the components priority- and output levels

The Django application runs in two threads. 
The main thread handles the http-requests when using the website. 
The second thread runs the MQTT client that listens for new data from the circuit.
