#!/usr/bin/env python3
# tst_ecv_iv.py
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2020-2021, Emmanuel DUMAS
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
# ECV Image Viewer
# -----------------------------------------------------------------------------
# History
# 19/10/2020 Creation ................................................ E. Dumas
# 29/12/2020 First operational version ............................... E. Dumas
# -----------------------------------------------------------------------------

# native python import
import unittest
import subprocess

# third party import
# import cv2
# import numpy as np

# project import

# tested file
from src import ecv_iv


# -----------------------------------------------------------------------------
# Class
# -----------------------------------------------------------------------------
class TST_EdsImgViewer(unittest.TestCase):
    """Test EdsImgViewer
    19/10/2020 Creation .............................................. E. Dumas
    """
    
    def setUp(self):
        """
        19/10/2020 Creation .......................................... E. Dumas
        """
        print("setup")

    def tearDown(self):
        """
        19/10/2020 Creation .......................................... E. Dumas
        """
        print("tearDown")
    
    def commonPart(self):
        """
        19/10/2020 Creation .......................................... E. Dumas
        """
        print("common part")
    
    def test_SimpleRun(self):
        """test a simple run with 2 basic images
        19/10/2020 Creation .......................................... E. Dumas
        """
        print("test Dataset 01")
        
        p = subprocess.Popen( [ "python3",
                                "../ecv_iv.py",
                                "-d",
                                "image_a.png",
                                "image_b.png"])
        p.wait()
    

# -----------------------------------------------------------------------------
# Test suite definition
# -----------------------------------------------------------------------------
def TST_TestSuite_EdsImgViewer(testSuite, oneByOne=False):
    """
    19/10/2020
    """
    allTests = (
        "test_SimpleRun",
        # "test_Dataset_02",
    )
    
    if oneByOne is True:
        runTests = (allTests[0], )
    else:
        runTests = allTests
    
    for t in runTests:
        testSuite.addTest( TST_EdsImgViewer( t ) )
    

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    testSuite = unittest.TestSuite()
    TST_TestSuite_EdsImgViewer(testSuite, oneByOne=False)
    unittest.TextTestRunner(verbosity=2).run(testSuite)


# end of file
