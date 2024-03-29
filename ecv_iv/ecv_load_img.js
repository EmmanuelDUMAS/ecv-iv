/* ecv_load_img.js

BSD 3-Clause License

Copyright (c) 2020-2022, Emmanuel DUMAS
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
===============================================================================
History
19/01/2021 Extract from ecv_load_img.html ............................ E. Dumas
19/01/2021 Support only one image .................................... E. Dumas
01/12/2021 Set line in red ........................................... E. Dumas
17/01/2022 Add setHome() ............................................. E. Dumas
23/03/2022 Update for 4 images ....................................... E. Dumas
===============================================================================
*/

"use strict";

class ecv_GlobalInfo {
    constructor() {
        this.tx = 0;
        this.ty = 0;
        this.zx = 2.0;
        this.zy = 2.0;
        
        this.cursorX = 100;
        this.cursorY = 100;

        this.colorCursor = "red";
        
        /* init 4 defaults view */
        this.view1 = null;
        this.view2 = null;
        this.view3 = null;
        this.view4 = null;
    } /* constructor */
    
    resize(ev) {
      this.view1.resize(ev);
      this.view1.updateOneImage();
      if (this.view2 != null)
      {
        this.view2.resize(ev);
        this.view2.updateOneImage();
      }
      if (this.view3 != null)
      {
        this.view3.resize(ev);
        this.view3.updateOneImage();
      }
      if (this.view4 != null)
      {
        this.view4.resize(ev);
        this.view4.updateOneImage();
      }
    } /* resize */
    
    initEvent() {
      window.addEventListener("resize", ev => this.resize(ev), false);
      
      this.resize(null);
    } /* initEvent */

    setHome() {
      this.tx = 0;
      this.ty = 0;
      this.zx = 2.0;
      this.zy = 2.0;
      
      this.view1.updateOneImage();
      if (this.view2 != null)
      {
        this.view2.updateOneImage();
      }
      if (this.view3 != null)
      {
        this.view3.updateOneImage();
      }
      if (this.view4 != null)
      {
        this.view4.updateOneImage();
      }

    } /* setHome */

    setCursorColor(color) {
      this.colorCursor = color;
        
      this.view1.updateOneImage();
      if (this.view2 != null)
      {
        this.view2.updateOneImage();
      }
      if (this.view3 != null)
      {
        this.view3.updateOneImage();
      }
      if (this.view4 != null)
      {
        this.view4.updateOneImage();
      }

    } /* setCursorColor() */

} /* class ecv_GlobalInfo() */

class ecv_Viewer {
  
  constructor(canvasViewId, textId, filename, globalInfo) {
    this.canvasViewId = canvasViewId;
    this.textId = textId;
    this.filename = filename;
    this.globalInfo = globalInfo;
    
    /* internal value */
    this.startX = 0;
    this.startY = 0;
    this.isMove = false;
    
    this.img = null;
  }
  
  /* ----------------------------------------------------------------------- */
  /* set text in status bar */
  setText(text) {
    document.getElementById(this.textId).textContent = text;
  }
  
  /* ----------------------------------------------------------------------- */
  /* update one image */
  updateOneImage() {
    /* console.log( "upateImg() tx=" + 
                 this.globalInfo.tx.toString() + " ty=" +
                 this.globalInfo.ty.toString() +
                 ")"); */
    
    if (this.img == null)
    {
      return;
    }
    
    this.ctx.imageSmoothingEnabled = false;
    this.ctx.drawImage( this.img,
                        this.globalInfo.tx, this.globalInfo.ty,
                        this.rect.width * this.globalInfo.zx, this.rect.height * this.globalInfo.zy,
                        0 , 0,
                        this.rect.width, this.rect.height);
    
    if (this.globalInfo.tx < 0 )
    {
      this.ctx.beginPath();
      this.ctx.fillStyle = "grey";
      this.ctx.fillRect(0, 0, -this.globalInfo.tx / this.globalInfo.zx, this.rect.height);
      this.ctx.stroke();
    }
    
    if (this.globalInfo.ty < 0 )
    {
      this.ctx.beginPath();
      this.ctx.fillStyle = "grey";
      this.ctx.fillRect(0, 0, this.rect.width, -this.globalInfo.ty / this.globalInfo.zy);
      this.ctx.stroke();
    }
    
    if ( (this.globalInfo.tx + this.rect.width * this.globalInfo.zx ) > this.img.width )
    {
      this.ctx.beginPath();
      this.ctx.fillStyle = "grey";
      this.ctx.fillRect( (- this.globalInfo.tx + this.img.width) / this.globalInfo.zx, 0,
                         this.rect.width, this.rect.height);
      this.ctx.stroke();
    }
    
    if ( (this.globalInfo.ty + this.rect.height * this.globalInfo.zy ) > this.img.height )
    {
      this.ctx.beginPath();
      this.ctx.fillStyle = "grey";
      this.ctx.fillRect( 0, (- this.globalInfo.ty + this.img.height) / this.globalInfo.zy,
                         this.rect.width, this.rect.height);
      this.ctx.stroke();
    }
    
    var myImageData = this.ctx.getImageData( this.globalInfo.cursorX,
                                             this.globalInfo.cursorY,
                                             1, 1).data;
    
    this.setText(
         this.globalInfo.cursorX.toString() + ";" +
         this.globalInfo.cursorY.toString() + " : RGBA " +
         myImageData[0].toString() + "," +
         myImageData[1].toString() + "," +
         myImageData[2].toString() + "," +
         myImageData[3].toString()
    );
    
    this.ctx.beginPath();
    this.ctx.strokeStyle = this.globalInfo.colorCursor;
    this.ctx.moveTo(this.globalInfo.cursorX, 0);
    this.ctx.lineTo(this.globalInfo.cursorX, this.rect.height);
    this.ctx.stroke();
    
    this.ctx.beginPath();
    this.ctx.strokeStyle = this.globalInfo.colorCursor;
    this.ctx.moveTo(0, this.globalInfo.cursorY);
    this.ctx.lineTo(this.rect.width, this.globalInfo.cursorY);
    this.ctx.stroke();
    
  }
  /* ----------------------------------------------------------------------- */
  /* update all images */
  updateAllImages() {
    if (this.globalInfo.view1 != null)
      {
         this.globalInfo.view1.updateOneImage();
      }
    
    if (this.globalInfo.view2 != null)
      {
         this.globalInfo.view2.updateOneImage();
      }
    
    if (this.globalInfo.view3 != null)
      {
         this.globalInfo.view3.updateOneImage();
      }
    
    if (this.globalInfo.view4 != null)
      {
         this.globalInfo.view4.updateOneImage();
      }
  }
  
  /* ----------------------------------------------------------------------- */
  /* handler zoom */
  zoom(ev, factor) {
    var px, py;
    px = this.globalInfo.tx + this.globalInfo.cursorX * this.globalInfo.zx;
    py = this.globalInfo.ty + this.globalInfo.cursorY * this.globalInfo.zy;
    this.globalInfo.zx *= factor;
    this.globalInfo.zy *= factor;
    this.globalInfo.tx = px - this.globalInfo.cursorX * this.globalInfo.zx;
    this.globalInfo.ty = py - this.globalInfo.cursorY * this.globalInfo.zy;
    this.updateAllImages();
  }
  
  /* ----------------------------------------------------------------------- */
  /* handler on load image */
  onLoadImage(ev) {
    this.updateOneImage();
    this.setText("image loaded");
  }
  
  /* ----------------------------------------------------------------------- */
  /* handler on mouse down */
  onMouseDown(ev) {
    this.startX = ev.clientX - this.rect.left;
    this.startY = ev.clientY - this.rect.top;
    this.globalInfo.cursorX = ev.clientX - this.rect.left;
    this.globalInfo.cursorY = ev.clientY - this.rect.top;
    this.isMove = true;
    
    this.updateAllImages();
  }
  
  /* ----------------------------------------------------------------------- */
  /* handler on mouse up */
  onMouseUp(ev) {
    this.isMove = false;
    this.globalInfo.cursorX = ev.clientX - this.rect.left;
    this.globalInfo.cursorY = ev.clientY - this.rect.top;
    this.updateAllImages();
  }
  
  /* ----------------------------------------------------------------------- */
  /* handler on mouse move */
  onMouseMove(ev) {
    this.mouseX = ev.clientX - this.rect.left;
    this.mouseY = ev.clientY - this.rect.top;
    if (this.isMove === true) {
      this.globalInfo.tx += (this.startX - this.mouseX) * this.globalInfo.zx;
      this.globalInfo.ty += (this.startY - this.mouseY) * this.globalInfo.zy;
      this.updateAllImages();
      this.startX = this.mouseX;
      this.startY = this.mouseY;
      this.globalInfo.cursorX = this.mouseX;
      this.globalInfo.cursorY = this.mouseY;
    }
  }
  
  /* ----------------------------------------------------------------------- */
  /* handler on keyDown */
  onKeyDown(ev) {
    // console.log("keyCode=" + ev.keyCode.toString());
    /*  "w" : 87
     *  "x" : 88
     *  "+" : 107
     *  "-" : 109
     */
    if ( (ev.keyCode == 87) || (ev.keyCode == 109) ) /* "w" or "-" */
      {
        // console.log("w or -");
        this.zoom(ev, 1.1);
      }
    else if ( (ev.keyCode == 88) || (ev.keyCode == 107) ) /* "x"  or "+" */
      {
        // console.log("x or +");
        this.zoom(ev, 1.0/1.1);
      };
  } /* onKeyDown() */
  
  /* ----------------------------------------------------------------------- */
  /* handler on keyDown */
  onWheel(ev) {
    // console.log("ev.deltaY=" + ev.deltaY.toString());
    this.zoom(ev, 1.0 + ev.deltaY/30);
  }
  

  /* ----------------------------------------------------------------------- */
  resize(ev) {
    // console.log("resize");
    var ww = window.innerWidth;
    var wh = window.innerHeight;
    
    // console.log("resize w=" + ww.toString() + "," + wh.toString());
    
    if (this.globalInfo.view3!=null)
    {  /* three or four view */
      this.ctx.canvas.width = (ww - 50) / 2;
      this.ctx.canvas.height = (wh - 150) / 2;
    }
    else if (this.globalInfo.view2!=null)
    { /* two view */
      this.ctx.canvas.width = (ww - 50) / 2;
      this.ctx.canvas.height = wh - 95;
    }
    else
    {  /* one view */
      this.ctx.canvas.width = (ww - 25);
      this.ctx.canvas.height = wh - 95;
    }
    
    this.rect = this.canvas.getBoundingClientRect();
    
  } /* resize() */
  
  /* ----------------------------------------------------------------------- */
  /* init canvas and load image */
  initImage() {
    // this.setText("call initImage()");
    
    this.canvas = document.getElementById(this.canvasViewId);
    // rect est un objet DOMRect avec 6 propriétés
    // left, top, right, bottom, width, height
    this.rect = this.canvas.getBoundingClientRect();
    this.ctx = this.canvas.getContext("2d");
    this.ctx.imageSmoothingEnabled = false;
    this.ctx.strokeStyle = "#FFFFFF";
    
    this.img = new Image();
    this.img.addEventListener("load", ev => this.onLoadImage(ev), false);
    this.img.src = this.filename; // define source of image
    
    /* set event handler */
    this.canvas.addEventListener("mousedown", ev => this.onMouseDown(ev), false);
    this.canvas.addEventListener("mouseup"  , ev => this.onMouseUp(ev)  , false);
    this.canvas.addEventListener('mousemove', ev => this.onMouseMove(ev), false);
    this.canvas.addEventListener("keydown"  , ev => this.onKeyDown(ev)  , false);
    this.canvas.addEventListener("wheel"    , ev => this.onWheel(ev)    , false);
    
  } /* initImage() */
  
} /* class ecv_Viewer() */


var filename1;
filename1=null;
var filename2;
filename2=null;
var filename3;
filename3=null;
var filename4;
filename4=null;

var globalInfo;

function draw() {
  /* search filename */
  const url = new URL(document.URL);

  // document.getElementById("textZone").textContent = url.search;
  
  var params = url.searchParams;
  var f1 = params.get('f1');
  var f2 = params.get('f2');
  var f3 = params.get('f3');
  var f4 = params.get('f4');
  
  document.getElementById("f1").textContent = f1;
  document.getElementById("f2").textContent = f2;
  document.getElementById("f3").textContent = f3;
  document.getElementById("f4").textContent = f4;
  
  /* console.log("f1=" + f1);
   *console.log("f2=" + f2);
   */
  filename1 = f1;
  filename2 = f2;
  filename3 = f3;
  filename4 = f4;
  
  var nImages;

  // var globalInfo;
  globalInfo = new ecv_GlobalInfo();
  
  globalInfo.view1 = new ecv_Viewer("imageView_1", "textZone_1", f1, globalInfo);
  globalInfo.view1.initImage();
  nImages = 1;
  
  if (f2 != null)
  {
    globalInfo.view2 = new ecv_Viewer("imageView_2", "textZone_2", f2, globalInfo);
    globalInfo.view2.initImage();
    nImages = 2;
  }
  
  if (f3 != null)
  {
    globalInfo.view3 = new ecv_Viewer("imageView_3", "textZone_3", f3, globalInfo);
    globalInfo.view3.initImage();
    nImages = 3;
  }

  if (f4 != null)
  {
    globalInfo.view4 = new ecv_Viewer("imageView_4", "textZone_4", f4, globalInfo);
    globalInfo.view4.initImage();
    nImages = 4;
  }

  // console.log("nImages=" + nImages.toString() );

  if (nImages == 1)
  {
    document.getElementById("d2").hidden = true;
    document.getElementById("top_d34").hidden = true;
  }
  
  if (nImages == 2)
  {
    document.getElementById("top_d34").hidden = true;
  }

  if (nImages == 3)
  {
    document.getElementById("d4").hidden = true;
  }

  globalInfo.initEvent();
  
} /* draw() */

function setHome()
{
  // console.log( "setHome()");
  globalInfo.setHome();
} /* setHome() */

function setCursorRed()
{
  // console.log( "setCursorRed()");
  globalInfo.setCursorColor("red");
} /* setCursorRed() */

function setCursorGreen()
{
  // console.log( "setCursorGreen()");
  globalInfo.setCursorColor("green");
} /* setCursorGreen() */

function setCursorBlue()
{
  // console.log( "setCursorBlue()");
  globalInfo.setCursorColor("blue");
} /* setCursorBlue() */



/* end of file */
