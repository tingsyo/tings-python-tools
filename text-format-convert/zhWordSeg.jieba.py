#!/usr/bin/python3
#-----------------------------------------------------------------------
# File: zhWordSeg.jieba.py
#-----------------------------------------------------------------------
# Description:
#   This python script use jieba library (https://github.com/fxsjy/jieba)
# to segment words in Chinese context.  User defined dictionary can be
# added optionally, and additional output of if-idf and text-rank can be
# specified.
#-----------------------------------------------------------------------
# Usage:
# > python3 docx2txt.py <source-directory> [output-directory]
# Example:
# > python3 docx2txt.py 
#-----------------------------------------------------------------------
import sys, os, re, argparse, csv
import jieba, jieba.analyse

def retrieveTextFromDocx(furi):
    d = Document(furi)
    txt = []
    for p in d.paragraphs:
        txt.append(p.text+'\n')
    return(txt)
    
def writeToTxt(content, ofile):
    with open(ofile, 'w') as of:
        of.writelines(content)
    return(0)
        
def writeListToCsv(output, ofile, headers):
    with open(ofile, 'w', newline='') as csvfile:
        cw = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        cw.writerow(headers)    # write header
        for item in output:
            cw.writerow(item)
    return(0)
    
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
    parser = argparse.ArgumentParser(description='Derive basic statistics of Chinese context.')
    parser.add_argument("srcfile", help="the plain text file of the Chinese context")
    parser.add_argument("-d", "--userdict", help="optional user-defined dictionary", default="")
    parser.add_argument("-s", "--stopwords", help="optional stop words list", default="")
    parser.add_argument("-o", "--output", help="the prefix of output files", default="output")
    parser.add_argument("-k", "--topK", help="max length of the list of tf-idf/text-rank", default=100)
    args = parser.parse_args()
    # Open the text file
    with open(args.srcfile, 'r') as f:
        content = f.readlines()
    # Combine all content
    allContent = ''.join(content)
    # Clean the text
    
    # Load user dictionary and stop words
    if (args.userdict != ""):
        jieba.load_userdict(args.userdict)
    if (args.stopwords != ""):        
        jieba.analyse.set_stop_words(args.stopwords)
    # Segmentation
    segmentedContent = jieba.cut(allContent, HMM=False)
    # TF-IDF
    tfidf = jieba.analyse.extract_tags(allContent, topK=args.topK, withWeight=True)
    # text-rank
    tr = jieba.analyse.textrank(allContent, topK=args.topK, withWeight=True)
    # Output
    writeToTxt(segmentedContent, args.output+"_segmented.txt")
    writeListToCsv(tfidf, args.output+"_tfidf.csv", ["term","tfidf"])
    writeListToCsv(tr, args.output+"_textrank.csv", ["term","text-rank"])    

#==========
# Script
#==========
if __name__=="__main__":
    main()