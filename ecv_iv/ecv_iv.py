#!/usr/bin/env python3
# ecv_iv.py
# -*- coding: utf-8 -*-
# -------------------------------------------------------
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
# Image viewer for EDS-CV-Lib
#
#    this image viewer have an launcher in python, but most of viewer must be
#    develop in javascript / html
#
# -----------------------------------------------------------------------------
# 15/10/2020 Creation ................................................ E. Dumas
# 20/10/2020 Set file as args ........................................ E. Dumas
# 29/12/2020 First operational version ............................... E. Dumas
# 05/01/2021 Move in a separate project : ECV-IV ..................... E. Dumas
# 13/01/2021 Support absolute path filename .......................... E. Dumas
# 18/01/2021 Use now main() function ................................. E. Dumas
# 09/11/2021 Server stays in background (daemon) ..................... E .Dumas
# 01/12/2021 Quick and dirty update for Windows ...................... E. Dumas
# -----------------------------------------------------------------------------

import argparse
import http.client
import http.server
import os
import pathlib
import platform
import socketserver
import subprocess
import sys
from functools import partial
from multiprocessing import Process


def basicHttpServer():
    """Start a basic HTTP server
    15/10/2020 creation EDS
    """
    # start a web server
    PORT = 8008
    # Handler = http.server.SimpleHTTPRequestHandler
    HandlerClass = partial( http.server.SimpleHTTPRequestHandler,
                            directory="/")
    
    with socketserver.TCPServer(("", PORT), HandlerClass) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def forkify():
    """create a process fork and run the function
    """
    system = platform.system()
    if system == "Windows":
        # print("Windows system")

        # no "fork" strategies
        basicHttpServer()

    elif system == "Linux":    
        # print("system=", system)
        if os.fork() != 0:
            return
        basicHttpServer()
    else:
        raise Exception("Unsupported system '%s'" % system)

def startServer():
    # print("Start server - 00")
    pserv = Process(target=forkify)
    pserv.start()

    # EDS 01/12/2021 : do better latter
    if platform.system() != "Windows":
        pserv.join()
    
    print("Server started")

def formatPath(p):
    p2 = os.path.normpath( os.path.join( os.getcwd(), p) )
    print("p2=", p2)
    if platform.system() == "Windows":
        r = pathlib.PurePath(p2).as_posix()[2:]
    else:
        r = pathlib.PurePath(p2).as_posix()
    print("r=", r)

    return r

# if __name__ == "__main__":
def main():
    parser = argparse.ArgumentParser(epilog="version 0.3")
    parser.add_argument("files", nargs='*',
                        help="image file(s) to display")
    parser.add_argument("-d", action="store_true",
                        help="start JS console (debug)")
    args = parser.parse_args()
    # print("args=", args)
    # print("args.files=", args.files)
    #    ->args.files= ['f1', 'f2', 'f3']
    
    # print("main - 20")

    c = http.client.HTTPConnection('127.0.0.1', 8008, timeout=1)
    try:
        c.request("HEAD","/")
    except ConnectionRefusedError as e:
        print("e=", e)
        if e.errno == 111:
            startServer()
        else:
            raise
    except TimeoutError as e:
        # print("e=", e)
        startServer()
    
    # print("main - 40")

    # EDS 01/12/2021 - factorization in formatPath
    # curPath = os.path.normpath( os.path.join( os.getcwd(),
    #                                          os.path.dirname(__file__ ) ) )
    # print("curPath=", curPath)
    # # Example :
    # # curPath= /home/xxx/working/eds-cv-lib/tools/edsimgviewer
    # # or on windows :
    # # curPath= c:\Users\Dumas\source\repos\ecv-iv\ecv_iv
    # if platform.system() == "Windows":
    #    formatPath = pathlib.PurePath(curPath).as_posix()[2:]
    # else:
    #     formatPath = curPath

    fPath = formatPath( os.path.dirname(__file__ ) )
    print("fPath=", fPath)

    secArg = "http://127.0.0.1:8008" + fPath + "/ecv_load_img.html"
    if len(args.files) == 1:
        if args.files[0][0] == "/":
            f1 = args.files[0]
        else:
            # f1 = os.getcwd() + "/" + args.files[0]
            f1 = formatPath( args.files[0] )
        secArg += "?f1=%s" % (f1,)
    elif len(args.files) >= 2:
        if args.files[0][0] == "/":
            f1 = args.files[0]
        else:
            # f1 = os.getcwd() + "/" + args.files[0]
            f1 = formatPath( args.files[0] )
        if args.files[1][0] == "/":
            f2 = args.files[1]
        else:
            # f2 = os.getcwd() + "/" + args.files[1]
            f2 = formatPath( args.files[1] )
        secArg += "?f1=%s&f2=%s" % (f1, f2)
    
    if platform.system() != "Windows":
        lArgs = [ "firefox", secArg ]
    else:
        lArgs = [ "C:\\Program Files\\Mozilla Firefox\\firefox.exe", secArg ]
    if args.d:
        lArgs.append("-jsconsole")
    
    print("lArgs=", *lArgs)

    pLauncher = subprocess.run( lArgs )
    

if __name__ == "__main__":
    sys.exit(main())

# end of file
