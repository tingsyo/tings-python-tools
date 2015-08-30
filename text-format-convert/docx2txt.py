#!/usr/bin/python3
#-----------------------------------------------------------------------
# File: docx2txt.py
#-----------------------------------------------------------------------
# Description:
#   This python script convert docx files (Microsoft Word 2003 and above) 
#   to utf-8 encoded plain text files, txt.
#-----------------------------------------------------------------------
# Usage:
# > python3 docx2txt.py <source-directory> [output-directory]
# Example:
# > python3 docx2txt.py 
#-----------------------------------------------------------------------
import sys, os, re, argparse
from docx import Document

def retrieveTextFromDocx(furi):
    d = Document(furi)
    txt = []
    for p in d.paragraphs:
        txt.append(p.text+'\n')
    return(txt)
    
def writeToTxt(content, ofile):
    with open(ofile, 'w') as of:
        of.writelines(content)

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    return(0)
#-----------------------------------------------------------------------
# Main function
#-----------------------------------------------------------------------
def main():
    # Configure Argument Parser
    parser = argparse.ArgumentParser(description='Convert docx file into plain text file.')
    parser.add_argument("srcdir", help="the directory holds the docx files")
    parser.add_argument("-o", "--outputdir", help="the directory to hold converted txt files")
    args = parser.parse_args()
    # Walk through args.srcdir to find '*.docx'
    for root, dirs, files in os.walk(args.srcdir):
        # For progress
        progress(0,len(files))
        ip = 0
        for file in files:
            if (file.endswith(".docx") or file.endswith(".DOCX") and (not file.startswith("~"))):
                full_fname = os.path.join(root, file)
                # Perform conversion
                content = retrieveTextFromDocx(full_fname)
                # Output
                if(args.outputdir):
                    if not os.path.exists(args.outputdir):
                        os.makedirs(args.outputdir)
                    ofile = args.outputdir + '/' + file + ".txt"
                else:
                    ofile = full_fname + ".txt"
                writeToTxt(content, ofile)
            # Progress update
            ip+=1
            progress(ip, len(files))

#==========
# Script
#==========
if __name__=="__main__":
    main()