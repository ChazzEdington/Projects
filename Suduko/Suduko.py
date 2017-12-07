#game was made to be easily scalable and (hopefully) userproof
#First project completed

#initial setup ---------------------------------------------------
import turtle
import random
                     
turtle.hideturtle()
turtle.pu()
turtle.speed(0)
screen = turtle.getscreen()
screen.tracer(0)


#------------------------Choose-Game-------------------------------

def choose_game():

    game1 = [[1,'',4,3],['',4,'',2],[2,1,'',''],['','',2,1]]
    game2 = [[4,2,3,1],['','','',''],['','','',''],[3,4,1,2]]
    game3 = [['',1,3,''],[4,'','',2],[1,'','',3],['',2,4,'']]
    game4 = [['',2,1,''],[1,'','',4],[3,'',4,''],['',4,'',1]]
    game5 = [['','',4,''],['','','',2],['',4,2,1],[1,'',3,'']]

    #for more fun, program scales to 9x9. Return hard_diff in choose_game() and
    #set size = 9 in the user interface!
    hard_diff = [[8,'','','',5,4,2,'',3],[5,'','',8,9,2,'',4,1],[4,'',2,6,'','','',5,9],
                 ['',6,7,'','',5,'',1,8],[1,'',8,'',3,'',5,'',7],[9,5,'',7,'',1,'',2,''],
                 ['',8,'',2,4,9,6,'',''],['','',3,5,'',8,'','',''],[2,9,5,'','',7,1,8,'']]
    
    game_list =[game1, game2, game3, game4, game5]
    rand = random.randint(0,4)
    selected_game = game_list[rand]                 #randomly choose game

    return hard_diff


#------------------------Erasable-Turtles--------------------------

def make_erasables(size, clear):                    #list of turtles that can be cleared

    if clear == 'No':                            
        global erasable_turtles
        erasable_turtles = [[turtle.Turtle() for i in range(size)] for j in range(size)]

        for i in range(size):
            for j in range(size):
                erasable_turtles[i][j].hideturtle()
                erasable_turtles[i][j].color('red')
                erasable_turtles[i][j].pu()
    
    if clear == 'Yes':                              #clears board

        for i in range(size):
            for j in range(size):
                erasable_turtles[i][j].clear()
    

#------------------------Check-Game--------------------------------

def check_game(user_game, size):

    correct = True
    status = 'Complete'
    

    for row_const in range(size):                   #Check remainding game

        for col_const in range(size):

            if user_game[row_const][col_const] == '': #If blank skip
                status = 'Incomplete'
                continue

            for col in range(size):                 #Check rows first
                if col == col_const:                #avoid checking against self
                    continue
                
                if user_game[row_const][col_const] == user_game[row_const][col]:
                    correct = False
                
            for row in range(size):                 #Check Columns next
                if row == row_const:                #avoid checking against self
                    continue
            
                if user_game[row_const][col_const] == user_game[row][col_const]:
                    correct = False

            
    bold = [[] for i in range(size)]            #map game so it is organized by
                                                #bold boxes and easier to check
                                                #Do last since inefficient    
    shift_r = 0
    shift_c = 0

    for boxes in range(size):

        if boxes%(size**.5) == 0 and boxes !=0:
            shift_c = 0
            shift_r +=1
        
        for row in range(int(shift_r*size**.5), int((shift_r+1)*size**.5)):
            
            for col in range(int(shift_c*size**.5), int((shift_c+1)*size**.5)):

                bold[boxes].append(user_game[row][col])
                

        shift_c +=1


    for i in range(size):                           #Check bolded boxes and incompletes

        for j in range(size -1):

            if bold[i][j] == '':               #do not check against cells if empty
                status = 'Incomplete'               #notes game is incomplete
                continue
            
            for k in range(j+1, size):
            
                if bold[i][k] == '':            
                    status = 'Incomplete'
                    
                
                elif bold[i][j] == bold[i][k]:
                    correct = False
        
                
                 
    return (correct, status)

#------------------------Draw-Square-------------------------------

def draw_square(n):

    turtle.pd()

    for side in range(4):

        turtle.forward(n)
        turtle.left(90)
       
    turtle.pu()

        


#------------------------Add-Numbers-------------------------------
def add_info(column, row, x, y):                #x,y only used in initial set up and not after

    if 'game' not in globals():                 #if game not yet chosen, choose game
        global game
        game = choose_game()

    if column == 'done':                        #if won, give congrats
        turtle.setpos(x,y)
        turtle.write('Congrats! You won.', font = ('Arial', 42, 'bold'))
        
    elif x == -1:
        
        side = chr(65+y)                        #keeps game scale-able
        turtle.write(side, font = ('Arial', 36))
        
        return
    
    elif y == -.7:
        
        bottom = 1 + x
        turtle.write(bottom, font = ('Arial', 36))
        

    elif 'game_copy' not in globals():          #initial board set up, once permanent nums
                                                #set game_copy will exist &skip this step 
        turtle.setpos(column, row)
        turtle.write(game[row][column], font = ('Arial', 28))
        turtle.setpos(x, y)

    else:                                       #user inputed info

        erasable_turtles[row][column].clear()   #clears whatever was previously there
        erasable_turtles[row][column].setpos(column, row)
        erasable_turtles[row][column].write(game[row][column], font = ('Arial', 28))

    



#------------------------Create-Gameboard--------------------------

def game_board(size):
                                                #Give extra room on edges for visual appeal
    turtle.setworldcoordinates(-3,-1, size, size+2)   
    turtle.hideturtle()
    
    for i in range(2):                          #first make normal squares, second bold lines

        x = -.5                                 #offset so numbers will be center in grid
        y = 0
        turtle.setpos(x,y)

        ld= 1                                   #distance of square lines
        
        if i == 1:                              #Checks second round, bolds if true
            size = int(size**.5)
            ld = size
            turtle.width(3)
           
        
        for row in range(size):

            for column in range(size):

                draw_square(ld)

                if i == 0:                      #Only add nums if first time through
                    add_info(column, row, x, y)

                x += ld
                turtle.setpos(x, y)

            x = -.5
            y += ld

            turtle.setpos(x,y)

        x = -1                                  #Final two loops for adding position info
        y -= 1
        
        for side in range(size):                #Letters marking side
            
            turtle.setpos(x,y)
            add_info(x,y, x,y)
            y -= 1

        x = 0
        y = -.7
        
        for bottom in range(size):              #Numbers marking bottom

            turtle.setpos(x,y)
            add_info(x,y, x,y)
            x += 1

            
#------------------------Alter-Game-Info--------------------------
                
                #Change user entered info to info known by written code
                #Check that info adheres to game rules
                #Add info to gameboard
            
def alter_info(cord, ans, check, size):
          
    if len(cord) != 2:                          #make sure correct length
        return 'Improper cordinates.\n'

    cord_list = [ char for char in cord]
    first = cord_list[0].upper()                #ensure uppercase so next line works
    row = ord(first)                            #Used to check if within game board
    col = ord(cord_list[1])                     #and account for random entries

    if check == 'cordinates':                   #Check cordinates are correct
                                                #Check if in bounds of game
        if row not in range(65, 65+size) or col not in range(49, 49+size):
            return 'Improper cordinates.\n'
        
        row = row - 65                          #change to fit game cordinates
        col = int(col) - 49
        
        if game_copy[row][col] != '':           #check that user isn't changing game info
            return 'No cheating. Improper cordinates.\n'

        return ''
    row = row - 65                              #change to fit game cordinates
    col = int(col) -49
           
                                                #check if answer allowed
    if ans != '' and len(ans) == len(str(size)) and ord(ans) in range(49, 49+size):                       
        ans = int(ans)
        
    elif ans != '':
        return "Answer must be integer between 1 and {} or left empty to erase\n".format(int(size))
        
                                                #if this far, no erros in input
    if check == 'Y':
        info_holder = game[row][col]
        game[row][col] = ans
            
        if check_game(game, size)[0] == False:
            game[row][col] = info_holder        #return game to previous info
            return 'Incorrect answer\n'

    game[row][col] = ans                        #do if check passes and correct,
                                                #or if not autochecking
    add_info(col,row, col,row)                  #x,y of add_info don't matter for this step
                                                #so just send col row in place
    return ''
    

            
#------------------------User-Interface----------------------------


def user_interface():
    
    size = 9                                  #variable sized used so game isn't limited to 4x4
    game_board(size)
    
    screen.update()
    
    make_erasables(size, 'No')                  #erasable turtles corresponding to each
                                                #spot in game grid
    
    global game_copy                            #used to prevent user from altering set game
    game_copy = [[game[i][j] for j in range(size)] for i in range(size)]
                                            
                #Check for constant check-------------------------------

    const_check = 'First'
    while True:
            
        if const_check in ['Y','y', 'N', 'n']:
            const_check= const_check.upper()    #for ease of calling later
            break;
        
        elif const_check == 'First':
            const_check = turtle.textinput('', 'Real time correction? (Y/N): ')
        
        else:
            const_check = turtle.textinput('', 'Please enter Y or N. \nReal time correction? (Y/N): ')
    
            
    info = ''                                   #place to add comments throughout play
    playing = True
    
                #Enter game play ---------------------------------------
    
    while playing == True:          

        
        pos = turtle.textinput('', '{}\nPosition (EX:A1): '.format(info))

        info = alter_info(pos, '0', 'cordinates', size) 
        if info != '':                          #Repeats pos line until proper cordinates given
            continue

        ans = turtle.textinput('', 'Enter answer or press enter to erase: ')
            
        info = alter_info(pos, ans, const_check, size)
        
        screen.update()

        if info == '':
            
            if check_game(game, size)[1] == 'Complete':
                
                submit = 'Enter loop'
                while submit not in ['Y','y','N','n']:
                    submit = turtle.textinput('', 'Submit game (Y/N): ')

                    if submit in ['Y', 'y']:
                        if check_game(game, size)[0] == True:
                            add_info('done','done', 0, size+1)
                            playing = False                 #exit game

                        else:                               #actions if game isn't correct
                            while True:
                                erase = turtle.textinput('', 'Game is not corret.\nStart from scratch? (Y/N):')

                                if erase in ['Y', 'y']:     #resets board   
                                    make_erasables(size, 'Yes')
                                    break;
                                
                                elif erase in ['N', 'n']:
                                    break;
                                
        screen.update()                  

user_interface() 

screen.update()
