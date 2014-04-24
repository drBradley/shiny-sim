Shiny-Sim
=========

# About

Shiny-Sim is a molecular dynamics simulator, which allows to
investigate the behavior of physical objects.

In shiny-sim I stick to two major objects

* PhysicalBodies - An physical object which can be described with its
  position and mass
* Interactions - describes the relation between two physical bodies,
  and exert on them force

The simulation of honeycomb structure in which one segment was
initially moved in positive z direction.

![alt text](https://raw.githubusercontent.com/drBradley/shiny-sim/master/screen-14-04-2014
 "Honeycomb structure with 'fixed' frame")

# Dependiencies

* Python 2.7
* PyQt 4.10
* Numpy 1.8.1
* Scipy 0.13.3

# Run it

```bash
% python main.py <grid_data> <init>
```

Where <grid-data> is a list of physical bodies nad interactions between
them.
Description of physical body consist of kind of a PhysicalBody,
followed by it x, y, and z coordinates and it's mass.

```
<PhysicalBody> <x> <y> <z> <mass>
```

Already implemented PhysicalBodies are
* Body

Description of interaction consist of Interaction, followed by indexes
of Bodies it interacts with, and a value of a constant specific for given interaction.

```
<Interaction> <r_index> <l_index> <constant>
```

Already implemented Interactions are
* String

## Example

```
Body 50 50 0 10
Body 76 50 0 10
Body 128 50 0 10
String 0 1 10
String 1 38 10
String 2 3 10
```

It is also possible to move objects from their initial state using  <init>.

```
<operation> <index> <x> <y> <z>
move 38*18+18 0 0 1.5
move 38*18+19 0 0 1.5
move 38*19+17 0 0 1.5
```

## Having problems ?

Alternatively you can use grid_generator for creating grid data.

```bash
% python frid_generator.py <x_size> <y_size> <output> <configuration>
```

where

* x_size - number of particles in a row
* y_size - number of rows
* output - output file
* configuration - one of the following options
  * 0 - plain square grid
  * 1 - plain honeycomb grid
