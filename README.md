# qey
A utility package to configure hotstrings with ease.

## Compatibility
Fully compatible with :

- **Windows** 7 and higher.
- **Linux** distributions running under the X Window System.

Requires `Python 3`. Tested on `Python 3.6`.

## Usage
You can clone the repository:
```
$ git clone https://github.com/Whenti/qey
```
or [download and extract the zip](https://github.com/Whenti/qey/archive/master.zip), and then run the setup:
```
$ python setup.py install
```

Check the [documentation below](https://github.com/Whenti/pyqo#Documentation) to see what is available.

## Dependencies
See the [requirements.txt](requirements.txt) file for details.

## Author

* **Quentin LÉVÊQUE** - [Whenti](https://github.com/Whenti)

## License
This project is proudly licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

# Documentation

After installing this package, you will have the command `qey` at your disposal. You may use `qey --help` for help.

To set up `qey` with your custom hotkeys, you first of all need to write an INI file describing the desired hotstrings. More precisely, each line of the file must have the following format :
```
<hotstring> <replacement>
```
where `<hotstring>` must not contain any space. Empty lines and lines between brackets will not be considered. If you have any trouble setting it up, please refert to the [example file](data_example.ini).

You can associate this file with `qey` using
```
qey setfile <path>
```
and
```
qey start
```
to start it, and you are good to go. `qey` use the character `^` to distinguish hotstrings from other words. Type `^<hotstring>` filling `<hotstrings>` with one of your hotstrings, it should be automatically replaced by the provided words.

With `qey startup`, you can make `qey` automatically run at startup. See `qey startup --help` for details.
