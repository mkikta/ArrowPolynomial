import arrow_polynomial as ap

# Data structure representing the symbols for a single crossing in a Gauss
# code.
class code:
    
    def __init__(self, is_over, number, sign):
        self.is_over = is_over
        self.number = number
        self.sign = sign
        
    def __str__(self):
        res = "O" if self.is_over else "U"
        res += str(self.number)
        res = res + "+" if self.sign else res + '-'
        return res

# Representation of a Gauss code as a list of single-crossing codes. Has
# methods to check validity and to convert it into a signed planar diagram.
class gauss_code:
    
    def __init__(self, codes):
        self.codes = codes
    
    # Convert this gauss code to a signed planar diagram representation of the
    # same knot.
    def convert_to_pd(self):
        crossings = {}
        
        # The label on the arc coming into the crossing.
        arc_num = 0
        for code in self.codes:
            
            # The label on the arc going out of the crossing.
            next_arc_num = (arc_num + 1) % len(self.codes)
            
            # The first time we encounter a label in this gauss code, we create
            # a new crossing in the planar diagram.
            if code.number not in crossings:
                
                # Recall that the arcs are to be stored as the end of the 
                # overcrossing arc first, then proceeding clockwise. Store the
                # labels for the arc we are on, and leave the other labels
                # blank.
                if code.is_over:
                    crossings[code.number] = ap.crossing(code.sign,\
                        [next_arc_num, None, arc_num, None])
                elif code.sign:
                    crossings[code.number] = ap.crossing(code.sign, 
                        [None, arc_num, None, next_arc_num])
                else:
                    crossings[code.number] = ap.crossing(code.sign, 
                        [None, next_arc_num, None, arc_num])
           
            # If this label has already been encountered, add to the crossing
            # the labels on the arc we are currently on.
            else:
                if code.is_over:
                    crossings[code.number].labels[0] = next_arc_num
                    crossings[code.number].labels[2] = arc_num    
                elif code.sign:
                    crossings[code.number].labels[1] = arc_num
                    crossings[code.number].labels[3] = next_arc_num
                else:
                    crossings[code.number].labels[1] = next_arc_num
                    crossings[code.number].labels[3] = arc_num
            arc_num += 1
            
        return ap.planar_diagram(list(crossings.values()))
    
    # Determine whether this Gauss code is valid.
    def is_valid(self):
        validation = {}
        
        # Track the over/under information and sign of each code with the same
        # label.
        for code in self.codes:
            if code.number not in validation:
                validation[code.number] = [code.is_over, code.sign]
            else:
                validation[code.number].append(code.is_over)
                validation[code.number].append(code.sign)
                
        # This Gauss code is invalid if there aren't exactly two occurences of
        # single-crossing codes with the same label, if they both have the 
        # same over/under information, or if they have different signs.
        for k, v in validation.items():
            if len(v) != 4 or v[0] == v[2] or v[1] != v[3]:
                return False
        return True
    
    # Return the arrow polynomial of the knot this gauss code represents.
    def arrow_poly(self):
        pd = self.convert_to_pd()
        return pd.arrow_poly()
    
    def __str__(self):
        res = ""
        for code in self.codes:
            res += str(code)
        return res
        