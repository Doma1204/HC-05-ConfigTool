# Change Log

## Version 0.1.1 - 2020-03-29
### Better Preset management
#### Added
- If preset is changed during the HC-05 set up process, it first asks if you want to save changes to the preset.
#### Fixed
- Fix Infinite loop when attempting to retrieve the name of the HC-05 module with firmware version 2.x.
- Add notification about decoding error instead of a fatal error. This error usually happens when the connection between the HC-05 module and the computer is unstable.

## Version 0.1.0 - 2020-02-01
### Add Manage Preset Feature, Program Optimization, Bugs Fixed
#### Added
- Add manage preset feature (Note: the older preset may not be compatible with this version).
- Add notification to re-enter AT mode when the HC-05 module suddenly exits AT mode or disconnect during the configure process.
#### Changed
- Optimize the speed of sending and receiving AT commands.
- Optimize the speed of configuring the HC-05 module.
#### Fixed
- Preset will not save on the current working directory now. Instead, it is saved on the home directory.

## Version 0.0.1 - 2020-01-27
### Launch of HC-05 Config Tool
- Simplify the configuration of HC-05 Bluetooth module, no need for memorizing AT command.
- Support Window, macOS and Linux with Python3 installed.