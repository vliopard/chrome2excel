# Chrome Bookmarks to Microsoft Excel

*This Python Application helps you to convert your Google Bookmarks to a Microsoft Excel Spreadsheet.*

## How it works:

This software access your Google Chrome Bookmarks and dump database to Excel Spreadsheet format.

It also has features regarding to clean URLs, stripping tracking tokens.

## How to install:

Just run command
`pip install -r requirements.txt`

## How to run:

For running in default profile:

`python chrome2excel.py`



**To identify local profiles:**

`python chromeprofile.py -p <ProfileNumber>`

For choosing an alternative profile:

`python chrome2excel.py -p <ProfileNumber>`

## Features:

**To turn on remove duplicate entries:**

`python chrome2excel.py -p <ProfileNumber> -u on`

**To turn on refresh URL Title:**

`python chrome2excel.py -p <ProfileNumber> -r on`

## About
*This is an* ***Open Source Project*** *that uses other [General Public License](http://www.gnu.org/copyleft/gpl.html) (GPL) sources from the web.*

By OTDS H Co.
___
    Vincent Liopard. is a BIUCS Project.

___