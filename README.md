# Chrome Bookmarks to Microsoft Excel

*This Python Application helps you to convert your **Google Chrome Bookmarks** to a **Microsoft Excel compatible Spreadsheet.***

## How it works:

This software access your **Google Chrome Bookmarks** and dump database to spreadsheet format.

It also has features regarding to clean URLs, refresh URLs titles and stripping tracking tokens from dirty URLs.

## Requirements - How to install:

Run command:

`pip install --user -U -r requirements.txt`

## How to run:

### Run in GUI:

For running Graphical User Interface:

`python chrome2excel.py -x`

### Run in CLI:

For running a profile in Command Line Interface:

`python chrome2excel.py -p <ProfileNumber>`


**To identify local profiles:**

`python chrome2excel.py -l [ProfileNumber]`


## Features:

**To turn on remove duplicate entries:**

`python chrome2excel.py -p <ProfileNumber> -u`

**To turn on refresh URL Title:**

`python chrome2excel.py -p <ProfileNumber> -r`

**To turn on get Hostname:**

`python chrome2excel.py -p <ProfileNumber> -g`

**To turn on clean URL from tracking**

`python chrome2excel.py -p <ProfileNumber> -c`

**To set output file type as HTML or XLSX:**

`python chrome2excel.py -p <ProfileNumber> -o [html, xlsx]`

**To set input text file name:**

`python chrome2excel.py -i <FileName>`

**To set output file name:**

`python chrome2excel.py -p <ProfileNumber> -n <FileName>`

## About
*This is an **Open Source Project** that uses other [General Public License](http://www.gnu.org/copyleft/gpl.html) (GPL) sources from the web.*

By OTDS H Co.
___
    Vincent Liopard. is a BIUCS Project.

___
