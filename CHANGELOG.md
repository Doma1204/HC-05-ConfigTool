# Change Log

- [v0.1.1](#Version-0.1.1---2020-03-29)
- [v0.1.0](#Version-0.1.0---2020-02-01)
- [v0.0.1]()

## Version 0.1.1 - 2020-03-29
### Better Preset management
#### Added
- If preset is changed during HC-05 set up process, it first ask if you want to save changes to the preset.
#### Fixed
- Fix Infinite loop when attempting to retrieve the name of HC-05 module with firmware version 2.x.
- Add notification about decoding error instead of fatal error. This error usually happen when the connection between the HC-05 module and computer is unstable.

## Version 0.1.0 - 2020-02-01
### Add Manage Preset Feature, Program Optimization, Bugs Fixed
#### Added
- Add manage preset feature (Note: the older preset may not be compatible with this version).
- Add notification to re-enter AT mode when the HC-05 module suddenly exit AT mode or disconnect during configure process.
#### Changed
- Optimize the speed of sending and receiving AT commands.
- Optimize the speed of configuring HC-05 module.
#### Fixed
- Preset will not save on the current working directory now. Instead, it is saved on home directory.

## Version 0.0.1 - 2020-01-27
### Launch of HC-05 Config Tool
- Simplify the configuration of HC-05 Bluetooth module, no need for memorizing AT command.
- Support Window, macOS and Linux with Python3 installed.