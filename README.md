# DataMatrix-Reader
I am currently exploring different options for reading in and decoding data matrices from JPG\PNG images for the Florida Museum of Natural History at UF. Until I have something more concrete, this will serve as a testing repository.

### Progress / Development Notes
Development has primarily taken place on Linux systems, however it is intended for use on MacOS and Windows systems at the Museum.

**Python:** The python script utilizes piping to call the cat command on an image and pipes the result to the dmtx-utils command line program dmtxread. This is effective and much quicker than any other software / script for decoding I have used, yet it is kind of a cheeky solution. Libdmtx and the command line utilities are the major dependency. I might explore the python wrappers, although from what I have already attempted it can be rather slow when compared to the command line dmtx programs

**C++:** No testing yet. (I plan on studying the dmtx-utils command line tools to create my own reader programs)

**Java:** No testing yet.

**Ruby:** No testing yet.

**Qt/QML**: No testing yet.

### Installation and Usage
**Python:** For now, the python script is only compatible with Linux and MacOS systems. Installation on Linux will depend on your distribution, however running the script is the same between Linux and MacOS. Installation for MacOS: you'll need [Python 3](https://www.python.org/downloads/), Command Line Tools for Xcode, and you can use [Homebrew](https://docs.brew.sh/Installation) to install the necessary dmtx dependencies:
```
brew install dmtx-utils
```

### References