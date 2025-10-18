import sys
import copy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Check every variable
        for var in self.domains:
            # get variable values
            # Check every entry in variable's domain
            for entry in self.domains[var]:
                # Update domain with new, node consistent list
                if len(entry) != var.length:
                    self.domains[var] = {
                        n for n in self.domains[var] if n != entry
                    }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
       
        
        
        
        # return revised
        
        # Initialize revised
        revised = False
        # Get overlap for combination
        overlap = self.crossword.overlaps[x, y]

        if overlap == None:
            domain_x = copy.deepcopy(self.domains[x])
            # for x in X.domain:
            for dom_x in self.domains[x]:
                # if no y in Y.domain satisfies constraint for (X,Y):
                satisfied = False
                for dom_y in self.domains[y]:
                    if dom_y != dom_x:
                        satisfied = True
                if satisfied == False:
                    # delete x from X.domain
                    self.domains[x] = {
                        n for n in self.domains[x] if n != dom_x
                    }
                    # revised = true
                    revised = True
        else:
            offset_x = abs((x.i + x.j) - (overlap[0] + overlap[1]))
            offset_y = abs((y.i + y.j) - (overlap[0] + overlap[1]))
            # for x in X.domain:
            for dom_x in self.domains[x]:
                # if no y in Y.domain satisfies constraint for (X,Y):
                satisfied = False
                for dom_y in self.domains[y]:
                    if dom_x[overlap[0]] == dom_y[overlap[1]]:
                        satisfied = True
                if satisfied == False:
                    # delete x from X.domain
                    self.domains[x] = {
                        n for n in self.domains[x] if n != dom_x
                    }
                    # revised = true
                    revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # queue = all arcs in csp
        queue = []
        if arcs == None:
            # Add constraint solutions must be unique (a != b != c ...) to queue
            for var_1 in self.crossword.variables:
                for var_2 in self.crossword.variables:
                    if var_1 is not var_2 and (var_1, var_2) not in queue:# and (var_2, var_1) not in queue:
                        queue.append((var_1, var_2))
        else:
            queue = arcs
        # while queue non-empty:
        while len(queue) > 0:
            # (X, Y) = Dequeue(queue)
            test = queue.pop(0)
            x = test[0]
            y = test[1]
            # if Revise(csp, X, Y): 
            if self.revise(x, y):
                # if size of X.domain == 0:
                #     return false
                if len(self.domains[x]) == 0:
                    return False
                # for each Z in X.neighbors - {Y}:
                #     Enqueue(queue, (Z,X))
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # i = (n for n in assignment if assignment[n] != None)
        if len(assignment) == len(self.crossword.variables):
            return True
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Empty assignment is valid
        if assignment == dict():
            return True
        # Iterate over each variable in assignment
        for var, word in assignment.items():
            # Return flase if assigned word doesn't fit in variable's length
            if var.length != len(word):
                return False
            # Secont iterate for comparison \
            for var_2, word_2 in assignment.items():
                # Prevent collision
                if var_2 is not var:
                    # Return false if words are the same
                    if word == word_2:
                        return False
                    # Get overlap for variables
                    overlap = self.crossword.overlaps[var, var_2]
                    if overlap:
                        # Return false if words conflict at overlap
                        if word[overlap[0]] != word_2[overlap[1]]:
                            return False
        # Return true if consistent
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Initialize values list
        values = []
        # Dictionary for sorting
        val_elim = dict()
        # Get neighbors of var
        neighbors = self.crossword.neighbors(var)
        # Check all values of var
        for val in self.domains[var]:
            # Count eliminated words
            elim = 0
            # Eliminate potential neighbor words
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                for dom in self.domains[neighbor]:
                    if val[overlap[0]] != dom[overlap[1]]:
                        elim += 1
            val_elim[val] = elim
        # Sort by value, return best choice
        sort = dict(sorted(val_elim.items(), key=lambda item: item[1]))
        values = list(sort.keys())
        return values


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Variable to consider
        consider = None
        neighbors = None
        # Check each variable not in assignment
        for dom in self.domains:
            if dom not in assignment:
                # Always consider the first
                if not consider:
                    consider = dom
                    neighbors = self.crossword.neighbors(dom)
                # Check if we should consider later variables
                else:
                    # Choose var with smallest domain
                    if len(self.domains[dom]) < len(self.domains[consider]):
                        consider = dom
                        neighbors = self.crossword.neighbors(dom)
                    # If equal domain length, choose var with most neighbors
                    elif len(self.domains[dom]) == len(self.domains[consider]):
                        if len(self.crossword.neighbors(dom)) > len(neighbors):
                            consider = dom
                            neighbors = self.crossword.neighbors(dom)
        # Returns variable to consider if it exists
        if consider:
            return consider

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        # if assignment complete:
        #     return assignment
        # var = Select-Unassigned-Var(assignment, csp)
        # for value in Domain-Values(var, assignment, csp):
        #     if value consistent with assignment:
        #         add {var = value} to assignment
        #         result = Backtrack(assignment, csp)
        #         if result ≠ failure:
        #             return result
        #         remove {var = value} from assignment
        # return failure

        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.consistent(assignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result == assignment:
                    return result
                assignment.pop(var)
                self.domains[var] = {
                    n for n in self.domains[var] if n != value
                }
        # Return none if assignment empty, no solution
        if assignment == dict():
            return None
        return assignment

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
