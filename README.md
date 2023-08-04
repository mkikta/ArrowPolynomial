# The Arrow Polynomial

The arrow polynomial is an invariant of virtual links, which may be calculated recursively by expanding each crossing of a link diagram. In terms of a Gauss code, this computation lends itself nicely to being solved algorithmically.

This program takes the Gauss code of a knot as user input in a REPL, converts the Gauss code into a planar diagram, performs the algorithm outlined in (Bhandari, 2009) to compute the arrow polynomial of the knot underlying the planar diagram, and prints out the normalized Dye-Kauffman arrow polynomial. 

An example of an expected input is a Gauss code of the form **O1-O2-U1-U2-O3+O4+U3+U4+**, where **O**/**U** denotes over/under information, the numbers are crossing labels, and **+**/**-** denotes the handedness of a crossing. Alternatively, enter "quit" to terminate the program.

In the future, I plan to modify the program to be able to calculate the arrow polynomial of virtual links with more than one component. Conveniently, implementing this would not require changing any part of the algorithm after the calculation of states. I also plan to enable the functionality for users to make variable substitutions, as the initial motivation for designing this program was to explore a potential relationship between the arrow polynomial and the two Jones-type polynomials in (Boninger, 2022).

# References

Bhandari, K. (2009). Computing the Arrow Polynomial. _Rose-Hulman Undergraduate Mathematics Journal_, 10 (1). https://scholar.rose-hulman.edu/rhumj/vol10/iss1/2

Boninger, J. (2022). The Jones Polynomial from a Goeritz Matrix. _Bulletin of the London Mathematical Society, 55_(2), 732-755.  https://doi.org/10.1112/\\blms.12753
