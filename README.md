This script and its subfunctions aim to calculate the motion and most importantly
the resulting force for a climbing fall.

**Simplifications**
- climber modelled as point mass
- rope attachement point = COG of climber
- no rope drag
- simplified rope length calculation
- rope considered as 1D linear elastic
- quickdraw & carabiner modelled as singular attachment point (infinite stiffness)
- static belay (for now) --> belay attachment modelled as fix point
- simulation stops when contact to the wall is detected and outputs the present velocity
    
**Input parameters**:
- height of highest quickdraw
- height of climber
- mass of climber
- angle of wall to the vertical plane
- Stiffness modulus of rope (Young's modulus * crossectional area)
- rope slack (additionall length)                                 
                                 
**Output**:
- Climber position over time
- scalar rope force
- force at quickdraw
