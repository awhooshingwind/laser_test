

## Potential DMDs to purchase

### Plug-and-Play USB

* [DLP 4710](https://www.ti.com/tool/DLPDLCR4710EVM-G2) **~$1000**
  - Most expensive module listed, same as referenced in spatial light modulator paper below 
  - 0.47 in array diagonal, 1920x1080 mirror array, 5.4 um mirror pitch
  - [User Guide](https://www.ti.com/lit/ug/dlpu044d/dlpu044d.pdf?ts=1673999527733&ref_url=https%253A%252F%252Fwww.ti.com%252Ftool%252FDLPDLCR4710EVM-G2)
  
* [DLP 3010 EVM-G2](https://www.ti.com/tool/DLPDLCR3010EVM-G2) **~$700**
  - 0.3" array diagonal, 1280x720 mirror array, 5.4 um mirror pitch
  - [User Guide](https://www.ti.com/lit/ug/dlpu058a/dlpu058a.pdf?ts=1674000007331&ref_url=https%253A%252F%252Fwww.ti.com%252Ftool%252FDLPDLCR3010EVM-G2)
 
 #### Needs host processor (RaspPi or similiar to interface) 
 
* Cheaper plug-and-play [DLP 230NP](https://www.ti.com/tool/DLPDLCR230NPEVM) **~$300** *just EVM, not including RaspPi (range from $30-$100)*
  - 0.23" array diagonal, 960x540 mirror array, 5.4 um mirror pitch
  - Smaller (81mm x 87mm)
  - [User Guide](https://www.ti.com/lit/ug/dlpu103a/dlpu103a.pdf?ts=1674000328384&ref_url=https%253A%252F%252Fwww.ti.com%252Ftool%252FDLPDLCR230NPEVM)
  
* Even cheaper, needs more tinkering [DLP LCR2000](https://www.ti.com/tool/DLPDLCR2000EVM) **~$100** *EVM only*
  - 0.2" array diagonal, 640x360 mirror array, 7.6 um mirror pitch
  - Smallest (54mm x 76mm)
  - [User Guide](https://www.ti.com/lit/ug/dlpu049c/dlpu049c.pdf?ts=1674155304087)

Might be possible to work around needing a host processor with USB-I2C dongle...

**Caveats: **

* DMD contained in optics module, some might be more accessible than others...
* Raspberry Pi supply has been low, but should be recovering first part of this year

### HomeBrew Solutions

* DIY approach [DLP230GP](https://www.ti.com/product/DLP230GP)
  - Just one mirror linked, would also need driver chips, etc.

**Caveats: **
* Need to design/build an analog and digital circuit to control DMD properly...plus a way to interface with it...
* Might allow for more custom configurations
* Not purchasing unneeded optics engines

### Conclusions 

Best module will be usage dependent, more complicated ML will likely want a computer with more processing power to run efficiently - bigger concern is required mirror size/number of mirrors for experiment.


## Progress/Guidance

A brief summary of what the very rough code does so far, what I think it could do - with some assistance on how to approach the optics

### Code Demo

* [Repo Link](https://github.com/awhooshingwind/laser_test)

Basically consists of three modules, which would later becomes 'modes' of the running app - a monitoring mode, a laser profiler (fits a gaussian profile curve), and a bitmap image generator.

* Monitor:
  - Plots intensity of a sliced range in real time
  - Displays sliced range on img
  - Fits a gaussian probability curve to intensity curve (slow, not useful, but could be replaced with gaussian profile fit from other module)

* Laser Profiler:
  - adaptation of a laser profiler from github
  - would need advice on how to appropriately use parameters, might not even need directly (depending on goal)
  - added a 3d surface plot of intensity from camera data

* Bitmap Maker
  - rough implementation to manually generate and save bitmaps to explore different effects of mirror configuration

Current 'testing' workflow:
1. Use monitor mode to 'find' slicing range (could be automated, even more easily when things are in fixed positions)
2. Take a laser profile of brightest point (based on slicing range)
3. Adjust bitmap 'filter' image
4. Repeat and visually compare results

---

## Relevant Papers

* [DMD as spatial light modulator](https://opg.optica.org/ao/fulltext.cfm?uri=ao-60-2-465&id=446312)
  - detailed and practical info about DMD mount/optical set up

* [Optical Potentials with DMD and  superluminescent diode](https://journals.aps.org/prresearch/pdf/10.1103/PhysRevResearch.3.033241)
  - using SLD as light source for higher fidelity imaging on atoms
  - more comparison between laser + DMD vs. SLD + DMD (favoring SLD)

* [DMD controlled optical tweezers](https://iopscience.iop.org/article/10.1088/1367-2630/aaa634#njpaaa634bib21)
  - using older DMD to trap/transport atoms with holographically generated optical tweezers
  - more detailed discussion of optics/theory for DMD traps

## Other Resources
* [TI DMD design planning](https://www.ti.com/design-resources/embedded-development/dlp-chip/display-and-projection.html)
* [TI Comparison Sheet](https://www.ti.com/lit/sg/sprt736d/sprt736d.pdf?ts=1674164293371)
* [TI PCB Design Requirements](https://www.ti.com/seclit/an/dlpa071/dlpa071.pdf?ts=1673997424169&ref_url=https%253A%252F%252Fwww.ti.com%252Fdesign-resources%252Fembedded-development%252Fdlp-chip%252Fdisplay-and-projection.html)
