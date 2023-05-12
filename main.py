import random
import time 
class Environment:
    def __init__(self,x,y) -> None:
        self.states = []
        self.x = x
        self.y = y
        pass
    
    def reset(self):
        column = []
        for i in range(self.y):
            row = []
            for j in range(self.x):
                row.append(0)
            column.append(row)
        self.states = column
        self.states[random.randint(0,self.y-1)][random.randint(0,self.x-1)]=1
        

    def step(self, action, state):   #next_state, reward, done
        new_state = []
        if state[0]+action[0] < 0 or state[0]+action[0] > self.x-1 or state[1]+action[1] < 0 or state[1]+action[1] > self.y-1:
            new_state.append(state[0]+action[0])
            new_state.append(state[1]+action[1])
            return new_state,-1,1 
        if self.states[state[1]+action[1]][state[0]+action[0]]==1:
            new_state.append(state[0]+action[0])
            new_state.append(state[1]+action[1])
            return new_state,1,1
        else:
            
            new_state.append(state[0]+action[0])
            new_state.append(state[1]+action[1])
            return new_state,0,0
        




class Agent:
    def __init__(self, x, y) -> None:
        self.state = []
        self.q_table = {}
        self.done = 0
        self.apple = []
        pass
    
    def set_apple(self, x,y):
        self.apple = [x,y]
    def set_agent(self, x, y):
        self.state = self.apple
        while self.state[0] == self.apple[0] and self.state[1] == self.apple[1]: 
            self.state = [random.randint(0,x-1), random.randint(0,y-1)]

    def start_q_table(self):
        key = ((self.state[0], self.state[1]),(self.apple[0], self.apple[1]))
        self.q_table[key]=[0,0,0,0]

    def q_table_display(self):
        for key, values in self.q_table:
            print(key, values)


    def get_action(self):
        action = [[1,0],[-1,0],[0,1],[0,-1]]
        values = []
        for row in action:
            key = ((self.state[0]+row[0], self.state[1]+row[1]),(self.apple[0], self.apple[1]))
            if key not in self.q_table:
                self.q_table[key]=[0.0,0.0,0.0,0.0]
            values.append(max(self.q_table[key]))
        
        if (x == values[0] for x in values):
            return action[random.randint(0,3)]
        else:
            return action[values.index(max(values))]
    
    def update(self, action, next_state, reward, done):   #aktualizacja q_table
        gamma = 0.9
        alpha = 0.1
        index = 0
        actions = [[1,0],[-1,0],[0,1],[0,-1]]
        for i, x in enumerate(actions):
            if x == action:
                index = i
        key1 = ((self.state[0], self.state[1]),(self.apple[0], self.apple[1]))
        key2 = ((self.state[0]+action[0], self.state[1]+action[1]),(self.apple[0], self.apple[1]))
        self.q_table[key1][index]+= alpha * (reward+gamma*max(self.q_table[key2])-self.q_table[key1][index])


        self.state=next_state
        if(done==1) :
            self.done=1

board_size_x = 3
board_size_y = 3

apple_x = 0
apple_y = 0
environment = Environment(board_size_x,board_size_y)
agent = Agent(board_size_x, board_size_y)

def generate_board(board_size_y, board_size_x):
    board = []
    for i in range(board_size_y+2):
        row=[]
        for j in range(board_size_x+2):
            if i == 0 or i == board_size_y+1:
                row.append("+")
                continue
            if j == 0 or j == board_size_x+1:
                row.append("+")
                continue
            row.append(" ")
        board.append(row)
    return board

def board_update(board):
    for i in range(board_size_y+2):
        for j in range(board_size_x+2):
            if board[i][j]=='*':
                board[i][j]=' '

def display_board(board):
    print("_________")
    for row in board:
        for x in row:
            print(x, end='')
        print()




epizodes = 500000
n = 0
for i in range(epizodes):
    environment.reset()
    for i in range(len(environment.states)):
        for j in range(len(environment.states[i])):
            if environment.states[i][j]==1:
                apple_x=j
                apple_y=i
    agent.set_apple(apple_x,apple_y)
    agent.set_agent(board_size_x, board_size_y)
    board = generate_board(board_size_y,board_size_x)
    board[apple_y+1][apple_x+1]="x"
    board[agent.state[1]+1][agent.state[0]+1]="*"
    #display_board(board)
    agent.start_q_table()
    while(agent.done!=1):
        board_update(board)
        action = agent.get_action()
        next_state, reward, done = environment.step(action, agent.state)
        agent.update(action, next_state, reward, done)
        board[agent.state[1]+1][agent.state[0]+1]="*"
        if n >epizodes-10:
            time.sleep(0.2)
            display_board(board)
            print(n)    
        
    agent.done=0
    n+=1
for key, values in dict(sorted(agent.q_table.items())).items():
    print(key, values)


