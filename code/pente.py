# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Names:        Jeffrey Costello
#               Timothy Magno
#               Daniel Zhang
# Section:      470
# Assignment:   Lab 13
# Date:         12 3 2023


import turtle
from PIL import Image, ImageDraw
import math

turn = 'w' #whos turn it is
stamp_data = {} #stores the stamp data. This includes the stamp id, 
white_counter = {} #This has the location for the on-board caputred pieces display. It uses the <color>_capture varaible as an index.
black_counter = {}

print("Steps:\n1.Click the run command ")
print("2.White gets the first move and is prompted to place a stone on the screen. This is\naccomplished by clicking where on the board you want to place your piece. This is an\nexample of clicking a piece, where the red circle represents where you clicked.")
print("3.In order to stop the program, click the “x” in the top right corner.")
print("4.In order to end the program after winning, click on “OK” like the program prompts you to.")
for x in range(1, 11): #This part of the code creates specific coordinates for black or white pieces in dictionary form in order to be used later.
    if x % 2 == 0:
        black_counter[x] = {'x' : 200, 'y' : 150-(50*(x/2))}
        white_counter[x] = {'x' : -200, 'y' : 150-(50*(x/2))}
    else:
        black_counter[x] = {'x' : 250, 'y' : 150-50*math.ceil(x/2)}
        white_counter[x] = {'x' : -250, 'y' : 150-50*math.ceil(x/2)}
black_capture = 0 #This is the number of white pieces captured
white_capture = 0
capture_coordinates_white = [] #pieces that white captures
capture_coordinates_black = [] #pieces that black captures

def create_gif_from_png(png_path, gif_path):
    """
    Turtle canT only paste gifs, so it converts a png to a gif using the library pillow.
    """
    # Open the PNG image with Pillow
    png_image = Image.open(png_path).convert("RGBA")

    # Create a new image with a transparent background
    gif_image = Image.new("RGBA", png_image.size, (0, 0, 0, 0))

    # Paste the PNG image onto the new image
    gif_image.paste(png_image, (0, 0), png_image)

    # Save the result as a GIF file
    gif_image.save(gif_path, "GIF")


def draw_png_image(turtle_obj, gif_path):
    """
    Pastes the gif
    """

    # Register the GIF image as a shape
    turtle.Screen().register_shape(gif_path)

    # Create a turtle with the registered shape
    turtle_obj.shape(gif_path)
    turtle_obj.penup()
    turtle_obj.goto(0, 0)  # Set the starting position


def place_piece(color = 'b', x = 0, y = 0):
    """
    Takes in the turn color and desired coordinates to place the piece. 
    Saves the pieces coordinate and bounds it to a unique stamp id.
    """
    turtle.setpos(x ,y)
    if color == 'b':
        turtle.fillcolor("black")
    else:
        turtle.fillcolor("white")
    stamp_id = turtle.stamp()
    stamp_data[(x, y)] = stamp_id
    print(stamp_data)

def remove_piece(color = 'b', x = 0, y = 0, ):
    """
    """
    print('went through remove piece')
    global stamp_data
    global white_capture
    global black_capture
    if (x, y) in stamp_data:
        stamp_id = stamp_data[(x, y)]
        print('Stamp Data:')
        print(stamp_data)
        print('Stamp Id')
        print(stamp_id)
        print(f'stamp_id {stamp_id} cleared')
        turtle.clearstamp(stamp_id)
        del stamp_data[(x, y)]
        print('Stamp Data:')
        print(stamp_data)
    if color == 'b':
        black_capture += 1
    else:
        white_capture += 1

    print("Number of captured black pieces:")
    print(black_capture)
    print("Number of captured white pieces:")
    print(white_capture)

def update_capture(color):
    global black_capture
    global white_capture
    turtle.shapesize(2)
    if color == 'b':
        print(black_capture)
        turtle.setpos(black_counter[black_capture]['x'], black_counter[black_capture]['y'])
        turtle.fillcolor('white')
        turtle.stamp()
    else:
        turtle.setpos(white_counter[white_capture]['x'], white_counter[white_capture]['y'])
        turtle.fillcolor('black')
        turtle.stamp()
    turtle.shapesize(0.6)

def get_mouse_location(x, y):
    """
    Function specific to turtle
    """
    return x, y

def is_click_in_button(click_x, click_y, button_x, button_y, button_width, button_height):
    """
    Checks if your click is within a button.
    """
    return (
        button_x - button_width / 2 < click_x < button_x + button_width / 2 and
        button_y - button_height / 2 < click_y < button_y + button_height / 2
    )

def show_warning_popup():
    """
    Shows a popup. This function is used if you try to place a piece on an occupied space.
    """
    turtle.hideturtle()
    user_input = turtle.textinput("Invalid move", "There is already a piece here.\nClick OK to continue.")
    turtle.showturtle()

    if user_input is not None:
        print("Clicked OK")
def show_win_screen(color):
    """
    Shows a popup. This function is used if you try to place a piece on an occupied space.
    """
    turtle.hideturtle()
    if color == 'b':
        user_input = turtle.textinput("BLACK WINS!", "BLACK WINS!.\nClick OK to close.")
        turtle.bye()
    else:
        user_input = turtle.textinput("WHITE WINS!", "WHITE WINS!.\nClick OK to close.")
        turtle.bye()

def pretty_board(board):
    """
    Responsible for the game matrix debug output.
    """
    for rows in game_board:
        print((' ').join(rows))

def check_horizontal(board):
    """
    Checks all the horizontals on the board. 
    Returns 'b' or 'w' depending on who one. 
    If a win isn't detected it will pass.
    """
    for rows in board:
        w_counter = 0
        b_counter = 0
        for space in rows:
            if space == 'b':
                b_counter += 1
                w_counter = 0
            elif space == 'w':
                w_counter += 1
                b_counter = 0
            else:
                b_counter = 0
                w_counter = 0
            if b_counter == 5:
                return 'b'
            elif w_counter == 5:
                return 'w'

def check_vertical(board):
    """
    Checks all the verticals on the board. 
    Returns 'b' or 'w' depending on who one. 
    If a win isn't detected it will pass.
    """
    for column in range(19):
        b_counter = 0
        w_counter = 0
        for rows in board:
            if rows[column] == 'b':
                b_counter += 1
                w_counter = 0
            elif rows[column] == 'w':
                w_counter += 1
                b_counter = 0
            else:
                b_counter = 0
                w_counter = 0
            if b_counter == 5:
                return 'b'
            if w_counter == 5:
                return 'w'

def check_diagonals(board):
    """
    Checks all the diagonals on the board. 
    Returns 'b' or 'w' depending on who one. 
    If a win isn't detected it will pass.
    """
    #left to right diagonal
    for diagonals in range(4, 19):
        b_counter = 0
        w_counter = 0
        index_x = diagonals
        index_y = 0
        for x in range(diagonals+1):
            if board[index_y][index_x] == 'b':
                b_counter += 1
                w_counter = 0
            elif board[index_y][index_x] == 'w':
                w_counter += 1
                b_counter = 0
            else:
                w_counter = 0
                b_counter = 0
            if b_counter == 5:
                return 'b'
            if w_counter == 5:
                return 'w'
            index_x -= 1
            index_y += 1
    for diagonals in range(1, 15):
        index_y = diagonals
        index_x = 18
        for x in range(19-index_y):
            if board[index_y][index_x] == 'b':
                b_counter += 1
                w_counter = 0
            elif board[index_y][index_x] == 'w':
                w_counter += 1
                b_counter = 0
            else:
                w_counter = 0
                b_counter = 0
            if b_counter == 5:
                return 'b'
            if w_counter == 5:
                return 'w'
            index_y += 1
            index_x -= 1
    #right to left
    for diagonal in range(4, 19):
        index_x = 0
        index_y = 18-diagonal
        for x in range(diagonal+1):
            if board[index_y][index_x] == 'b':
                b_counter += 1
                w_counter = 0
            elif board[index_y][index_x] == 'w':
                w_counter += 1
                b_counter = 0
            else:
                w_counter = 0
                b_counter = 0
            if b_counter == 5:
                return 'b'
            if w_counter == 5:
                return 'w'
            index_y += 1
            index_x += 1
    for diagonal in range(1, 19):
        index_x = diagonal
        index_y = 0
        for x in range(19-index_x):
            if board[index_y][index_x] == 'b':
                b_counter += 1
                w_counter = 0
            elif board[index_y][index_x] == 'w':
                w_counter += 1
                b_counter = 0
            else:
                w_counter = 0
                b_counter = 0
            if b_counter == 5:
                return 'b'
            if w_counter == 5:
                return 'w'
            index_y += 1
            index_x += 1
def update_turn(color):
    pass

def check_win(board):
    """
    Checks whether black or white won using the check_<direction>() funcitons.
    Prints black, or white won
    """
    if ((check_diagonals(board) or check_horizontal(board) or check_vertical(board)) == 'b') or black_capture == 10:
        print('black won')
        show_win_screen('b')
    elif ((check_diagonals(board) or check_horizontal(board) or check_vertical(board)) == 'w') or white_capture == 10:
        print('white won')
        show_win_screen('w')
    else:
        print('no one won')

def remover(color, list):
    global game_board
    # print(x_coord)
    # print(y_coord)
    for elements in list:
        remove_piece(color, x_coord[elements[0]], y_coord[elements[1]])
        game_board[elements[1]][elements[0]] = 'n'
        update_capture(color)
    




def capture_horzontal(board):
    """
    Checks for captures on the horizontals and updates the list 'capture_coordinates_<color>' with coordinates of those exact pieces.
    """
    for y in range(19):
        for x in range(16):
            if board[y][x] == 'b' and board[y][x + 1] == 'w' and board[y][x + 2] == 'w' and board[y][x + 3] == 'b':
                capture_coordinates_black.append([x + 1, y])
                capture_coordinates_black.append([x + 2, y])
            if board[y][x] == 'w' and board[y][x + 1] == 'b' and board[y][x + 2] == 'b' and board[y][x + 3] == 'w':
                capture_coordinates_white.append([x + 1, y])
                capture_coordinates_white.append([x + 2, y])

def capture_vertical(board):
    """
    Checks for captures on the verticals and updates the list 'capture_coordinates_<color>' with coordinates of those exact pieces.
    """
    for y in range(16):
        for x in range(19):
            if board[y][x] == 'b' and board[y + 1][x] == 'w' and board[y + 2][x] == 'w' and board[y + 3][x] == 'b':
                capture_coordinates_black.append([x, y + 1])
                capture_coordinates_black.append([x, y + 2])
            if board[y][x] == 'w' and board[y + 2][x] == 'b' and board[y + 2][x] == 'b' and board[y + 3][x] == 'w':
                capture_coordinates_white.append([x, y + 1])
                capture_coordinates_white.append([x, y + 2])
                
def capture_diagonal(board):
    """
    Checks for captures on the diagonals and updates the list 'capture_coordinates_<color>' with coordinates of those exact pieces.
    """
    for y in range(16):
        for x in range(16):
            # Check for black capture of white
            if (board[y][x] == 'b' and board[y + 1][x + 1] == 'w' and 
                board[y + 2][x + 2] == 'w' and board[y + 3][x + 3] == 'b'):
                capture_coordinates_black.extend([[x + 1, y + 1], [x + 2, y + 2]])
            # Check for white capture of black
            if (board[y][x] == 'w' and board[y + 1][x + 1] == 'b' and 
                board[y + 2][x + 2] == 'b' and board[y + 3][x + 3] == 'w'):
                capture_coordinates_white.extend([[x + 1, y + 1], [x + 2, y + 2]])

    for y in range(16):
        for x in range(3, 19):
            # Check for black capture of white
            if (board[y][x] == 'b' and board[y + 1][x - 1] == 'w' and 
                board[y + 2][x - 2] == 'w' and board[y + 3][x - 3] == 'b'):
                capture_coordinates_black.extend([[x - 1, y + 1], [x - 2, y + 2]])
            # Check for white capture of black
            if (board[y][x] == 'w' and board[y + 1][x - 1] == 'b' and 
                board[y + 2][x - 2] == 'b' and board[y + 3][x - 3] == 'w'):
                capture_coordinates_white.extend([[x - 1, y + 1], [x - 2, y + 2]])


def process_capture(board): #checks for capturable pieces and handles all aspects of capture
    """
    Processes captures and consolodates all capture functions to one function
    """
    global stamp_id
    capture_horzontal(board)
    capture_diagonal(board)
    capture_vertical(board)
    print(capture_coordinates_black)
    print(capture_coordinates_white)
    remover(color = 'b', list = capture_coordinates_black)
    capture_coordinates_black.clear()
    remover(color = 'w', list = capture_coordinates_white)
    capture_coordinates_white.clear()


def on_button_click(x, y):
    """
    This is essentially the game loop and perfoms checks and updates for every time a new piece is placed.
    """
    global turn
    for button_id, button_info in buttons.items():
        if is_click_in_button(x, y, button_info["x"], button_info["y"], button_width, button_height):
            if game_board[y_index[button_id]][x_index[button_id]] != 'n': #checks for piece existing in location
                print("there is already a piece here")
                show_warning_popup()
            else:
                if turn == 'b':
                    game_board[y_index[button_id]][x_index[button_id]] = 'b'
                    place_piece(turn, x=button_info['x'], y=button_info['y'])
                    turn = 'w'
                else:
                    game_board[y_index[button_id]][x_index[button_id]] = 'w'
                    place_piece(turn, x=button_info['x'], y=button_info['y'])
                    turn = 'b'
                ########################################
                #debug info for every turn
                pretty_board(game_board)
                print(f"Button {button_id} Clicked at ({button_info['x']}, {button_info['y']})")
                print(f' index {x_index[button_id]},{y_index[button_id]} should have been updated')
            process_capture(game_board)
            check_win(game_board)

def main():
    ####################################################
    #Variables:
    #Globals are used to make them valid within the main() funciton
    global buttons 
    global button_height
    global button_width
    global button_id
    global game_board 
    global x_index #button : x coord
    global y_index #button : y coord
    global x_coord #index : x coord
    global y_coord #index : y coord
    x=0
    game_board = [['n' for x in range(19)] for _ in range(19)]
    x_index = {} #button : x coord
    y_index = {} #button : y coord
    x_coord = {}  #index : x coord
    y_coord = {}  #index : y coord
    ####################################################
    #turtle initialization
    turtle.hideturtle()
    turtle.penup()
    ####################################################
    #Places buttons
    button_width, button_height = 15, 15
    button_spacing = 15 
    turtle.tracer(0) #gets rid of animations for the turtle
    screen = turtle.Screen()
    buttons = {}
    button_id = 1
    for i in range(19): #This for loop creartes 361 with saved coordiantes and button id's into a dictionarie.
        for j in range(19):
            button_x = (-135 + j * button_spacing) #x coordinate of the buttons
            button_y = (135 - i * button_spacing) #y coordiante of the buttons
            screen.register_shape(f"button{button_id}", ((-button_width / 2, -button_height / 2), (-button_width / 2, button_height / 2), (button_width / 2, button_height / 2), (button_width / 2, -button_height / 2)))
            turtle_button = turtle.Turtle()
            turtle_button.pencolor("") #removes pen color
            turtle_button.shape(f"button{button_id}") 
            turtle_button.fillcolor("") #sets fil color to clear
            turtle_button.penup() 
            turtle_button.goto(button_x, button_y)
            buttons[button_id] = {"x": button_x, "y": button_y, "turtle": turtle_button} #ids all the buttons placed into a dictionary
            y_index[button_id] = i #ties the button id to the to a y index
            x_index[button_id] = j #ties the button id to the to a x index
            x_coord[j] = buttons[button_id]['x'] #ties the index to the the button coordinate
            if j == 18:
                 y_coord[i] = buttons[button_id]['y']
            button_id += 1 
    screen.onclick(on_button_click)
    # print('y_cood')
    # print(y_coord)
    # print('x_coord')
    # print(x_coord)
    ####################################################
    #places the board
    png_path = "sprites/2.png"
    gif_path = "output_image.gif"
    try:
        create_gif_from_png(png_path, gif_path)
        my_turtle = turtle.Turtle()
        turtle.penup()
        turtle.speed(10)
        draw_png_image(my_turtle, gif_path)
    except FileNotFoundError:
        print('File \'2.png\' not found')
        turtle.hideturtle()
        user_input = turtle.textinput("FILE NOT FOUND!", "2. png is missing from the correct directiory.\nClick OK to close.")
        turtle.showturtle()
        turtle.bye()
        
    ####################################################
    #Draws Titles for sides.
    turtle.setpos(240,150)
    turtle.write("Black's Pieces", align="center", font=("Arial", 12, "normal"))
    turtle.setpos(-240,150)
    turtle.write("White's Pieces", align="center", font=("Arial", 12, "normal"))
    turtle.setpos(0, -200)
    turtle.write("Rules:", align="center", font=("Arial", 15, "normal"))
    turtle.setpos(0, -240)
    text = "Five Pieces in a row or 10 captures win the game.\nThe pattern bwwb or wbbw will capture the pieces in the middle.\nWhite goes first."
    turtle.write(text, align="center", font=("Arial", 8, "normal"))




    ####################################################
    #Makes capture spots
    turtle.bgcolor("#8b5e34") #hex code colors sourced from coolors.com
    turtle.shape("circle")
    turtle.shapesize(2)
    turtle.color('#603808')
    turtle.fillcolor('#603808')
    for x in range(1, 6):  #this loop creates the indented circles on either side to act as piece holders
        turtle.setpos(200, 150-50*x)
        turtle.stamp()
        turtle.setpos(250, 150-50*x)
        turtle.stamp()
        turtle.setpos(-200, 150-50*x)
        turtle.stamp()
        turtle.setpos(-250, 150-50*x)
        turtle.stamp()
    turtle.shapesize(1.5)
    turtle.color('#583101')
    turtle.fillcolor('#583101')
    for x in range(1, 6):
        turtle.setpos(200, 150-50*x)
        turtle.stamp()
        turtle.setpos(250, 150-50*x)
        turtle.stamp()
        turtle.setpos(-200, 150-50*x)
        turtle.stamp()
        turtle.setpos(-250, 150-50*x)
        turtle.stamp()
    ####################################################
    #sets stamp shape:
    turtle.shapesize(0.6)
    ####################################################
    #Random test stuff  
    turtle.update()
    turtle.mainloop()


if __name__ == "__main__":
    main()