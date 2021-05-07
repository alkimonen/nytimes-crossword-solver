from datetime import datetime
from tkinter import *

class CrosswordGUI:
    CROSSWORD_SIZE = 5
    if datetime.now().strftime( "%A").lower() == "saturday":
        CROSSWORD_SIZE = 7
        print( "It's saturday!")

    def __init__( self, retData, solvedData):
        # initialize Tkinter window
        self.window = Tk()
        # set window title and background
        self.window.title( "The Mini Crossword")
        self.window.configure( bg = 'white')
        # set window icon
        self.window.call( 'wm', 'iconphoto', self.window._w, PhotoImage( file = 'icon.png'))

        self.draw_grid( retData['cells'], False)
        self.draw_clues( retData['clues'])
        self.draw_grid( solvedData['cells'], True)
        print( "CrosswordGUI: Crossword puzzle created.")

        # open window
        self.window.resizable(False, False)
        self.window.mainloop()

        print( "CrosswordGUI: Program terminated.")


    def draw_grid( self, cells, bum):
        def update_time():
            info_label.configure( text = datetime.now().strftime( "%d/%m/%Y %H:%M:%S")
                                    + " ARTILLIGENCE")
            self.window.after( 1000, update_time)

        GRID_MARGIN = 10
        SQUARE_WIDTH = 80

        font_size_number = SQUARE_WIDTH // 5
        font_number = ( "Arial", font_size_number)
        font_size_letter = 2 * SQUARE_WIDTH // 3
        font_letter = ( "Arial", font_size_letter)
        if bum:
            font_color = 'black'
        else:
            font_color = '#232ed6'

        # general frame of grid
        grid_frame = Frame( master = self.window, bg = 'white')
        grid_frame.pack( fill = BOTH, side = LEFT, padx = 10, pady = 10)

        canvas = Canvas( master = grid_frame,
                        width = SQUARE_WIDTH * self.CROSSWORD_SIZE + 2 * GRID_MARGIN,
                        height = SQUARE_WIDTH * self.CROSSWORD_SIZE + 2 * GRID_MARGIN,
                        highlightthickness = 0,
                        bg = 'white')
        canvas.pack( fill = BOTH, side = TOP)

        for i in range( self.CROSSWORD_SIZE):
            for j in range( self.CROSSWORD_SIZE):
                cell_id = i * self.CROSSWORD_SIZE + j
                cell_data = cells[cell_id]

                # draw rectangle
                x1 = GRID_MARGIN + j * SQUARE_WIDTH
                y1 = GRID_MARGIN + i * SQUARE_WIDTH
                x2 = x1 + SQUARE_WIDTH
                y2 = y1 + SQUARE_WIDTH

                if cell_data['block']:
                    background = "black"
                else:
                    background = "white"
                canvas.create_rectangle( x1, y1, x2, y2, fill = background,
                                        outline = "gray")

                # write letter if any
                x2 = x1 + (SQUARE_WIDTH // 2)
                y2 = y1 + (3 * SQUARE_WIDTH // 5)
                canvas.create_text( x2, y2,
                                    text = cell_data['text'].upper(),
                                    font = font_letter, fill = font_color)

                # write number if any
                x2 = x1 + (font_size_number // 2)
                y2 = y1 + (2 * font_size_number // 3)
                canvas.create_text( x2, y2,
                                    text = cell_data['number'],
                                    font = font_number)

        # date and time
        if bum:
            info_label = Label( master = grid_frame, text = "",
                                font = "Arial 16", anchor = E, bg = 'white')
            info_label.pack( fill = BOTH, side = BOTTOM, padx = 10)
            update_time()


    def draw_clues( self, clues):
        font_title = "Arial 16 bold"
        font_clue = "Arial 14"

        # general frame of clues
        clue_frame = Frame( master = self.window, bg = 'white')
        clue_frame.pack( fill = Y, side = LEFT, padx = 10, pady = 10)

        # frame of across clues
        across_frame = Frame( master = clue_frame, bg = 'white')
        across_frame.grid( column = 0, row = 0, ipadx = 10, sticky = NW)

        # across clues title
        across_label = Label( master = across_frame,
                            text = "ACROSS",
                            font = font_title,
                            anchor = W,
                            bg = 'white')
        across_label.pack( fill = X, padx = 10, pady = 10)

        across_clues = Text( master = across_frame,
                            font = font_clue,
                            wrap = 'word',
                            width = 25,
                            height = 17,
                            relief = FLAT,
                            highlightthickness = 0)
        across_clues.tag_configure( 'bulleted', lmargin1 = 0, lmargin2 = 20)

        # across clues
        for clue in clues['across']:
            text = clue['id'] + ". " + clue['text']
            across_clues.insert( 'end', text + "\n\n", 'bulleted')
            across_clues.pack( fill = X, pady = 5)
        across_clues.configure( state = DISABLED)

        # frame of down clues
        down_frame = Frame( master = clue_frame, bg = 'white')
        down_frame.grid( column = 1, row = 0, ipadx = 10, sticky = NW)

        # down clue title
        down_label = Label( master = down_frame,
                            text = "DOWN",
                            font = font_title,
                            anchor = W,
                            bg = 'white')
        down_label.pack( fill = X, padx = 10, pady = 10)

        down_clues = Text( master = down_frame,
                            font = font_clue,
                            wrap = 'word',
                            width = 25,
                            height = 17,
                            relief = FLAT,
                            highlightthickness = 0)
        down_clues.tag_configure( 'bulleted', lmargin1 = 0, lmargin2 = 20)

        # down clues
        for clue in clues['down']:
            text = clue['id'] + ". " + clue['text']
            down_clues.insert( 'end', text + "\n\n", 'bulleted')
            down_clues.pack( fill = X, pady = 5)
        down_clues.configure( state = DISABLED)
