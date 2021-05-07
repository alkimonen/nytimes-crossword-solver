# The New York Times 5x5 AI based Crossword Solver

This project implements an AI based puzzle solver in order to solve [NY Times Mini Crossword](https://www.nytimes.com/crosswords/game/mini "NYT Mini Crossword"). You can get more information below.

## Description of AI
There are several terms that should be defined before getting into the description. “Cell” is one letter of 5x5 crossword with a certain row and a column number, “Root” is the first CrosswordTree instance created, “Block” means the cell is black and does not contain a letter, “Across” and “Down” are the clue types that are respectively horizontally and vertically defined.

The AI of the program works in iterations. Each iteration, the program traces the cells in the crossword, searches the answers for its clues and proceeds recursively. We use demand-based scraping where the clue is only searched when it is asked to return the possible candidates which these candidates are also filtered with the constraint of the hidden word. In each iteration, the current crossword’s score is calculated and compared with the best crossword yet. If the score is higher than the best one, which we will describe the scoring of the puzzle later in the report, it saves the current crossword. The AI returns the crossword only if all cells are solved for both across and down clues. If the crossword is not solved after tracing all cells in the root, the AI returns the best crossword as the answer [3].
### Data Structures
Clues are divided and saved as across and down. They initially have values ‘id’ which is the number of the clue and ‘text’ which is the clue itself. After initialization of Solver class, ‘length’, ‘words’, and ‘searched’ attributes are added. These store respectively the length of the answer to the clue, the candidate word list, and whether it is searched or not.
All cells are held in a 2D cell array which is called a crossword. Each cell contains one long string for the character, the boolean for identifying if the cell is blocked and separate booleans for whether the clues are solved for across and down. Also if the cell is a starting point of a clue, it holds the number of the clue.
### Search Procedure
Iteration in the project is to trace the cells in the crossword and proceeds recursively. As already mentioned, the search procedure is demand-based where the search is only conducted when it is called in iterations. During these iterations, the program searches for the answers to the clues. If it is searched before, the program reaches the candidate words that are already stored in a global data structure. Otherwise, the program follows the search procedure. This is why the program runs slower in the first 10-15 iterations. It creates an empty list, adds the original clue to it and then looks for some special characters in the clue text. If it contains commas, the program splits the clue into pieces between them and appends the divided parts into the list. If the clue contains ‘:’, everything before that point is added to the list. In the end, each item in the list is searched in two different sources.

First, the program uses Wikipedia API in Python. We search for articles related to our item. Then we get the names of the articles together with the first 20 sentences in them. Secondly, we search encyclopedia.com using Selenium web driver and scrape names and descriptions of the results. In the end, we split all results into words and put them into a word list.

After getting a general word list for a clue, the program applies some word checks for the list. We use n as the length of the answer. The words that are n+1 characters and have ‘S’ or punctuation at the end are added back to the list by removing their last character. Then we eliminate every word that does not have the length n. We also remove every word that still has punctuation. Last, we eliminate some words if they are repeated words and conjunctions (he, it, not, but, this, that, hence, etc.).
### Deciding If Crossword Is Solved
In order to decide if a crossword is solved or not, the program traces each cell in the current crossword. Every cell being filled is not necessarily meant that crossword is solved, where to say that crossword is solved, both across and down clues of each cell should be solved, then crossword is solved. Otherwise, it is not solved yet.
### Best Solution And Scoring System
In case the crossword is not solved after iterating all possibilities, the program stores its best solution in the process and returns it at the end. In each iteration, the score of the current crossword is calculated and compared with the best solution. If it has a higher score, then the current is the best solution yet. The score is the sum of the scores of each cell.

The cell gets the score:
- 5: if both across and down clue is solved
- 1: if only one of across or down clue is solved
- 0: if none of the clues are solved

### Solving The Crossword
The program’s decision making is done recursively in the solve() function of the CrosswordTree class. The algorithm starts by tracing cells in order to find an unsolved cell. However, in order to have a loop-free search tree and also for some performance optimizations, the function takes two parameters. These are starting row and column values to start tracing. This way, children nodes do not trace the cells already visited by their parents. In addition, we also use recursion. This also eliminates the possibility of state repetition of the crossword.

The program traces each cell in order to understand if a cell is the starting point of a clue. It first checks the across clues and then down clues. If it is a starting point and also it is unsolved for that clue, the solving stage for the cell starts. First, the program searches for the answers and gets a candidate word list. Then it iterates the list by trying all of them one by one.

For each word, a new crossword matrix is created. The program then iterates the word in rows or columns according to the clue’s type. If there is a mismatch, the new matrix is deleted and iteration continues with another word. Otherwise, a child is created and its solve function is called recursively with this new matrix.

After iterating every cell, the program checks whether the crossword is solved or not. If it is solved, the function returns the current crossword. Otherwise, the current crossword is compared with the best global crossword and saves itself if the current has a higher score. It then returns None as it is not fully solved.

When the recursive function is done and the program returns to the main solver, the return value is evaluated. If it is not None, then the crossword is fully solved and could be returned as the result. Otherwise, it is partially solved and the best scoring crossword should be returned to the user. In the end, the resulting crossword is drawn next to the original crossword and clue descriptions.
