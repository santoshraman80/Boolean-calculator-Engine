# Boolean-calculator-Engine
The Boolean Calculator Engine is an optimized version of my previous project "Boolean Complement Calculation using Unate Recursive Paradigm". Unlike the "boolean complement calculation using URP" where we can complement only one given function at a time, here we can manage several different huge boolean functions (upto 32) and calculate their boolean complements simultaneously using the "Boolean Calculator Engine" and can perform various logical operations. An example of one of the input files's format is given below:

COMMAND FILE
1. r 2 // read in F2
2. r 3 // read in F3
3. ! 4 2 // F4 = F2’
4. ! 5 3 // F5 = F3’
5. & 6 2 5 // F6 = F2 * F5, ie, F2 F3’
6. & 7 3 4 // F7 = F3 * F4, ie, F3 F2’
7. + 0 6 7 // F0 = F6 + F7, ie F2 F3’ + F3 F2’
8. p 0 // output F0 = F2 exor F3
9. q // we are done

!(NOT) , &(AND) , +(OR) for performing logical operations



