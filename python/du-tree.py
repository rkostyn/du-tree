#!/usr/bin/python
# By Alex Kostyn

# Starting import section ##
import sys
import math
import argparse
import subprocess

# GLOBALS
VERSION = 0.2


# Classes
# ALL THE COLORS!
class Colors:
    """ANSI Colors"""
    clrscr = '\033[2J'
    clrline = '\033[K'
    home = '\033[0;0f'
    xclear = '\033[2J\033[K\033[K'

    def __init__(self):
        self.off = '\033[m'
        self.red = '\033[31m'
        self.yel = '\033[33m'
        self.blu = '\033[36m'
        self.wht = '\033[37m'

    def bleach(self):
        self.off = ''
        self.red = ''
        self.yel = ''
        self.blu = ''
        self.wht = ''


# Functions
# Used to take bytes and set them to the appropiate names.
# Takes an Int that resembles bytes
# Returns a string of its human readable size.
def convertsize(size):
    if size == 0:
        return '0B'
    size_name = ("KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    num = int(math.floor(math.log(size, 1024)))
    power = math.pow(1024, num)
    size = round(size/power, 2)
    return '%s %s' % (size, size_name[num])


# Function is just printing the full path with colors.
# Depending on the percent of total Disk Usage determins the color of the print
def printpath(pppercent, ppsubfilename, ppsubfilesize):
    if pppercent == 100:
        print ppsubfilename + "\t" + ppsubfilesize
        if args.verbose:
            print "@ " + str(pppercent) + "%"
    elif pppercent > 60:
        print termColor.red + ppsubfilename\
            + "\t" + ppsubfilesize + termColor.off
        if args.verbose:
            print "@ " + str(pppercent) + "%"
    elif pppercent > 40:
        print termColor.yel + ppsubfilename\
              + "\t" + ppsubfilesize + termColor.off
        if args.verbose:
            print "@ " + str(pppercent) + "%"
    elif pppercent > 20:
        print termColor.blu + ppsubfilename\
              + "\t" + ppsubfilesize + termColor.off
        if args.verbose:
            print "@ " + str(pppercent) + "%"
    elif 20 > pppercent > 10:
        print ppsubfilename + "\t" + ppsubfilesize
        if args.verbose:
            print "@ " + str(pppercent) + "%"


# Prints out just the file like old du-tree.
# Depending on the percent of total Disk Usage determins the color of the print
# Each tab is replaced with two spaces.
def printfile(pfpercent, pfsubfilename, pfsubfilesize):
    splitsubfilename = pfsubfilename.split("/")
    spacenumber = pfsubfilename.count("/") * 2

    if pfpercent == 100:
        print pfsubfilename + "\t" + pfsubfilesize
        if args.verbose:
            print "@ " + str(pfpercent) + "%"
    elif pfpercent > 60:
        print termColor.red + " " * spacenumber + \
            splitsubfilename[-1] + "\t" + pfsubfilesize + termColor.off
        if args.verbose:
            print "@ " + str(pfpercent) + "%"
    elif pfpercent > 40:
        print termColor.yel + " " * spacenumber + \
            splitsubfilename[-1] + "\t" + pfsubfilesize + termColor.off
        if args.verbose:
            print "@ " + str(pfpercent) + "%"
    elif pfpercent > 20:
        print termColor.blu + " " * spacenumber + \
            splitsubfilename[-1] + "\t" + pfsubfilesize + termColor.off
        if args.verbose:
            print "@ " + str(pfpercent) + "%"
    elif 20 > pfpercent > 10:
        print " " * spacenumber + splitsubfilename[-1] + "\t" + pfsubfilesize
        if args.verbose:
            print "@ " + str(pfpercent) + "%"

# --- Entry --- #
# Starting ArgParser:
parser = argparse.ArgumentParser(description='DU formatter')
# Run on any directory.
parser.add_argument('directory',
                    help="The directory you want to scan.",
                    nargs="*")
# Generic version speal.
parser.add_argument('-V', '--version',
                    action='version',
                    version='%(prog)s, Version: ' + str(VERSION))
# Prints everything.
# Is more useful for me dubugging the code.
parser.add_argument('-v', '--verbose',
                    action='store_true',
                    help="Prints everything the program is doing.")
# Prints a legend showing what each color means.
parser.add_argument('-l', '--legend',
                    action='store_true',
                    help="Prints color legend before running.")
# Clear colors from output.
parser.add_argument('-b', '--bleach',
                    action='store_true',
                    help="Removes color from output")
# Prints full path.
parser.add_argument('-f', '--full',
                    action='store_true',
                    help="Prints full path")
# Doing the needful.
args = parser.parse_args()

# Setting Variables.
depth = 5
dirs = args.directory
termColor = Colors()

if args.bleach:
    termColor.bleach()

# Printing legend if argument was passed.
# Specifically showing what colors mean what.
if args.legend:
    print "\n  --- Color Legend --- "
    print termColor.red + \
        " [*] Greater than 60% overall usage." + termColor.off
    print termColor.yel + \
        " [*] Greater than 40% overall usage." + termColor.off
    print termColor.blu + \
        " [*] Greater than 20% overall usage." + termColor.off
    print "\n"

# Running the command and sending the output to a variable
# Running without human readable for acuracy.
# stderr = subprocess.PIPE to hide permission denied messages.
# same with stdout = subprocess.PIPE

if not args.bleach:
    print "Running Du",
    sys.stdout.flush()

command = ['/usr/bin/du', '-d' + str(depth)]
# Adding dirs to the end of the command.
for i in dirs:
    command.append(i)
proc = subprocess.Popen(
    command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output = proc.communicate()

if not args.bleach:
    print "\rComplete: "

# More for dubugging purposes
if args.verbose:
    print output

# Trimming the output.
# Command is stored in a Tuple.
# Grabbing just the first element.
# Splitting via '\n' Then storing in an array.
FormattedOutPut = output[0]
FormattedOutPut = FormattedOutPut.splitlines()

# Going through each element of the output to find the base dir.
# The base dir will always be the largest
# Each item is seperated with a tab, therefore I split each line by '\t'
# Casted baseDirSize in comparison for better calculations.
count = 0
baseDir = ""
baseDirSize = 0
for line in FormattedOutPut:

    count += 1
    dirSize = int(line.split('\t')[0])

    if dirSize > int(baseDirSize):
        if args.verbose:
            print str(dirSize) + " > " + str(baseDirSize)

        baseDirSize = dirSize
        baseDir = line.split('\t')[1]


# Going through and outputing large folders / files
# Converted baseDirSize to an float before doing anything.
# Reversing the list so that it makes more sense.
# To grab the percent you set both file size vars to floats,
# then you deivide sub/base, then multiply it by 100.
# Converted to int to remove the decimal.
baseDirSize = float(baseDirSize)
for line in reversed(FormattedOutPut):

    subFileSize = float(line.split('\t')[0])
    subFileName = line.split('\t')[1]

    percent = int(subFileSize / baseDirSize * 100)
    subFileSize = convertsize(subFileSize)

    if args.full:
        printpath(percent, subFileName, subFileSize)
    else:
        printfile(percent, subFileName, subFileSize)
