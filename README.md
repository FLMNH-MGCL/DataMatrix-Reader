# DataMatrix-Reader
I am currently exploring different options for reading in and decoding data matrices from JPG\PNG images for the Florida Museum of Natural History at UF. Until I have something more concrete, this will serve as a testing repository.

### Progress / Development Notes
Development has primarily taken place on Linux systems, however it is intended for use on MacOS and Windows systems at the Museum.

**Python:** The python script utilizes piping to call the cat command on an image and pipes the result to the dmtx-utils command line program dmtxread. This is effective and much quicker than any other software / script for decoding I have used. I plan on implementing more specific
timing stats in the testing script, but it seems PNG files scan quicker on average than the
JPG images. Average times went from 1.5-2.5 seconds to 3-4 seconds when switching to JPG. 

**C++:** No testing yet. (I plan on studying the dmtx-utils command line tools to create my own reader programs)

**Java:** Successfully implemented zxing core library into base Java project. Faced with same limitations in QT/QML, but will attempt to use zxing detectors to scan entire image for DM.

**Ruby:** No testing yet.

**Qt/QML**: Successfully implemented QZXing wrapper library. The main issue faced so far is the data matrix must be exact center of image in order to be properly found/decoded. Will attempt work around, however if not fixable this will not be an ideal solution.

### Installation and Usage
**Python:** For now, the python script is only compatible with Linux and MacOS systems. Installation on Linux will depend on your distribution, however running the script is the same between Linux and MacOS. Installation for MacOS: you'll need [Python 3](https://www.python.org/downloads/), Command Line Tools for Xcode, and you can use [Homebrew](https://docs.brew.sh/Installation) to install the necessary dmtx dependencies:
```
$ brew install dmtx-utils
$ git clone <git_url>
$ cd DataMatrix-Reader/python
$ python dm_reader.py
```
This program's intended use is for the FLMNH, and as such the file naming scheme is specific. If this were to be adapted to a different project the renaming would need to be refactor to suit the new needs. 
### References
