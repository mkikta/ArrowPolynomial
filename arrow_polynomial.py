from sympy import Symbol, simplify
import copy

# Data structure representing an arc. If the arc is oriented, then the first
# label represents the start of the arc and the second label the end. If it is
# unoriented, then the labels represent the endpoints of the arc.
class arc:
    
    def __init__(self, is_oriented, label):
        self.is_oriented = is_oriented
        self.label = label
        
    def __str__(self):
        return "[ " + str(self.is_oriented) + " | " + str(self.label[0]) + \
            ", " + str(self.label[1]) + " ]"

# Data structure representing a classical crossing. The labels on the strands
# go clockwise starting at the end of the overcrossing strand.
class crossing:
    
    def __init__(self, handedness, labels):
        self.handedness = handedness
        self.labels = labels
        
    def __str__(self):
        return "[ " + str(self.handedness) + " | " + str(self.labels[0]) + \
            ", " + str(self.labels[1]) + ", " + str(self.labels[2]) + ", " + \
                str(self.labels[3]) + " ]"

# Data structure to be used in the state expansion calculation of the arrow 
# polynomial. Tracks the weight associated with the state in the expansion.
class state:
    
    def __init__(self, weight, arcs):
        self.weight = weight
        self.arcs = arcs
     
    # Reduce the arcs of this diagram to aid in calculation.                 
    def reduce(self):
        
        # Helper method.
        def find_reduction():
            
            # Consider whether each pair of arcs in this state may be reduced.
            for i in range(len(self.arcs)):
                for j in range(len(self.arcs)):
                    if i != j:
                        
                        # If there exist two adjacent unoriented arcs, they may
                        # be reduced to one unoriented arc.
                        if (not self.arcs[i].is_oriented) and (not \
                            self.arcs[j].is_oriented) and \
                            self.arcs[i].label[1] == self.arcs[j].label[0]:
                            self.arcs[i].label[1] = self.arcs[j].label[1]
                            self.arcs.pop(j)
                            return True
                        elif (not self.arcs[i].is_oriented) and (not \
                            self.arcs[j].is_oriented) and \
                            self.arcs[i].label[1] == self.arcs[j].label[1]:
                            self.arcs[i].label[1] = self.arcs[j].label[0]
                            self.arcs.pop(j)
                            return True
                        
                        # If there exist two adjacent arcs with the same
                        # orientation, they may be reduced to one unoriented
                        # arc.
                        elif self.arcs[i].is_oriented and \
                            self.arcs[j].is_oriented and self.arcs[i].label[1]\
                                == self.arcs[j].label[0]:
                            self.arcs[i].label[1] = self.arcs[j].label[1]
                            self.arcs[i].is_oriented = False
                            self.arcs.pop(j)
                            return True
                        
                        # If there exist an oriented arc and an adjacent
                        # unoriented arc, they may be reduced to one oriented
                        # arc.
                        elif self.arcs[i].is_oriented and (not \
                            self.arcs[j].is_oriented) and \
                            self.arcs[i].label[1] == self.arcs[j].label[0]:
                            self.arcs[i].label[1] = self.arcs[j].label[1]
                            self.arcs.pop(j)
                            return True
                        elif self.arcs[i].is_oriented and (not \
                            self.arcs[j].is_oriented) and \
                            self.arcs[i].label[1] == self.arcs[j].label[1]:
                            self.arcs[i].label[1] = self.arcs[j].label[0]
                            self.arcs.pop(j)
                            return True
                        elif self.arcs[i].is_oriented and (not \
                            self.arcs[j].is_oriented) and \
                            self.arcs[i].label[0] == self.arcs[j].label[0]:
                            self.arcs[i].label[0] = self.arcs[j].label[1]
                            self.arcs.pop(j)
                            return True
                        elif self.arcs[i].is_oriented and (not \
                            self.arcs[j].is_oriented) and \
                            self.arcs[i].label[0] == self.arcs[j].label[1]:
                            self.arcs[i].label[0] = self.arcs[j].label[0]
                            self.arcs.pop(j)
                            return True
            
            # If no reduction was found, then we are done.
            return False
        
        # Reduce this state as much as possible.
        while(find_reduction()):
            pass
    
    # Count the number of loops in this state and the powers of the k_i.
    def determine_loops_and_states(self):
        tmp = copy.deepcopy(self.arcs)
        
        # The first entry of result is the number of loops in this state, ith
        # entry of result is the power of k_i for i > 0. Note there cannot be
        # more loops than arcs in this state.
        result = [0] * len(tmp)
        i = 0
        
        # Count the number of loops that are just one arc. They cannot
        # contribute any k_i since they have at most one arrow.
        while i < len(tmp):
            if tmp[i].label[0] == tmp[i].label[1]:
                result[0] += 1
                tmp.pop(i)
            else:
                i += 1
                
        # Count the number of other loops and the number of arrows on each of
        # them. Note that every arc in a reduced state will have an arrow as
        # long as it is not the only arc in a loop.
        while 0 < len(tmp):
            first = tmp[0].label[0]
            last = tmp[0].label[1]
            arrow_count = 1
            tmp.pop(0)
            
            # Add arcs to the large arc from first to last, until first equals
            # last, at which point it is a loop.
            while first != last:
                i = 0
                while i < len(tmp):
                    if first == tmp[i].label[0]:
                        first = tmp[i].label[1]
                        tmp.pop(i)
                        arrow_count += 1
                    elif first == tmp[i].label[1]:
                        first = tmp[i].label[0]
                        tmp.pop(i)
                        arrow_count += 1
                    elif last == tmp[i].label[0]:
                        last = tmp[i].label[1]
                        tmp.pop(i)
                        arrow_count += 1
                    elif last == tmp[i].label[1]:
                        last = tmp[i].label[0]
                        tmp.pop(i)
                        arrow_count += 1
                    else:
                        i += 1
                  
            # Inrement the number of loops, and increment the exponent on the
            # proper k_i.
            result[0] += 1
            if 1 <= arrow_count // 2:
                result[arrow_count // 2] += 1
                
        # Account for a simple loop with no labels.
        if result == []:
            return [1]
        return result
            
    
    def __str__(self):
        res = str(self.weight) + ", < "
        for arc in self.arcs:
            res += str(arc) + " "
        return res + ">"
    
# Data structure representing a virtual knot as a list of its crossings.
class planar_diagram:
    
    def __init__(self, crossings):
        self.crossings = crossings
        
        # Calculate and reduce the states of this.
        self.states = self.expand_crossings()
        for state in self.states:
            state.reduce()
         
    # Return the states of this virtual knot
    def expand_crossings(self):
        states = []
        
        # Helper method that expands a the crossing at the given index in a
        # given state.
        def expand_crossing(i, state):
            
            # Base case; add the full state to the list of states.
            if i == len(self.crossings):
                states.append(state)
                return
            
            # Create two branches from the current state, which result from the
            # proper expansion of the current crossing.
            crossing = self.crossings[i]
            branch1 = copy.deepcopy(state)
            branch2 = copy.deepcopy(state)
            A = Symbol("A")
            
            # Expansion if the crossing is positive.
            if crossing.handedness:
                branch1.weight *= A
                branch1.arcs.append(arc(False, [crossing.labels[1], \
                    crossing.labels[0]]))
                branch1.arcs.append(arc(False, [crossing.labels[2], \
                    crossing.labels[3]]))
                branch2.weight /= A
                branch2.arcs.append(arc(True, [crossing.labels[2], \
                    crossing.labels[1]]))
                branch2.arcs.append(arc(True, [crossing.labels[0], \
                    crossing.labels[3]]))
                
            # Expansion if the crossing is negative.
            else:
                branch1.weight *= A
                branch1.arcs.append(arc(True, [crossing.labels[3], \
                    crossing.labels[2]]))
                branch1.arcs.append(arc(True, [crossing.labels[1], \
                    crossing.labels[0]]))
                branch2.weight /= A
                branch2.arcs.append(arc(False, [crossing.labels[2], \
                    crossing.labels[1]]))
                branch2.arcs.append(arc(False, [crossing.labels[3], \
                    crossing.labels[0]]))
                
            # Expand the next crossing within each of the two branches.
            expand_crossing(i + 1, branch1)
            expand_crossing(i + 1, branch2) 
        
        # Recursive call.
        expand_crossing(0, state(1,[]))
        return states
    
   # Calculate the arrow polynomial of this virtual knot.
    def arrow_poly(self):
        A = Symbol("A")
        k = []
        
        # Calculate $\sum_{s\in S}A^{\alpha-\beta}d^{|S|-1}<S>$.
        poly = 0
        for state in self.states:
            loops_and_states = state.determine_loops_and_states()
            term = state.weight * (-A**2-A**(-2)) ** (loops_and_states[0] - 1)
            for i in range(1, len(loops_and_states)):
                k.append(Symbol(f"k_{i}"))
                term *= k[i - 1]**loops_and_states[i]
            poly += simplify(term)

        # Normalize the arrow polynomial. 
        writhe = 0
        for crossing in self.crossings:
            writhe = writhe + 1 if crossing.handedness else writhe - 1
        poly *= ((-A**3)**(-writhe))
        return simplify(poly)
