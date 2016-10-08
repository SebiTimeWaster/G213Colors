# G213Colors
A Python script to change the key colors on a Logitech G213 Prodigy Gaming Keyboard (And potentially other keyboards).

## What it does
The commands `chamferCube` and `chamferCylinder` can be used to create chamfered versions of the existing `cube` and `cylinder` commands.

The Chamfers are always at a 45° angle to the ground plane and are printable on Fused deposition modelling (FDM) printers in a good quality.

![Demo of possiblities with chamfers](https://github.com/SebiTimeWaster/OpenSCAD-Chamfer/blob/master/Chamfer.png)

Additionally
* The `chamferCylinder` can also produce a circular sector (wedge), what the cylinder command cannot
* The `circleSegments` function calculates the amount of segments needed for a certain circle radius, it reproduces a much better quality than $fa and $fs settings
* A `globalCircleQuality` variable can be set to globally override the standard setting of 1.0, but the quality setting in `chamferCylinder` stil has precedence over this variable

Changelog v0.3:
* Added a global override for the standard circle quality

Changelog v0.2:
* Added new circle quality feature (segment calculator) which introduces an incompatibility with v0.1
* Prevented cylinders with height 0 from being created when setting chamferHeight to 0

## Installation
* [Download](https://github.com/SebiTimeWaster/Chamfers-for-OpenSCAD/releases) the library
* Unpack it to OpenSCAD\libraries
* Restart OpenSCAD

OR

* Open your console
* Go to OpenSCAD\libraries
* Run ```git clone https://github.com/SebiTimeWaster/Chamfers-for-OpenSCAD.git```
* Restart OpenSCAD

## Usage
Don't forget to import the library to your script by adding this to the first line:

`include <Chamfers-for-OpenSCAD/Chamfer.scad>;`

Please read the documentation in [Demo.scad](https://github.com/SebiTimeWaster/OpenSCAD-Chamfer/blob/master/Demo/Demo.scad) to see how to use it.
