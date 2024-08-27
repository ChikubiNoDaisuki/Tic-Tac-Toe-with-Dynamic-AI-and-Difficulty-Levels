from tkinter import *

def check_winner():
    for i in range(3):
        if buttons[i][0]['text'] == buttons[i][1]['text'] == buttons[i][2]['text'] != "":
            return buttons[i][0]['text']
        if buttons[0][i]['text'] == buttons[1][i]['text'] == buttons[2][i]['text'] != "":
            return buttons[0][i]['text']

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return buttons[0][0]['text']
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return buttons[0][2]['text']

    if all(buttons[i][j]['text'] != "" for i in range(3) for j in range(3)):
        return "Tie"

    return None

def evaluate(board):
    winner = check_winner()
    if winner == ai_player:
        return 10
    elif winner == human_player:
        return -10
    else:
        return 0

def minimax_easy(board, depth, is_maximizing):
    winner = check_winner()
    if winner == "X":
        return 1
    elif winner == "O":
        return -1
    elif winner == "Tie":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j]['text'] == "":
                    board[i][j]['text'] = ai_player
                    score = minimax_easy(board, depth + 1, False)
                    board[i][j]['text'] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j]['text'] == "":
                    board[i][j]['text'] = human_player
                    score = minimax_easy(board, depth + 1, True)
                    board[i][j]['text'] = ""
                    best_score = min(score, best_score)
        return best_score

def minimax_difficult(board, depth, is_maximizing, alpha, beta):
    score = evaluate(board)
    
    if score != 0 or check_winner() == "Tie":
        return score - depth if is_maximizing else score + depth
    
    if is_maximizing:
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j]['text'] == "":
                    board[i][j]['text'] = ai_player
                    eval = minimax_difficult(board, depth + 1, False, alpha, beta)
                    board[i][j]['text'] = ""
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j]['text'] == "":
                    board[i][j]['text'] = human_player
                    eval = minimax_difficult(board, depth + 1, True, alpha, beta)
                    board[i][j]['text'] = ""
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if buttons[i][j]['text'] == "":
                buttons[i][j]['text'] = ai_player
                if difficulty == "Easy":
                    score = minimax_easy(buttons, 0, False)
                else:
                    score = minimax_difficult(buttons, 0, False, -float('inf'), float('inf'))
                buttons[i][j]['text'] = ""
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def next_turn(row, column):
    global player

    if buttons[row][column]['text'] == "" and check_winner() is None:
        buttons[row][column]['text'] = player
        buttons[row][column].config(bg="#282828", fg="white")

        if player == human_player:
            if check_winner() is None:
                player = ai_player
                label.config(text="AI's turn", fg="#0FF0FC")
                root.update()  # Updates the UI to reflect the AI's turn
                ai_move = best_move()
                if ai_move:
                    next_turn(ai_move[0], ai_move[1])  # AI takes its move
            elif check_winner() == "Tie":
                label.config(text="It's a Tie!", fg="#0FF0FC")
            else:
                label.config(text=f"Player {human_player} wins!", fg="#0FF0FC")
        
        elif player == ai_player:  # AI's turn
            if check_winner() is None:
                player = human_player
                label.config(text=f"Player {human_player}'s turn", fg="#0FF0FC")
            elif check_winner() == "Tie":
                label.config(text="It's a Tie!", fg="#0FF0FC")
            else:
                label.config(text="AI wins!", fg="#0FF0FC")

def reset():
    global player
    player = human_player  # Set the player who goes first
    label.config(text=f"Player {human_player}'s turn", bg="#101010", fg="#0FF0FC")

    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", bg="#101010", fg="#0FF0FC")

def select_player(choice):
    global human_player, ai_player, player
    human_player = choice
    ai_player = "O" if choice == "X" else "X"
    player = human_player  # Player goes first
    label.config(text=f"Player {human_player}'s turn")
    start_game()

def select_difficulty(choice):
    global difficulty
    difficulty = choice
    start_frame.pack_forget()
    player_frame.pack()

def start_game():
    player_frame.pack_forget()  # Hide the player selection screen
    game_frame.pack()  # Show the game board

# Main program setup
root = Tk()
root.title("Tic Tac Toe")
root.configure(bg="#101010")

# Player choice variables
human_player = None
ai_player = None
player = None
difficulty = None

# UI frames
start_frame = Frame(root, bg="#101010")
start_frame.pack()

Label(start_frame, text="Choose Difficulty:", font=('Arial', 24), bg="#101010", fg="#0FF0FC").pack(pady=20)
Button(start_frame, text="Easy", font=('Arial', 18), bg="#0FF0FC", fg="#101010", command=lambda: select_difficulty("Easy")).pack(side=LEFT, padx=20)
Button(start_frame, text="Hard", font=('Arial', 18), bg="#0FF0FC", fg="#101010", command=lambda: select_difficulty("Difficult")).pack(side=RIGHT, padx=20)

player_frame = Frame(root, bg="#101010")

Label(player_frame, text="Choose your Player:", font=('Arial', 24), bg="#101010", fg="#0FF0FC").pack(pady=20)
Button(player_frame, text="Play as X", font=('Arial', 18), bg="#0FF0FC", fg="#101010", command=lambda: select_player("X")).pack(side=LEFT, padx=20)
Button(player_frame, text="Play as O", font=('Arial', 18), bg="#0FF0FC", fg="#101010", command=lambda: select_player("O")).pack(side=RIGHT, padx=20)

game_frame = Frame(root, bg="#101010")

# Game setup
label = Label(game_frame, text="", font=('Arial', 24, 'bold'), bg="#101010", fg="#0FF0FC")
label.pack(side="top", pady=20)

reset_button = Button(game_frame, text="Restart", font=('Arial', 14, 'bold'), command=reset, bg="#0FF0FC", fg="#101010", relief="flat")
reset_button.pack(side="top", pady=10)

buttons = [[None, None, None], [None, None, None], [None, None, None]]
frame = Frame(game_frame, bg="#101010")
frame.pack()

for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(frame, text="", font=('Arial', 40), width=5, height=2,
                               bg="#101010", fg="#0FF0FC", activebackground="#282828",
                               command=lambda row=i, column=j: next_turn(row, column))
        buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

root.mainloop()
