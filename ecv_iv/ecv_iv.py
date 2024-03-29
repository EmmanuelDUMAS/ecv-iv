#!/usr/bin/env python3
# ecv_iv.py
# -*- coding: utf-8 -*-
# -------------------------------------------------------
# BSD 3-Clause License
#
# Copyright (c) 2020-2022, Emmanuel DUMAS
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
# 17/01/2022 Add checkStartServer() .................................. E. Dumas
# 26/01/2022 Hack for windows / wsl .................................. E. Dumas
# 31/01/2022 First operational version on windows .................... E. Dumas
# 23/03/2022 Update for 4 images ..................................... E. Dumas
# -----------------------------------------------------------------------------

import argparse
import http.client
import http.server
import os
import pathlib
import platform
import site
import socketserver
import subprocess
import sys
import time
from functools import partial
# from multiprocessing import Process
import multiprocessing


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
    pserv = multiprocessing.Process(target=forkify)
    pserv.start()

    # EDS 01/12/2021 : do better latter
    if platform.system() != "Windows":
        pserv.join()
    
    print("Server started")

def checkStartServer():
    """Check if we need to start Server, and if needed start Server
    17/01/2022 : extract from main()
    """
    
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

def formatPath(p):
    p2 = os.path.normpath( os.path.join( os.getcwd(), p) )
    print("p2=", p2)
    if platform.system() == "Windows":
        r = pathlib.PurePath(p2).as_posix()[2:]
    else:
        r = pathlib.PurePath(p2).as_posix()
    print("r=", r)

    return r

def searchHtmlFile():
    """Search HTML file ecv_load_img.html in different case
       - source code
       - install software
       - ...
    """
    # is a normal installation ?
    sp = site.getsitepackages()
    # ['/usr/local/lib/python3.8/dist-packages', '/usr/lib/python3/dist-packages', '/usr/lib/python3.8/dist-packages']
    # or ['C:\\Program Files\\Python310', 'C:\\Program Files\\Python310\\lib\\site-packages']
    for s in sp:
        f = os.path.normpath( s + "/ecv_iv/ecv_load_img.html")
        if os.path.isfile(f):
            return f

    s = formatPath( os.path.dirname(__file__ ) )
    print("search HTml file s=", s)
    f = os.path.normpath( s + "/ecv_load_img.html")
    if os.path.isfile(f):
       return f

    if sp == []:
        # cx_freeze on Windows ?
        print("cx_freeze on Windows ?")
        # print("sys.argv=", sys.argv)

        import win32api
        gmfn = win32api.GetModuleFileName(0)
        print("gmfn=", gmfn)
        # gmfn= C:\Program Files\ECV_IV\ecv_iv.exe

        f = os.path.normpath( os.path.dirname(gmfn) + "\Lib\site-packages\ecv_iv\ecv_load_img.html" )
        print("f", f)
        if os.path.isfile(f):
            print("%s  is a file" % f)
            if platform.system() == "Windows":
                fr = pathlib.PurePath(f).as_posix()[2:]
            else:
                fr = pathlib.PurePath(f).as_posix()

            print("fr=", fr)

            return fr
        
        raise Exception("%s is not a file" % f)



    raise Exception("nothing found in " + str(sp))

def main():
    parser = argparse.ArgumentParser(epilog="version 0.4")
    parser.add_argument("files", nargs='*',
                        help="image file(s) to display")
    parser.add_argument("-d", action="store_true",
                        help="start JS console (debug)")
    args = parser.parse_args()
    # print("args=", args)
    # print("args.files=", args.files)
    #    ->args.files= ['f1', 'f2', 'f3']
    
    # print("main - 20")

    # Mutualization in checkStartServer() - 17/01/2022
    # c = http.client.HTTPConnection('127.0.0.1', 8008, timeout=1)
    # try:
    #    c.request("HEAD","/")
    # except ConnectionRefusedError as e:
    #    print("e=", e)
    #    if e.errno == 111:
    #        startServer()
    #    else:
    #        raise
    # except TimeoutError as e:
    #    # print("e=", e)
    #    startServer()
    checkStartServer()
    
    # print("main - 40")

    print("__file__=", __file__)
    print("os.__file__=", os.__file__)

    # fPath = formatPath( os.path.dirname(__file__ ) )
    # print("fPath for current file=", fPath)

    secArg = "http://127.0.0.1:8008" + searchHtmlFile()

    if len(args.files) == 1:
        if args.files[0][0] == "/":
            f1 = args.files[0]
        else:
            f1 = formatPath( args.files[0] )
        secArg += "?f1=%s" % (f1,)
    elif len(args.files) == 2:
        if args.files[0][0] == "/":
            f1 = args.files[0]
        else:
            f1 = formatPath( args.files[0] )
        if args.files[1][0] == "/":
            f2 = args.files[1]
        else:
            f2 = formatPath( args.files[1] )
        secArg += "?f1=%s&f2=%s" % (f1, f2)
    elif len(args.files) == 3:
        if args.files[0][0] == "/":
            f1 = args.files[0]
        else:
            f1 = formatPath( args.files[0] )
        if args.files[1][0] == "/":
            f2 = args.files[1]
        else:
            f2 = formatPath( args.files[1] )
        if args.files[2][0] == "/":
            f3 = args.files[2]
        else:
            f3 = formatPath( args.files[2] )
        secArg += "?f1=%s&f2=%s&f3=%s" % (f1, f2, f3)
    elif len(args.files) >= 4:
        if args.files[0][0] == "/":
            f1 = args.files[0]
        else:
            f1 = formatPath( args.files[0] )
        if args.files[1][0] == "/":
            f2 = args.files[1]
        else:
            f2 = formatPath( args.files[1] )
        if args.files[2][0] == "/":
            f3 = args.files[2]
        else:
            f3 = formatPath( args.files[2] )
        if args.files[3][0] == "/":
            f4 = args.files[3]
        else:
            f4 = formatPath( args.files[3] )
        secArg += "?f1=%s&f2=%s&f3=%s&f4=%s" % (f1, f2, f3, f4)

    print("platform=", platform.system() );
        
    if platform.system() != "Windows":
        # hack for WSL on windows
        if os.path.isfile("/mnt/c/Program Files/Mozilla Firefox/firefox.exe"):
            lArgs = [ "/mnt/c/Program Files/Mozilla Firefox/firefox.exe", secArg ]
        else:
            lArgs = [ "firefox", secArg ]
        
    else:
        lArgs = [ "C:\\Program Files\\Mozilla Firefox\\firefox.exe", secArg ]
    
    if args.d:
        lArgs.append("-jsconsole")
    
    print("lArgs=", *lArgs)

    try:
        pLauncher = subprocess.run( lArgs )
    except Exception as e:
        print("e=", e)
    
    print("subprocess.run() done")

    # bad patch
    if platform.system() == "Windows":
        time.sleep(100000)

    print("main() - 99")

    

if __name__ == "__main__":
    # need for CX freeze under Windows
    multiprocessing.freeze_support()
    sys.exit(main())

# end of file
