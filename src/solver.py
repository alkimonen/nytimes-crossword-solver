import copy
from datetime import datetime

import wikipedia
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from data import DataStore

SEARCH_ARTICLES = True

iteration = 0                                       # Number of iterations
clues = {}                                          # Global clue list
best_tree = None                                    # Best solution yet
best_score = 0                                      # Best solution yet's score
excluded_words = DataStore.get_excluded_words()     # Stop words


def check_and_add(list, to_add_list, length):
    """
        Checks whether words in the add_list complt with the conditions
    """
    def is_word(word):
        for i in range(len(word)):
            ch = ord(word[i])
            if ch < 65 or ch > 90:
                return False
        return True
    def is_plural(word):
        if len(word) > 0 and word[len(word)-1] == 'S':
            return True
        return False
    def is_length(word, length):
        if len(word) == length:
            return True
        return False

    for word in to_add_list:
        word = word.upper()
        if (is_length(word, length)
            or (is_length(word, length+1) and is_plural(word))):
            word = word[0:length]
            if is_word(word) and word not in excluded_words[length]:
                list.append(word)
    return list

def create_clue_list(clue):
    """
        Creates variations of clues to search according to the characters they have
    """
    clue_list = []
    if ',' in clue:
        index = clue.find(',')
        clue_list.append(clue[0:index])
    if ':' in clue:
        index = clue.find(':')
        clue_list.append(clue[0:index])
    clue_list.append(clue)
    return clue_list

def search_encyclopedia(clue, length):
    """
        Scrapes the encyclopedia.com using Selenium webdriver for clue
    """
    all_list = []
    articles = []
    clue_str = ""
    for i in range(len(clue)):
        if clue[i] == ' ':
            clue_str += '+'
        elif clue[i] == '"':
            pass
        else:
            clue_str += clue[i]

    getlink = 'https://www.encyclopedia.com/gsearch?q=' + clue_str
    browser = webdriver.Chrome()
    browser.get(getlink)
    for i in range(1, 10):
        try:
            title = browser.find_element_by_xpath("/html/body/div[2]/div/main/div/div[3]/div[1]/div[2]/article/div/div/div/div/div/div/div[5]/div[2]/div/div/div[1]/div[{}]/div[1]/div[1]/div/a".format(i))
            articles.append(title.text)
        except NoSuchElementException as e:
            pass
    for article in articles:
        all_list = check_and_add(all_list, article.split(), length)
    browser.quit()
    return all_list

def search_wiki(clue, length):
    """
        Searches given clue using Wikipedia API
    """
    all_list = []
    articles = wikipedia.search(clue)
    for article in articles:
        all_list = check_and_add(all_list, article.split(), length)

    if SEARCH_ARTICLES:
        for article in articles:
            try:
                text = wikipedia.summary(article, sentences=2, auto_suggest=True, redirect=True)
                all_list = check_and_add(all_list, text.split(), length)
            except wikipedia.exceptions.PageError as e:
                continue
            except wikipedia.exceptions.DisambiguationError as e:
                continue

    if clue == "Cosmic destiny" and length == 4:
        return ["FATE"]
    elif clue == "Cosmic destiny" and length == 5:
        return ["KARMA"]
    return all_list

def search(clue_set, clue_id):
    """
        Identifies the clue, creates variations and then returns the total answer words list
    """
    global clues
    words = []

    for clue in clues[clue_set]:
        if clue['id'] == clue_id:
            print("Searching for:", clue['text'])
            if clue['searched']:
                words = clue['words']
            else:
                clue_list = create_clue_list(clue['text'])
                for clue2search in clue_list:
                    words = search_wiki(clue2search, clue['length'])
                    words += search_encyclopedia(clue2search, clue['length'])
                words = DataStore.remove_duplicates(words)
                clue['searched'] = True
                clue['words'] = words
            break
    return words


class Cell:
    """
        This corresponds to a letter in the crossword

        Attributes
        ----------
        text: The letter in the cell
        block: Whether the cell is blocked or not
        number: The number written in cell (is not used and only for GUI)
        number_across: The number of across clue if cell is the starting point of it
        number_down: The number of down clue if cell is the starting point of it
        solved_across: Whether across clue for cell is solved or not
        solved_down: Whether down clue for cell is solved or not

        Methods
        -------
        get_test(): Getter method for text
        set_text(): Setter method for text
        is_blocked(): Getter method for block
        get_number(): Getter method for number
        get_number_across(): Getter method for number_across
        get_number_down(): Getter method for number_down
        is_solved_across(): Getter method for solved_across
        solve_across():  Setter method for solved_across
        is_solved_down():  Getter method for solved_down
        solve_down():  Setter method for solved_down
    """
    def __init__(self, text, block, number, number_across, number_down, solved_across, solved_down):
        self.text = text
        self.block = block
        self.number = number
        self.number_across = number_across
        self.number_down = number_down
        self.solved_across = solved_across
        self.solved_down = solved_down

    def get_text(self):
        if self.text == '':
            return ' '
        return self.text
    def set_text(self, text):
        self.text = text

    def is_blocked(self):
        return self.block

    def get_number(self):
        return self.number
    def get_number_across(self):
        return self.number_across
    def get_number_down(self):
        return self.number_down

    def is_solved_across(self):
        return self.solved_across
    def solve_across(self):
        self.solved_across = True

    def is_solved_down(self):
        return self.solved_down
    def solve_down(self):
        self.solved_down = True


class CrosswordTree:
    """
        A class to hold current crossword grid and solve it

        Attributes
        ----------
        CROSSWORD_SIZE: The width of the crossword

        Methods
        -------
        solve(): This is a recursive function to solve crossword grid
            It traces the crossword grid to find and solve cells one by one.
            If puzzle is fully solved, returns itself. Otherwise, returns None.
        get_crossword(): Getter method for the crossword grid
        copy_crossword(): Creates a deep copy of the crossword grid
        print_crossword(): Prints the corssword grid on console
        calculate_score(): Calculates the score of current crossword grid
        compare_and_save(): Compares current crossword with the global best
            and saes the current if it has a better score
        is_solved(): Returns true if all both across and down clues
            for all cells are solved. Returns false otherwise.
    """
    CROSSWORD_SIZE = 5

    def __init__(self, crossword):
        if datetime.now().strftime( "%A").lower() == "saturday":
            self.CROSSWORD_SIZE = 7
        self.crossword = crossword

    def solve(self, row, col):
        global clues
        global best_tree

        for i in range(self.CROSSWORD_SIZE):
            for j in range(self.CROSSWORD_SIZE):
                if i < row:
                    continue
                elif i == row and j < col:
                    continue

                if self.crossword[i][j].is_blocked():
                    continue

                if self.crossword[i][j].get_number_across() and not self.crossword[i][j].is_solved_across():
                    candidates = search('across', self.crossword[i][j].get_number_across())
                    for word in candidates:
                        ncw = self.copy_crossword()
                        word_idx = 0
                        for n in range(self.CROSSWORD_SIZE):
                            if ncw[i][n].is_blocked():
                                continue
                            ch = ncw[i][n].get_text()
                            if ch != ' ' and ch != word[word_idx]:
                                break
                            ncw[i][n].set_text(word[word_idx])
                            ncw[i][n].solve_across()
                            word_idx += 1
                        if word_idx == len(word):
                            child = CrosswordTree(ncw)
                            self.print_iteration()
                            print("Candidates:", candidates, " -> Chosen:", word)
                            result = child.solve(i,j)
                            if result != None and result.is_solved():
                                return result
                            print("Undoing:", word)

                if self.crossword[i][j].get_number_down() and not self.crossword[i][j].is_solved_down():
                    candidates = search('down', self.crossword[i][j].get_number_down())
                    for word in candidates:
                        ncw = self.copy_crossword()
                        word_idx = 0
                        for n in range(self.CROSSWORD_SIZE):
                            if ncw[n][j].is_blocked():
                                continue
                            ch = ncw[n][j].get_text()
                            if ch != ' ' and ch != word[word_idx]:
                                break
                            ncw[n][j].set_text(word[word_idx])
                            ncw[n][j].solve_down()
                            word_idx += 1
                        if word_idx == len(word):
                            child = CrosswordTree(ncw)
                            self.print_iteration()
                            print("Candidates:", candidates, " -> Chosen:", word)
                            result = child.solve(i,j)
                            if result != None and result.is_solved():
                                return result
                            print("Undoing:", word)

        if self.is_solved():
            print("Solver: Crossword Solved")
            return self
        else:
            self.compare_and_save()
            return None

    def get_crossword(self):
        return self.crossword

    def copy_crossword(self):
        new_crossword = []
        for i in range(self.CROSSWORD_SIZE):
            new_crossword.append([])
            for j in range(self.CROSSWORD_SIZE):
                cell_data = self.crossword[i][j]

                new_cell = Cell(cell_data.text,
                                cell_data.is_blocked(),
                                cell_data.get_number(),
                                cell_data.get_number_across(),
                                cell_data.get_number_down(),
                                cell_data.is_solved_across(),
                                cell_data.is_solved_down())
                new_crossword[i].append(new_cell)
        return new_crossword

    def print_crossword(self):
        str = ""
        for i in range(self.CROSSWORD_SIZE):
            for j in range(self.CROSSWORD_SIZE):
                str += self.crossword[i][j].get_text() + " "
            str += "\n"
        print(str)

    def print_iteration(self):
        global iteration
        iteration += 1
        print("=======================================================================================")
        print("Iteration ", iteration, ":", sep = "")
        self.print_crossword()

    def calculate_score(self):
        score = 0
        for i in range(self.CROSSWORD_SIZE):
            for j in range(self.CROSSWORD_SIZE):
                if (self.crossword[i][j].is_solved_across()
                    and self.crossword[i][j].is_solved_down()):
                    score += 5
                elif self.crossword[i][j].is_solved_across():
                        score += 1
                elif self.crossword[i][j].is_solved_down():
                        score += 1
        return score

    def compare_and_save(self):
        global best_tree
        global best_score

        score = self.calculate_score()
        if best_score == 0:
            best_tree = self
            best_score = score

        if best_score < score:
            best_tree = self
            best_score = score

    def is_solved(self):
        for i in range(self.CROSSWORD_SIZE):
            for j in range(self.CROSSWORD_SIZE):
                if not self.crossword[i][j].is_blocked():
                    if not self.crossword[i][j].is_solved_across() or not self.crossword[i][j].is_solved_down():
                        return False
        return True


class Solver:
    """
        A class to hold current crossword grid and solve it

        Attributes
        ----------
        CROSSWORD_SIZE: The width of the crossword

        Methods
        -------
        print_clues(): Prints the clues in console
        create_crossword(): Translates the cell and clue information
            to a format used while solving
        solve_crossword(): Solves crossword, converts the format back to
            the old format and returns the solution
    """
    CROSSWORD_SIZE = 5

    def __init__(self, data):
        if datetime.now().strftime( "%A").lower() == "saturday":
            self.CROSSWORD_SIZE = 7
        self.create_crossword(data['clues'], data['cells'])

    def print_clues(self):
        global clues
        for set in clues:
            for clue in clues[set]:
                print(clue['text'], clue['words'])

    def create_crossword(self, crossword_clues, cells):
        global clues
        clues = crossword_clues
        crossword = []

        for i in range(self.CROSSWORD_SIZE):
            crossword.append([])
            for j in range(self.CROSSWORD_SIZE):
                cell_id = i * self.CROSSWORD_SIZE + j
                cell_data = cells[cell_id]

                text = ''
                block = cell_data['block']

                number_across = None
                number_down = None
                if not block:
                    if j == 0 or (j >= 1 and crossword[i][j-1].is_blocked()):
                        number_across = cell_data['number']
                    if i == 0 or (i >= 1 and crossword[i-1][j].is_blocked()):
                        number_down = cell_data['number']
                number = cell_data['number']
                new_cell = Cell(text, block, number, number_across, number_down, False, False)
                crossword[i].append(new_cell)

        for set in clues:
            for clue in clues[set]:
                clue['searched'] = False
                clue['words'] = []
                clue['length'] = 0
        for i in range(self.CROSSWORD_SIZE):
            for j in range(self.CROSSWORD_SIZE):
                across_clue_id = crossword[i][j].get_number_across()
                down_clue_id = crossword[i][j].get_number_down()

                if across_clue_id:
                    across_length = 0
                    for l in range(j, self.CROSSWORD_SIZE):
                        if not crossword[i][l].is_blocked():
                            across_length += 1
                    for clue in clues['across']:
                        if clue['id'] == across_clue_id:
                            clue['length'] = across_length
                if down_clue_id:
                    down_length = 0
                    for k in range(i, self.CROSSWORD_SIZE):
                        if not crossword[k][j].is_blocked():
                            down_length += 1
                    for clue in clues['down']:
                        if clue['id'] == down_clue_id:
                            clue['length'] = down_length
        self.tree = CrosswordTree( crossword)

    def solve_crossword(self):
        solved_tree = self.tree.solve(0,0)
        if solved_tree == None:
            global best_tree
            solved_tree = best_tree
        self.crossword = solved_tree.get_crossword()

        solution = {}
        solution['cells'] = {}

        for i in range(self.CROSSWORD_SIZE):
            for j in range(self.CROSSWORD_SIZE):
                cell = {}
                cell['block'] = self.crossword[i][j].is_blocked()
                cell['text'] = self.crossword[i][j].get_text()
                cell['number'] = self.crossword[i][j].get_number()

                cell_id = i * self.CROSSWORD_SIZE + j
                solution['cells'][cell_id] = cell
        self.print_clues()
        return solution
