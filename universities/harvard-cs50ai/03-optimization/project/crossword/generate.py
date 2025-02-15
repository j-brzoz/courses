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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        domains_copy = copy.deepcopy(self.domains)

        for var in domains_copy:
            for word in domains_copy[var]:
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        if self.crossword.overlaps[x, y]:

            # find coordinates of overalping words
            coordinates = self.crossword.overlaps[x, y]

            domains_copy = copy.deepcopy(self.domains)

            for word_x in domains_copy[x]:
                matched = False
                for word_y in self.domains[y]:
                    # if the same, no need in checking other word_ys
                    if word_x[coordinates[0]] == word_y[coordinates[1]]:
                        matched = True
                        break
                # if not the same, remove word_x and change 'revised'
                if not matched:
                    self.domains[x].remove(word_x)
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
        queue = []
        if arcs is None:
            # add 'arcs' to the queue
            for overlap in self.crossword.overlaps:
                queue.insert(0, overlap)

        while queue != []:
            x, y = queue.pop()
            # check for revision
            if self.revise(x, y):
                # check if there is solution
                if self.domains[x] == 0:
                    return False
                # add new arcs to the queue
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.insert(0, (z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = set()
        for var in assignment:
            # check if length is correct
            if var.length != len(assignment[var]):
                return False

            # check for duplicates
            if assignment[var] in words:
                return False
            else:
                words.add(assignment[var])

            # check for coflicts with neighbors
            for nghbr in self.crossword.neighbors(var):
                if nghbr in assignment:
                    coordinates = self.crossword.overlaps[var, nghbr]
                    if (assignment[var][coordinates[0]] !=
                            assignment[nghbr][coordinates[1]]):
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        words = dict()

        for word in self.domains[var]:
            # add word to dictionary
            words[word] = 0
            for nghbr in self.crossword.neighbors(var):
                # ignore if neighbor has value already
                if nghbr not in assignment:
                    # check for eliminations
                    coordinates = self.crossword.overlaps[var, nghbr]
                    for nghbr_word in self.domains[nghbr]:
                        if word[coordinates[0]] != nghbr_word[coordinates[1]]:
                            words[word] += 1
        # sort dictionary
        return sorted(words)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        var_min_value = float('inf')
        var_max_degree = 0

        for var in self.domains:
            if var not in assignment:
                # find the variable with the fewest values in its domain
                if len(self.domains[var]) < var_min_value:
                    var_name = var
                    var_min_value = len(self.domains[var])
                    var_max_degree = len(self.crossword.neighbors(var))

                # if tie, choose variable that has the largest degree
                elif len(self.domains[var]) == var_min_value:
                    if len(self.crossword.neighbors(var)) > var_max_degree:
                        var_name = var
                        var_min_value = len(self.domains[var])
                        var_max_degree = len(self.crossword.neighbors(var))
        return var_name

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # check if assignment is ready
        if self.assignment_complete(assignment):
            return assignment

        # select unassigned variable
        var = self.select_unassigned_variable(assignment)

        # find value for variable
        for value in self.order_domain_values(var, assignment):
            # make copy to check if variable would be consistent
            assignment_copy = assignment.copy()
            assignment_copy[var] = value
            if self.consistent(assignment_copy):
                result = self.backtrack(assignment_copy)
                if result is not None:
                    return result
        return None


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
