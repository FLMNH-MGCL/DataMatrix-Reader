# DataMatrix-Reader
This program was created or the Digitization Department of the McGuire Center for Lepidoptera at the Florida Museum of Natural History. Given a collection of specimen pictures, the program will decode the data matrix inside each pictrure and rename / sort them according to a museum-standardized naming scheme. 

### Installation and Usage
For now, this will only be compatible with Linux and MacOS systems. 

Installation on Linux will depend on your distribution, however running the program is the same between Linux and MacOS. Installation for MacOS: you'll need [Python 3](https://www.python.org/downloads/), Command Line Tools for Xcode, and you can use [Homebrew](https://docs.brew.sh/Installation) to install the necessary dmtx dependencies:

```
$ brew install dmtx-utils
$ git clone <git_url>
$ cd DataMatrix-Reader/src
$ python dm_reader.py (or use python3 dm_reader.py)
```

This program's intended use is for the FLMNH, and as such the file naming scheme is specific. If this were to be adapted to a different project the renaming would need to be refactored in order to suit the new needs. 

### References
