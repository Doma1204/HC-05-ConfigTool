# HC-05 Config Tool
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Doma1204/HC-05-ConfigTool/Upload_Python_Package)](https://github.com/Doma1204/HC-05-ConfigTool/actions)
[![GitHub release](https://img.shields.io/github/v/release/Doma1204/HC-05-ConfigTool)](https://github.com/Doma1204/HC-05-ConfigTool/releases)
[![PyPI](https://img.shields.io/pypi/v/HC-05-ConfigTool?color=brightgreen)](https://pypi.org/project/HC-05-ConfigTool)
![PyPI - Downloads](https://img.shields.io/pypi/dm/HC-05-ConfigTool)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/HC-05-ConfigTool)
[![Licence](https://img.shields.io/github/license/Doma1204/HC-05-ConfigTool)](/LICENSE)

A python terminal tool for configuring HC-05 bluetooth module with AT mode

### Table of content
- [Installation](#Installation)
- [Run](#Run)
- [Usage](#Usage)
- [Dependencies](#Dependencies)
- [Licence](#Licence)

## Installation
#### Install with pip
```
$ pip3 install HC-05-ConfigTool
```
#### Manual Install (latest, but unstable)
```
$ git clone https://github.com/Doma1204/HC-05-ConfigTool.git
$ cd HC-05-ConfigTool
$ python3 setup.py install
```

## Run
To run the terminal tool, type the following command
```
$ python -m hc05config
```
If your computer have both Python2 and Python3, use `python3`
```
$ python3 -m hc05config
```

## Usage
After typing the command above, you should see a panel and you are prompted to select one of the job.
```
Please select the following job:
1. Get basic Information of the HC-05
2. Config a HC-05
3. Set up a pair of master and slave HC-05
4. View preset
5. Exit
Please enter 1-5:
```

#### 1. Get basic Information of the HC-05
The tool retrieves and displays all the basic information of the HC-05 module. The following is a sample output.

```
Information of the HC-05 bluetooth module
-----------------------------------------
Name: HC-05 Bluetooth
Baud rate: 9600
Stop bit: 0
Parity bit: 0
Password: 1234
Address: ABCD:2B:1234
Version: 3.0-20170601
Role: Slave(0)
Connection mode: 1
Bind address: 0:0:0
-----------------------------------------
```

If the HC-05 module has not entered AT mode, the following warning message will be recieved. You should set the module to AT mode before pressing enter.

```
The bluetooth module have not entered AT mode yet, please fix your module and then press enter
```

#### 2. Config a HC-05
The tool retrieves all the basic information of the HC-05 module and asks for item(s) to configure. The following is a sample output.

```
Please select the item you want to change:
1. name: HC-05 Bluetooth
2. baud_rate: 9600
3. stop_bit: 0
4. parity_bit: 0
5. password: 1234
6. role: 0
7. connection_mode: 1
8. bind_address: 0:0:0
Please enter 1-8, or press enter to exit:
```

Press enter to start writing changes to the module. The configuration can be saved to a preset for later use if multiple modules are needed to be configure with same or similar configuration.

#### 3. Set up a pair of master and slave HC-05
The tool can help set up a pair of master and slave. It can be done by using one serial port or two serial ports. You need to plug and remove the master module and slave module multiple times during the set up process if you choose to set up with one serial port. You are prompted to enter the name of the two modules, baud rate, stop bit and parity bit for setting the pair. Follow the instructions on the display to set up the pair. Presets can also be used in the mode.

Sample:
```
----------------------------------------------------

Please enter the following value to set up the pair

Master module name: Master
Slave module Name: Slave
Baud rate: 9600
Stop bit: 0
Parity bit: 0

----------------------------------------------------
```

#### 4. View preset
View the preset for ***Config a HC-05*** and ***Set up a pair of master and slave HC-05***.

Sample output:
```
Please select a Category
1. BT_Config
2. Master_and_Slave
Please select 1-2: 1

Please select the following preset:
1. Testing
Please select 1-1: 1

-----------------------------------------

name: HC-05 Bluetooth
baud_rate: 9600
stop_bit: 0
parity_bit: 0
password: 1234
role: 0
connection_mode: 1
bind_address: 0:0:0

-----------------------------------------
```

#### 5. Exit
Exit the program

## Dependencies
The tool requires Python with version above 3.0. It is built on top of [pyserial](https://pypi.org/project/pyserial/).

## Licence
[MIT Licence](/LICENSE)
