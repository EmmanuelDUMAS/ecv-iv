#!/usr/bin/env python3
# ecv_iv.py
# -*- coding: utf-8 -*-
# -------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2021, Emmanuel DUMAS
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------
# SETUP for Image viewer ECV-IV
# -----------------------------------------------------------------------------
# 18/01/2021 Creation ................................................ E. Dumas
# 19/01/2021 Add ecv_load_img.js ..................................... E. Dumas
# -----------------------------------------------------------------------------

# import os
from setuptools import setup


setup(
    name="ECV-IV",
    version="0.1",
    author="Emmanuel DUMAS",
    author_email="emmanuel.dumas@free.fr",
    description=("Simple Image viewer with web technologies"),
    license="BSD",
    keywords="simple image viewer",
    url="https://github.com/EmmanuelDUMAS/ecv-iv",
    packages=["src", ],
    package_data={"src": [ "ecv_load_img.html",
                           "ecv_load_img.js",
                         ]},
    entry_points={'console_scripts': ['ecv_iv=src.ecv_iv:main']},
    long_description="""ecv-iv

EDS CV lib - Image Viewer

Simple image viewer focus :

only viewer - no edition -
use web technology to reduce size of code
focus on image processing users
command line starter
basic usage

ECV Image viewer have a CLI.
Simple usage :
ecv_iv imageFileName

Bit more advance usage :
ecv_iv imageFileName1 imageFilename2

Who will be use icv_iv ?

People that work on image with program on command line.
eg :
joe@computer:$ myprogram imageInput # produce imageOutput file
joe@computer:$ ecv_iv imageInput imageOutput

Origin

extract from project EDS CV library - URL

""",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: BSD License",
    ],
)

# end of file
