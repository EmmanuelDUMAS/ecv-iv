#!/usr/bin/env python3
# ecv_iv.py
# -*- coding: utf-8 -*-
# -------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2021-2022, Emmanuel DUMAS
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
# SETUP for Image viewer ECV-IV - windows version
#
#  to create .msi file
#    python3 ./setup_win.py  bdist_msi
# -----------------------------------------------------------------------------
# 17/01/2021 Creation ................................................ E. Dumas
# -----------------------------------------------------------------------------

# import os
# from setuptools import setup
from cx_Freeze import setup, Executable

# Create our registry key, and fill with install directory and exe
registry_table = [
        ('ECV_IVKLM'       , 2, r'SOFTWARE\ECV_IV', '*'         , None, 'TARGETDIR'),
        ('ECV_ICInstallDir', 2, r'SOFTWARE\ECV_IV', 'InstallDir', '[TARGETDIR]', 'TARGETDIR'),
        ('ECV_IVExecutable', 2, r'SOFTWARE\ECV_IV', 'Executable', '[TARGETDIR]ecv_iv.exe', 'TARGETDIR'),
    ]

# Provide the locator and app search to give MSI the existing install directory
# for future upgrades
reg_locator_table = [
        ('ECV-IVInstallDirLocate', 2, r'SOFTWARE\ECV_IV', 'InstallDir', 0),
    ]
app_search_table = [('TARGETDIR', 'ECV_IVInstallDirLocate')]

msi_data = {
        'Registry': registry_table,
        'RegLocator': reg_locator_table,
        'AppSearch': app_search_table,
    }

bdist_msi_options = {
    "add_to_path": True,
    "all_users": True,
    "data": msi_data,
    # "environment_variables": [
    #            ("E_MYAPP_VAR", "=-*MYAPP_VAR", "1", "TARGETDIR")
    #        ],
    # "upgrade_code": "{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}",
}


setup(
    name="ECV_IV",
    version="0.4",
    author="Emmanuel DUMAS",
    author_email="emmanuel.dumas@free.fr",
    description=("Simple Image viewer with web technologies"),
    license="BSD",
    keywords="simple image viewer",
    url="https://github.com/EmmanuelDUMAS/ecv-iv",
    executables = [
        Executable( "ecv_iv/ecv_iv.py",
                    base=None)],
    packages=[
        'ecv_iv',
    ],
    package_data={"ecv_iv": [ "ecv_load_img.html",
                              "ecv_load_img.js",
                              ]},
    options={
        # "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    entry_points={'console_scripts': ['ecv_iv=ecv_iv.ecv_iv:main']},
    long_description="""ecv_iv

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
