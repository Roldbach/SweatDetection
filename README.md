# SweatDetection
This is the official implementation of the project "A Wearable Sweat-detection Device for Inflammatory Bowel Disease Management" by Group Fantastic Detector.

## Get Started
- To successfully use our program, an Arduino Uno-based circuit is required to pair with the computer first. This could be done by:

    1. Correctly connect the circuit (could be found in the ***Diagram***).
    2. Open the Bluetooth control pannel using computer and find the device called "HC-05".
    3. Pair the device with default password: 1234
    
    For more detailed instrution, please visit: https://www.instructables.com/Arduino-AND-Bluetooth-HC-05-Connecting-easily/
- Run the **Main.py** script to start the monitoring program.
- By default, we use the serial port **COM6** for Bluetooth connection. Please make sure the availability of this port. To change to another port, please modify the **Configuration.py**.

## General Structure
This repopsitory could be mainly divided into:
- Report Related
- Computer Program Related (Bluetooth Server)
- Arduino Circuit Related (Bluetooth Client)

### Report Replated
- Our full report could be found in the ***Report***.
- With the ***Data***, we simulated the sensor reading after being processed by the processing circuit. We demonstrated the functionality of the program for better data visulization, which could be found in the ***Plot***.
- Our data for proof-of-principle glucose sensor could be found in the ***ExperimentalData***. We verified the accuracy and the reliablity of the sensor and those results could also be found there.
- All codes for analysing data and plotting could be found in the ***PaperScript***.

### Computer Program Related
- We used PyQT5 to construct our user interface, which could all be found in the ***UI***.
- The class *BluetoothServe* could handle all issues related to Bluetooth signal transmission including receiving data, sending alarm signal. This could be found in the **BluetoothServe.py**
- The class *UIController* could control all pages as well as the Bluetooth module, which was implement in the **UIController.py**
- Our database could all data and could be used for further analysis (could be found in the **DataBase.py**). The corresponding **Test.py** contains lots of testing functions to make sure the database could work smoothly and efficiently.

### Arduino Circuit Related
- Our script for Arduino was written in C++ and could be found in the ***BluetoothClient***. For now, it could randomly generate consentration signals within a reasonable range, which could be used for further analysis and plotting by the computer.
- Within the ***ArduinoLibrary***, it saved the necessary libraries for Arduino to measure the temperature. Other libraries could also be stored here.
