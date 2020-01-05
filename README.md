# simple-python-raytracer

Requires Python3

![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/shadow-plane.png)
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/shadow-suns.png)

![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/neglight.png)
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/many.png)

## Usage
`python raytrace.py input_file.txt`

See `examples` for sample input files.

## Supported operations

+ sphere *x y z r*
Places a sphere of radius *r* with it's center at *x y z*.



+ sun *x y z*
Places a light source infinitely far away in the *x y z* direction.
![sun](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/sun.png)

+ bulb *x y z*
Places a point light source centered at *x y z*. Uses the current color as the color of the bulb. Falls off in intensity following the inverse square law.
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/inside.png)
+ color *r g b*
Sets the current drawing color to *r g b*. Colors are taken as floating point between 0 and 1, where 0, 0, 0 is black and 1, 1, 1 is white.
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/color.png)
+ plane *A B C D*
Places a plane that satisifes the plane equation Ax+By+Cz+D=0
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/plane.png)
+ shininess *s*
Sets flag so future objects have a reflectivity *s*, between 0 and 1.

+ fisheye 
Applies a fisheye effect to the camera
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/fisheye.png)

+ eye *ex ey ez*
Changes the `eye` location used in generating rays
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/eye.png)

+ forward *fx fy fz*
Changes the `forward` direction used in generating rays.
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/forward.png)

+ up *ux uy uz*
Change the `up` direction used in generating rays.
![](https://raw.githubusercontent.com/frostdpr/simple-python-raytracer/master/output/up.png)
