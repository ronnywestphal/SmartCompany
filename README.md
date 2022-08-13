# SmartCompany
This Django web application is part of a school project at the end of the second year in the Electrical Engineering program at KTH Royal Institute of Technology.

The course objective is to create an IoT device that can: 
  - measure "something" in it's environment and process the collected data. 
  - be controlled/monitored/configured by an app via IP or bluetooth.

## Project Overview
The purpose of this project was to build a system that could automate and monitor how much energy different processes consume. It would use the current hourly price of electricity to decide the optimal time to run certain processes. This could then be applied to a home or a company that looks to lower their energy consumption. 

## Django Web Application
The core functionality of the system is handled by the Django Web Application.
  - store and process the data in a database 
  - present the data in graphs and lists
  - automate the output levels of the components
  - manually control the components priority- and output levels

## Testing Circuit
The circuit is powered by solar panels and/or wall outlet and was built to simulate a company's energy conumption. INA219 chips and an ESP32 were used to measure the effect and voltage in the circuits components.

## MQTT Protocol
MQTT was used to communicate wirelessly between the circuit and the web application. The ESP32 transmitted/received data to/from a RPI4 that was in a separate network using Dynamic DNS. The RPI4 forwarded/received data to/from the web application. The MQTT subscriber client in the web application needs to run in a separate thread to avoid it blocking the rest of the application. 


