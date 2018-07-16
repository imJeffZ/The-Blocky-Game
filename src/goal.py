"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """
    
    def __init__(self, target_colour: Tuple[int, int, int]):
        Goal.__init__(self, target_colour)
        
    def score(self, board: Block):
        scores = []
        flattened = board.flatten()
        board_size = len(flattened)
        visited = []
        row = []
        for _ in range(board_size):
            row.append(-1)
        for _ in range(board_size):
            visited.append(row.copy())
        
        for i in range(board_size):
            for j in range(board_size):
                if visited[i][j] == -1:
                    scores.append(self._undiscovered_blob_size((i, j),\
                                                                flattened,\
                                                                 visited))
        return max(scores)
                
    def description(self):
        return "Create the largest blob"
        

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if pos[0] >= 0 and pos[0] < len(board)\
         and pos[1] >= 0 and pos[1] < len(board)\
         and visited[pos[0]][pos[1]] == -1:
            if board[pos[0]][pos[1]] == self.colour:
                visited[pos[0]][pos[1]] = 1
                score = 1
                for i in (-1, 1):
                    score += \
                    self._undiscovered_blob_size((pos[0]+i, pos[1]),\
                                                      board, visited)
                for j in (-1, 1):
                    score += \
                    self._undiscovered_blob_size((pos[0], pos[1]+j),\
                                                      board, visited)
                return score
            else:
                visited[pos[0]][pos[1]] = 0
        return 0
    
class PerimeterGoal(Goal):
    """A goal to create the largest perimeter"""
    
    def __init__(self, target_colour: Tuple[int, int, int]):
        Goal.__init__(self, target_colour)
        
    def score(self, board: Block):
        flattened = board.flatten()
        score = 0
        side_length = len(flattened)
        for i in range(side_length):
            #score left
            if flattened[0][i] == self.colour:
                score += 1
            #score right
            if flattened[-1][i] == self.colour:
                score += 1
            #score top
            if flattened[i][0] == self.colour:
                score += 1
            #score down
            if flattened[i][-1] == self.colour:
                score += 1
        return score
    
    def description(self):
        return "Create the largest perimeter"


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
