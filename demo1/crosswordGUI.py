from datetime import datetime
from tkinter import *

class CrosswordGUI:
    CROSSWORD_SIZE = 5
    if datetime.now().strftime( "%A").lower() == "saturday":
        CROSSWORD_SIZE = 7
        print( "It's saturday!")

    def __init__( self, retData):
        self.data = retData

        # initialize Tkinter window
        self.window = Tk()

        # set window icon
        self.window.call( 'wm', 'iconphoto', self.window._w, PhotoImage( file = 'icon.png'))

        # set window title
        self.window.title( "The Mini Crossword")

        self.draw_title()
        self.draw_grid( self.data['cells'])
        self.draw_clues( self.data['clues'])

        print( "CrosswordGUI: Crossword puzzle created.")
        # open window
        self.window.resizable(False, False)
        self.window.mainloop()

        print( "CrosswordGUI: Program terminated.")


    def draw_title( self):
        title_frame = Frame( master = self.window)
        title_frame.pack( fill = X, padx = 10, pady = 10)
        # title
        title_label = Label( master = title_frame,
                            text = "The Mini Crossword",
                            font = "Times 40 bold",
                            padx = 10)
        title_label.grid( column = 0, row = 0, sticky = S)
        # date of the day
        date_label = Label( master = title_frame,
                            text = datetime.now().strftime('%A, %B %e, %Y'),
                            font ='Arial 26')
        date_label.grid( column = 1, row = 0, ipady = 3.5, sticky = S)


    def draw_grid( self, cells):
        def update_time():
            info_label.configure( text = datetime.now().strftime( "%d/%m/%Y %H:%M:%S")
                                    + ", ARTILLEGENCE")
            self.window.after( 1000, update_time)

        GRID_MARGIN = 10
        SQUARE_WIDTH = 100

        font_size_number = SQUARE_WIDTH // 5
        font_number = ( "Arial", font_size_number)
        font_size_letter = 2 * SQUARE_WIDTH // 3
        font_letter = ( "Arial", font_size_letter)

        # general frame of grid
        grid_frame = Frame( master = self.window)
        grid_frame.pack( fill = BOTH, side = LEFT, padx = 10, pady = 10)

        canvas = Canvas( master = grid_frame,
                        width = SQUARE_WIDTH * self.CROSSWORD_SIZE + 2 * GRID_MARGIN,
                        height = SQUARE_WIDTH * self.CROSSWORD_SIZE + 2 * GRID_MARGIN)
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
                                    font = font_letter, fill = '#232ed6')

                # write number if any
                x2 = x1 + (font_size_number // 2)
                y2 = y1 + (2 * font_size_number // 3)
                canvas.create_text( x2, y2,
                                    text = cell_data['number'],
                                    font = font_number)

        # date and time
        info_label = Label( master = grid_frame, text = "",
                            font = "Arial 12", anchor = E)
        info_label.pack( fill = BOTH, side = BOTTOM, padx = 10)
        update_time()


    def draw_clues( self, clues):
        font_title = "Arial 16 bold"
        font_clue = "Arial 14"

        # general frame of clues
        clue_frame = Frame( master = self.window)
        clue_frame.pack( fill = Y, side = TOP, padx = 10, pady = 10)

        # frame of across clues
        across_frame = Frame( master = clue_frame)
        across_frame.grid( column = 0, row = 0, ipadx = 10, sticky = NW)

        # across clues title
        across_label = Label( master = across_frame,
                            text = "ACROSS",
                            font = font_title,
                            anchor = W)
        across_label.pack( fill = X, padx = 10, pady = 10)
        # across clues
        for clue in clues['across']:
            text = clue['id'] + ". " + clue['text']
            across_label = Label( master = across_frame,
                                text = text,
                                font = font_clue,
                                anchor = W,
                                justify = LEFT,
                                wraplength = 300)
            across_label.pack( fill = X, pady = 5)

        # frame of down clues
        down_frame = Frame( clue_frame)
        down_frame.grid( column = 1, row = 0, ipadx = 10, sticky = NW)

        # down clue title
        down_label = Label( master = down_frame,
                            text = "DOWN",
                            font = font_title,
                            anchor = W)
        down_label.pack( fill = X, padx = 10, pady = 10)
        # down clues
        for clue in clues['down']:
            text = clue['id'] + ". " + clue['text']
            down_label = Label( master = down_frame,
                                text = text,
                                font = font_clue,
                                anchor = W,
                                justify = LEFT,
                                wraplength = 300)
            down_label.pack( fill = X, pady = 5)
