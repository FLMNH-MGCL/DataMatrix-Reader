# DataMatrix-Reader

A Python program for extracting decoded datamatrix information from images. This program was created for the Digitization Department of the McGuire Center for Lepidoptera at the Florida Museum of Natural History. Given a collection of specimen images, the program will decode the datamatrix inside each picture and rename / sort them according to a predefined, standardized naming scheme.

### Installation and Usage

For now, this will only be compatible with Linux and MacOS systems.

Installation on Linux will depend on your distribution, however running the program is the same between Linux and MacOS. Installation for MacOS: you'll need [Python 3](https://www.python.org/downloads/), Command Line Tools for Xcode, and you can use [Homebrew](https://docs.brew.sh/Installation) to install the necessary dmtx dependencies:

```
$ brew install dmtx-utils
$ git clone <git_url>
$ cd DataMatrix-Reader/src
$ python dm_reader.py (or use python3 dm_reader.py)
```

Currently, we rely on executing the utility scripts built using libdmtx in from python. In the future, we would like to instead build the libdmtx library and create our own bindings.

This program's intended use is for the FLMNH, and as such the file naming scheme is specific. If this were to be adapted to a different project the renaming would need to be refactored in order to suit the new needs.

### References
