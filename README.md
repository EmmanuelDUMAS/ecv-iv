# ecv-iv
EDS CV lib - Image Viewer

Simple image viewer focus :
  * only viewer - no edition -
  * use web technology to reduce size of code
  * focus on image processing users
  * command line starter

# basic usage
EDS CV Image viewer have a CLI.
Simple usage :
```
joe@computer:$ ecv_iv imageFileName.png
```

On windows :
```
C:\Users\> ecv_iv.exe imageFileName.png
```

Bit more advance usage :  
```
joe@computer:$ ecv_iv imageFileName1.png imageFilename2.png
```

# Who will be use icv_iv ?
People that work on image with program on command line.  
eg :
```
joe@computer:$ myprogram imageInput.png   # produce imageOutput.png file
joe@computer:$ ecv_iv imageInput.png imageOutput.png
```


# Installation

## download
Download package here : [Github release](https://github.com/EmmanuelDUMAS/ecv-iv/releases)

## Install on Windows
Double click .msi file.

## Install on Linux
```
joe@computer:$ python3 setup.py build
sjoe@computer:$ udo python3 setup.py install
```

# Origin
extract from project [EDS CV library - URL](https://github.com/EmmanuelDUMAS/eds-cv-lib)

end of document
