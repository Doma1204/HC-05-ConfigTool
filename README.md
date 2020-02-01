# HC-05 Config Tool
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Doma1204/HC-05-ConfigTool/Upload_Python_Package)](https://github.com/Doma1204/HC-05-ConfigTool/actions)
[![GitHub release](https://img.shields.io/github/v/release/Doma1204/HC-05-ConfigTool)](https://github.com/Doma1204/HC-05-ConfigTool/releases)
[![PyPI](https://img.shields.io/pypi/v/HC-05-ConfigTool?color=brightgreen)](https://pypi.org/project/HC-05-ConfigTool)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/HC-05-ConfigTool)](https://pypi.org/project/HC-05-ConfigTool/#files)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/HC-05-ConfigTool)
[![Licence](https://img.shields.io/github/license/Doma1204/HC-05-ConfigTool)](https://github.com/Doma1204/HC-05-ConfigTool/blob/master/LICENSE)

A python terminal tool for configuring HC-05 bluetooth module with AT mode

### Table of content
- [Installation](#Installation)
- [Run](#Run)
- [Usage](#Usage)
- [About HC-05 AT Mode](#About-HC-05-AT-Mode)
- [Dependencies](#Dependencies)
- [Licence](#Licence)

## Installation
#### Install with pip
```
$ pip3 install HC-05-ConfigTool
```
#### Manual Install (latest, but maybe unstable)
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
4. Manage preset
Please enter 1-4, or press enter to exit: 
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
1. Name: HC-05 Bluetooth
2. Baud Rate: 9600
3. Stop Bit: 0
4. Parity Bit: 0
5. Password: 1234
6. Role: 0
7. Connection Mode: 1
8. Bind Address: 0:0:0
Please enter 1-8, or press enter to exit: 
```

Press enter to start writing changes to the module. The configuration can be saved to a preset for later use if multiple modules are needed to be configure with same or similar configuration.

#### 3. Set up a pair of master and slave HC-05
The tool can help set up a pair of master and slave. It can be done by using one serial port or two serial ports. You need to plug and remove the master module and slave module multiple times during the set up process if you choose to set up with one serial port.

You are prompted to enter the name of the two modules, baud rate, stop bit and parity bit for setting the pair. Follow the instructions on the display to set up the pair. Presets can also be used in the mode.

#### 4. Manage Preset
There are serval features for managing presets.

Sample output: 
```
Please select the following job:
1. View preset
2. Edit preset
3. Rename preset
4. Copy preset
5. Delete preset
6. Export preset
7. Import preset
Please enter 1-7, or press enter to exit: 
```
Follow the instructions after selecting the job to manage preset.

Sample Preset for configuring HC-05:
```
{
    "Name": "HC-05 Bluetooth",
    "Baud Rate": 9600,
    "Stop Bit": 0,
    "Parity Bit": 0,
    "Password": "1234",
    "Role": 0,
    "Connection Mode": 1,
    "Bind Address": "0:0:0"
}
```

Sample Preset for configuring master and slave pair:
```
{
    "Master Name": "Master",
    "Slave Name": "Slave",
    "Baud Rate": 9600,
    "Stop Bit": 0,
    "Parity Bit": 0
}
```

Presets are saved on the user home directory(`~/.hc05config_preset`). Note that uninstall the package by using `pip uninstall HC-05_ConfigTool` **does not** delete the preset file.

## About HC-05 AT Mode
AT mode is the main way to config the HC-05 Bluetooth module. For the details of AT mode, please refer to the [document](https://github.com/Doma1204/HC-05-ConfigTool/blob/master/HC-05_AT_command.pdf) that I found in the Internet.

This package **does not** fully support all HC-05 AT mode commands. The supported commands are listed below:
- `AT+VERSION`
- `AT+ADDR`
- `AT+NAME`
- `AT+ROLE`
- `AT+PSWD`
- `AT+UART`
- `AT+CMODE`
- `AT+BIND`

## Dependencies
The tool is built on top of [pyserial](https://pypi.org/project/pyserial/).

## Licence
[MIT Licence](https://github.com/Doma1204/HC-05-ConfigTool/blob/master/LICENSE)
