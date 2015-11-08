#!/bin/bash
#-----------------------------------------------------------------------
# File: doc2docx.sh
#-----------------------------------------------------------------------
# Description:
#   This bash script convert doc files tp docx format using libreoffice.
#-----------------------------------------------------------------------
# Usage:
# > bash doc2docx.sh <source-directory> [output-directory]
# Example:
# > bash ./verbatim/24/
#-----------------------------------------------------------------------
CONVERTOR="/cygdrive/c/PortableApps/LibreOfficePortable/App/libreoffice/program/soffice.exe"
SRCPATH="$1"

$CONVERTOR --headless --convert-to docx --outdir $SRCPATH $SRCPATH/*.doc

