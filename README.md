# qey
A utility package to configure hotstrings with ease.

## Compatibility
Fully compatible with :

- **Windows** 7 and higher.
- **Linux** distributions running under the X Window System.

Requires `Python 3.0` or higher.

## Usage
You can clone the repository:
```
$ git clone https://github.com/Whenti/qey
```
or [download and extract the zip](https://github.com/Whenti/qey/archive/master.zip), and then run the setup:
```
$ python setup.py install
```

Check the [documentation below](https://github.com/Whenti/qey#Documentation) to see what is available.

## Author

* **Quentin LÉVÊQUE** - [Whenti](https://github.com/Whenti)

## License
This project is proudly licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

# Documentation

Run
```
$ qey start
```
and you're already good to go! Type `^cat` to see it in action. More generally, you can type `^<hotstring>` filling `<hotstring>` with one of the defined hotstrings.

To set up `qey` with your custom hotstrings, you can either run
```
$ qey edit
```
to edit the hotstring file, or run
```
$ qey set_file <new_file>
```
to set your own hotstring file.

## Hotstring file format

The hotstring file consists in an INI file where the key and the values are separated with a whitespace. Empty lines and lines starting with `[` are ignored. If you have any trouble setting it up, please refer to the [example file](hotstring_file_example.ini).

# `pyqo` compatibility

`qey` has been specially designed to be compatible with [`pyqo`](https://github.com/Whenti/pyqo). In particular, all variables defined through the `pyqo` commands automatically define hotstrings with the following format:
```
<pyqo_command>^<variable_name>
```

## Example
```
$ # add a website to i
$ i google -a https:\\www.google.com
$ # now you can freely use the hotkey `i^google`
```
