from retriever import CrosswordDataRetriever
from crosswordGUI import CrosswordGUI
from data import DataStore
from solver import Solver

index = -1
old_data = DataStore.get_old_data()
crosswordData = old_data[index]['data']
solution = None

crosswordData = CrosswordDataRetriever().retrieve_crossword()
print( crosswordData)
solution = Solver(crosswordData).solve_crossword()

print("\n", end="")
if solution != None:
    print("=======================================================================================")
    print("Finished")
    DataStore.print_grid(solution)
    gui = CrosswordGUI(retData=crosswordData, solvedData=solution)
    print("\nDate:", old_data[index]['date'])
else:
    gui = CrosswordGUI(retData=crosswordData, solvedData=crosswordData)
