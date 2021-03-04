import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class CrosswordDataRetriever:
    def retrieve_crossword(self):
        self.create_driver()
        self.reveal_solutions()
        data = {'clues': self.retrieve_clues(), 'cells': self.retrieve_cells()}
        time.sleep(2)
        self.close_driver()
        return data

    def retrieve_clues( self):
        clues = {}
        # clues are listed in section named "Layout-clueLists--10_Xl"
        clue_lists = self.driver.find_element_by_class_name( 'Layout-clueLists--10_Xl')
        # across and down clues are divided into divs
        divs = clue_lists.find_elements_by_tag_name( 'div')
        for div in divs:
            # title: text of h3 (across or down)
            title = div.find_element_by_tag_name( 'h3').text.lower()
            clues[title] = []
            # Clues are divided into divs
            list_items = div.find_elements_by_tag_name( 'li')
            for list_item in list_items:
                # Clues' numbers and texts are divided into spans
                # Text of span[0]: Clue number, text of span[1]: Clue text
                spans = list_item.find_elements_by_tag_name( 'span')
                # { 'id', 'text'}
                clues[title].append( {'id': spans[0].text, 'text': spans[1].text})
        print( "CrosswordDataRetriever: Clues retrieved.")
        return clues

    def retrieve_cells( self):
        cells = {}
        # cell information is stored in g with data-group = "cells"
        cell_table = self.driver.find_element_by_css_selector( 'g[data-group=cells]')
        # cells are divided into g's
        gs = cell_table.find_elements_by_tag_name( 'g')
        cell_id = 0;
        for g in gs:
            data = { 'block': False, 'text': '', 'number': ''}
            # each cell g contains a rect
            rect = g.find_element_by_tag_name( 'rect')
            # id="cell-idX" where x is 0-24
            #cell_id = rect.get_attribute('id').split('-')[2]
            # class can contain "Cell-block..." if black or "Cell-cell" if empty
            if 'Cell-block' in rect.get_attribute( 'class'):
                data[ 'block'] = True
            # text in rect contains number and letter in each cell
            text_fields = g.find_elements_by_tag_name( 'text')
            for text_field in text_fields:
                # if text-anchor="start" then this is number of starting clue
                if text_field.get_attribute( 'text-anchor') == 'start':
                    data['number'] = text_field.text
                # if text-anchor="start" then this is letter in the cell
                if text_field.get_attribute( 'text-anchor') == 'middle':
                    data['text'] = text_field.text
            cells[cell_id] = data
            cell_id += 1
        print( "CrosswordDataRetriever: Cells retrieved.")
        return cells

    def create_driver( self):
        self.driver = webdriver.Chrome()
        self.driver.get( "https://www.nytimes.com/crosswords/game/mini")
        print( "CrosswordDataRetriever: Connected to \"https://www.nytimes.com/crosswords/game/mini\".")

    def close_driver( self):
        self.driver.quit()
        print( "CrosswordDataRetriever: Connection terminated.")

    def reveal_solutions( self):
        self.click_continue()
        self.click_ok()
        self.click_reveal_menu_button()
        self.click_puzzle_reveal_button()
        self.click_reveal_confirmation_button()
        self.close_pop_up()
        print( "CrosswordDataRetriever: Solutions revealed.")

    def click_continue( self):
        try:
            continue_button = self.driver.find_element_by_css_selector( 'button[class="StartModal-underlined--3IDBr"]')
            continue_button.click()
        except NoSuchElementException:
            pass

    def click_ok( self):
        try:
            ok_button = self.driver.find_element_by_css_selector( 'button[class="buttons-modalButton--1REsR buttons-startBtn--3OK72"]')
            ok_button.click()
        except NoSuchElementException:
            pass

    def click_reveal_menu_button( self):
        reveal_button = self.driver.find_element_by_css_selector( 'button[aria-label="reveal"]')
        reveal_button.click()

    def click_puzzle_reveal_button( self):
        puzzle_reveal_button = self.driver.find_element_by_link_text( 'Puzzle')
        puzzle_reveal_button.click()

    def click_reveal_confirmation_button( self):
        reveal_button = self.driver.find_element_by_css_selector( 'button[class="buttons-modalButton--1REsR"]')
        reveal_button.click()

    def close_pop_up( self):
        span = self.driver.find_element_by_css_selector( 'span[class="ModalBody-closeX--2Fmp7"]')
        span.click()
