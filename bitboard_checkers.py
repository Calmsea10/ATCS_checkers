import pygame
import math
import time

def initialize_white_board(white_board):
    for i in range(20,33):
        white_board=white_board|(1<<i)
    return white_board

def initialize_red_board(red_board):
    for i in range(0,12):
        red_board=red_board|(1<<i)
    return red_board

def board_repr(board):
    for i in range(0,8):
        for j in range(0,4):
            print((board>>((4*i)+j))&1,end=' ')
        print('')

def display_board(board1,board2,screen):
    for i in range(0,8):
        for j in range(0,8):
            if i%2==0:
                if j%2==0:
                    pygame.draw.rect(screen,"black",(j*64,i*64,64,64))
            if i%2!=0:
                if j%2!=0:
                    pygame.draw.rect(screen,"black",(j*64,i*64,64,64))
        for k in range(0,4):
            if (board1>>(4*i)+k)&1:
                if (i%2)==0:
                    pygame.draw.circle(screen,"burlywood4",((k)*128+96,i*64+32),32)
                else:
                    pygame.draw.circle(screen,"burlywood4",((k)*128+32,i*64+32),32)
            if (board2>>(4*i)+k)&1:
                if (i%2)==0:
                    pygame.draw.circle(screen,"darkred",((k)*128+96,i*64+32),32)
                else:
                    pygame.draw.circle(screen,"darkred",((k)*128+32,i*64+32),32)
    return 0

def display_moves(board_white,board_red,pos,team,screen):
    if not pos==32:
        if (pos//4)%2==0:
            pygame.draw.circle(screen,"yellow",(((pos%4)*128)+96,((pos//4)*64)+32),32,4)
        else:
            pygame.draw.circle(screen,"yellow",(((pos%4)*128)+32,((pos//4)*64)+32),32,4)
    if team:
        board1=board_white
        board2=board_red
    else:
        board1=board_red
        board2=board_white
    all_captures=capture_positions(board1,board2,team)
    if len(all_captures)>0:
        if pos not in all_captures:
            return 0
    capture_list=get_shallow_captures(board1,board2,team,pos)
    move_list=get_moves(board1,board2,team,pos)
    if len(capture_list)>0:
        for i in range(0,8):
            for k in range(0,4):
                for j in range(0,len(capture_list)):
                    if capture_list[j][0]==((4*i)+k):
                        if (i%2)==0:
                            pygame.draw.circle(screen,"yellow",((k)*128+96,i*64+32),32)
                        else:
                            pygame.draw.circle(screen,"yellow",((k)*128+32,i*64+32),32)
    else:
        for i in range(0,8):
            for k in range(0,4):
                if ((4*i)+k) in move_list:
                    if (i%2)==0:
                        pygame.draw.circle(screen,"yellow",((k)*128+96,i*64+32),32)
                    else:
                        pygame.draw.circle(screen,"yellow",((k)*128+32,i*64+32),32)
    return 0

def evaluate_board(board1,board2,team):
    value=0
    if team:
        board_white=board1
        board_red=board2
    else:
        board_white=board2
        board_red=board1
    for i in range(0,32):
        if (board_white>>i)&1:
            value+=1
        if (board_red>>i)&1:
            value-=1
    return value

def get_moves(board1,board2,team,pos):
    if not (board1>>pos)&1:
        return []
    else:
        moves=[]
        if team:
            move1=(pos-(3+((pos//4)%2)))
            move2=(pos-(4+((pos//4)%2)))
            if move1>=0:
                if (pos//4)-(move1//4)==1:
                    if (not (board1>>move1)&1) and (not (board2>>move1)&1):
                        moves.append(move1)
            if move2>=0:
                if (pos//4)-(move2//4)==1:
                    if (not (board1>>move2)&1) and (not (board2>>move2)&1):
                        moves.append(move2)
        else:
            move1=(pos+(3+(((pos//4)+1)%2)))
            move2=(pos+(4+(((pos//4)+1)%2)))
            if move1<=31:
                if (pos//4)-(move1//4)==-1:
                    if (not (board1>>move1)&1) and (not (board2>>move1)&1):
                        moves.append(move1)
            if move2<=31:
                if (pos//4)-(move2//4)==-1:
                    if (not (board1>>move2)&1) and (not (board2>>move2)&1):
                        moves.append(move2)
        return moves

def can_capture(board1,board2,team,pos):
    capture_dirs=[]
    if team:
        capture1=(pos-7)
        move1=(pos-(3+((pos//4)%2)))
        capture2=(pos-9)
        move2=(pos-(4+((pos//4)%2)))
        if capture1>=0:
            if (pos//4)-(capture1//4)==2:
                if (not ((board1>>capture1)&1)) and (not ((board2>>capture1)&1)):
                    if (board2>>move1)&1:
                        capture_dirs.append(1)
        if capture2>=0:
            if (pos//4)-(capture2//4)==2:
                if (not ((board1>>capture2)&1)) and (not ((board2>>capture2)&1)):
                    if (board2>>move2)&1:
                        capture_dirs.append(2)
    else:
        capture1=(pos+7)
        move1=(pos+(3+(((pos//4)+1)%2)))
        capture2=(pos+9)
        move2=(pos+(4+(((pos//4)+1)%2)))
        if capture1<=31:
            if (capture1//4)-(pos//4)==2:
                if (not ((board1>>capture1)&1)) and (not ((board2>>capture1)&1)):
                    if (board2>>move1)&1:
                        capture_dirs.append(3)
        if capture2<=31:
            if (capture2//4)-(pos//4)==2:
                if (not ((board1>>capture2)&1)) and (not ((board2>>capture2)&1)):
                    if (board2>>move2)&1:
                        capture_dirs.append(4)
    if len(capture_dirs)==0:
        return [0]
    else:
        return capture_dirs

def get_shallow_captures(board1,board2,team,pos):
    return_moves=[]
    if not (board1>>pos)&1:
        return return_moves
    capture_dirs=can_capture(board1,board2,team,pos)
    if 1 in capture_dirs:
        return_moves.append([pos-7,(pos-(3+((pos//4)%2)))])
    if 2 in capture_dirs:
        return_moves.append([pos-9,(pos-(4+((pos//4)%2)))])
    if 3 in capture_dirs:
        return_moves.append([pos+7,(pos+(3+(((pos//4)+1)%2)))])
    if 4 in capture_dirs:
        return_moves.append([pos+9,(pos+(4+(((pos//4)+1)%2)))])
    return return_moves

def get_possible_captures(board1,board2,team,capture_list):
    return_moves=[]
    holder=[]
    pos=capture_list[0]
    capture_dirs=can_capture(board1,board2,team,pos)
    if 1 in capture_dirs:
        holder=capture_list[:]
        holder[0]=capture_list[0]-7
        holder.append(pos-(3+((pos//4)%2)))
        return_moves.extend(get_possible_captures(board1,board2,team,holder))
    if 2 in capture_dirs:
        holder=capture_list[:]
        holder[0]=capture_list[0]-9
        holder.append(pos-(4+((pos//4)%2)))
        return_moves.extend(get_possible_captures(board1,board2,team,holder))
    if 3 in capture_dirs:
        holder=capture_list[:]
        holder[0]=capture_list[0]+7
        holder.append(pos+(3+((pos//4)%2)))
        return_moves.extend(get_possible_captures(board1,board2,team,holder))
    if 4 in capture_dirs:
        holder=capture_list[:]
        holder[0]=capture_list[0]+9
        holder.append(pos+(4+((pos//4)%2)))
        return_moves.extend(get_possible_captures(board1,board2,team,holder))
    if 0 in capture_dirs:
        capture_list.append(-1)
        return capture_list
    return return_moves

def get_captures(board1,board2,team,pos):
    capture_list=get_possible_captures(board1,board2,team,[pos])
    all_captures=[]
    current_capture=[]
    for i in range(0,len(capture_list)):
        if capture_list[i]==-1:
            if len(current_capture)>1:
                all_captures.append(current_capture)
            current_capture=[]
        else:
            current_capture.append(capture_list[i])
    return all_captures

def capture_positions(board1,board2,team):
    capture_positions=[]
    for i in range(0,32):
        if len(get_shallow_captures(board1,board2,team,i))>0:
            capture_positions.append(i)
    return capture_positions

def move(board1,board2,team,start_pos,end_pos):
    if team:
        if board1>>(start_pos)&1:
            if end_pos in get_moves(board1,board2,team,start_pos):
                board1=board1|(1<<end_pos)
                board1=board1^(1<<start_pos)
                return board1
    else:
        if board1>>(start_pos)&1:
            if end_pos in get_moves(board1,board2,team,start_pos):
                board1=board1|(1<<end_pos)
                board1=board1^(1<<start_pos)
                return board1

def capture(board1,board2,start_pos,capture_list):
    for i in range(1,len(capture_list)):
        board2=board2^(1<<capture_list[i])
    board1=board1|(1<<capture_list[0])
    board1=board1^(1<<start_pos)
    return (board1,board2)

def get_all_moves(board1,board2,team):
    capture_boards=[]
    move_boards=[]
    for i in range(0,32):
        capture_list=get_captures(board1,board2,team,i)
        moves_list=get_moves(board1,board2,team,i)
        for j in range(0,len(capture_list)):
            capture_boards.append(capture(board1,board2,i,capture_list[j]))
        for k in range(0,len(moves_list)):
            move_boards.append((move(board1,board2,team,i,moves_list[k]),board2))
    if len(capture_boards)>0:
        return capture_boards
    else:
        return move_boards

def minimax(board1,board2,team,depth):
    evals=[]
    if board1==0:
        return [-1*math.inf]
    elif board2==0:
        return [math.inf]
    elif depth==0:
        return [evaluate_board(board1,board2,team)]
    else:
        boards=get_all_moves(board1,board2,team)
        for i in range(0,len(boards)):
            if team:
                evals.append(min(minimax(boards[i][1],boards[i][0],not team,depth-1)))
            else:
                evals.append(max(minimax(boards[i][1],boards[i][0],not team,depth-1)))
    return evals

def main():
    running=True
    board_white=0
    board_red=0
    pos=0
    team=True
    piece_selected=False
    selected_piece=32
    capture_forced=False
    pygame.display.init()
    clock=pygame.time.Clock()
    screen=pygame.display.set_mode((512,512))
    board_white=initialize_white_board(board_white)
    board_red=initialize_red_board(board_red)
    board_repr(board_red+board_white)
    while running==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type ==pygame.MOUSEBUTTONDOWN:
                pos=(pygame.mouse.get_pos()[0]//128)+((pygame.mouse.get_pos()[1]//64)*4)
                if piece_selected:
                    if team==True:
                        board1=board_white
                        board2=board_red
                    else:
                        board1=board_red
                        board2=board_white
                    capture_pos=capture_positions(board1,board2,team)
                    print(capture_pos)
                    if len(capture_pos)>0:
                        if selected_piece in capture_pos:
                            captures=get_shallow_captures(board1,board2,team,selected_piece)
                            for i in range(0,len(captures)):
                                if captures[i][0]==pos:
                                    boards=capture(board1,board2,selected_piece,captures[i])
                                    board1=boards[0]
                                    board2=boards[1]
                                    break
                    elif pos in get_moves(board1,board2,team,selected_piece):
                        board1=move(board1,board2,team,selected_piece,pos)
                        selected_piece=pos
                    else:
                        piece_selected=False
                        selected_piece=32
                        pos=32
                    if team==True:
                        board_white=board1
                        board_red=board2
                    else:
                        board_white=board2
                        board_red=board1
                else:
                    if (board_white>>pos)&1:
                        team=True
                        piece_selected=True
                        selected_piece=pos
                    if (board_red>>pos)&1:
                        team=False
                        piece_selected=True
                        selected_piece=pos
                    print(selected_piece)
                    print(team)
                print(minimax(board_red,board_white,False,3))
        screen.fill("gray")
        display_board(board_white,board_red,screen)
        display_moves(board_white,board_red,pos,team,screen)
        pygame.display.flip()
        clock.tick(60)
    

if __name__ == "__main__":
    main()