# Lenovo K5923 Manager

The Lenovo K5923/Chicony TG-1226 Wireless TouchPads are devices that emulate a real touchpad by reporting to be a mouse and keyboard combo to the OS. In order to support gestures, they send key presses (Keyboard shortcuts) to the OS. The problem is that keyboard shortcuts are different between Windows and Linux, so most gestures do not work or are doing weird things by default. Lenovo does not provide a way to change those shortcuts, so I decided to write a daemon and a "Control Panel"/"Manager" application through which users will be able to set different actions for every gesture.

For now this is only a non-configurable daemon but it will evolve in a full app fairly quickly as I am using this touchpad as a daily driver.

This is an unofficial app made by me and has nothing to do with Lenovo and Chicony or their brand.

## How to use

Start the daemon as administrator.

```bash
sudo python3 src/k5923d.py
```

## Default gesture actions

The current settings are tailored twords GNOME.

| Gesture | Action (key combo) |
| --- | --- |
| Top edge swipe | Unmaximize current application (Super+Down) |
| Top to bottom edge swipe | Close current application (Alt+F4) |
| Left edge swipe | Show all apps (Super+A) |
| Right edge swipe | Switch bettween applications (Super+TAB) |
| Rotate Clockwise | Rotate Clockwise (Ctrl+R) |
| Rotate Counterclockwise | Rotate Counterclockwise (Shift+Ctrl+R) |
| 3 Finger swipe left | Tile current window to the left (Super+Left) |
| 3 Finger swipe right | Tile current window to the right (Super+Right)  |
| 3 Finger swipe down | Show activities (Super) |
| 3 Finger swipe up | Maximize current window (Super+Up) |
| 4 Finger swipe up | Move one workspace down (Super+PageDown) |
| 4 Finger swipe down | Move one workspace up (Super+PageUp) |
| 4 Finger swipe right | Lock the screen (Super+L)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
