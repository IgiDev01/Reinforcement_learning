import random

class Environment:
    def __init__(self,x,y) -> None:
        self.states = []
        self.gamma = 0.9
        self.alpha = 0.1
        self.x = x
        self.y = y
        pass
    
    def reset(self):
        for i in range(self.y):
            #row = []
            for j in range(self.x):
                self.states.append(0)
            #self.states.append(row)
        #self.states[random.randint(0,self.y-1)][random.randint(0,self.x-1)]=1
        self.states[self.x-1]=1
        

    def step(self, action, state, q_table):   #next_state, reward, done
        if self.states[state+action]==1:
            return state+action,1,1 
        return state+action,0,0
        




class Agent:
    def __init__(self) -> None:
        self.state = 0
        self.q_table = []
        self.done = 0
        pass

    def q_table_generate(self, a, b):
        for i in range(b):
            row = []
            for j in range(a):
                row.append(0.0)
            self.q_table.append(row)

    def q_table_display(self):
        for row in self.q_table:
            print(row)
    

    def get_best_action(self):
        if self.q_table[self.state-1][0] > self.q_table[self.state+1][1]:
            return -1
        else:
            return 1

    def get_action(self):
        actions=[-1,1]
        if self.state == 0:
            return actions[1]
        if self.q_table[self.state-1][0] == self.q_table[self.state+1][1] :
            return actions[random.randint(0,1)]
        else:
            return self.get_best_action()
    
    def update(self, action, next_state, reward, done):   #aktualizacja q_table
        gamma = 0.9
        alpha = 0.1
        if action < 0:
            index = 0
        else:
            index = 1
        self.q_table[self.state][index]+=alpha*(reward+gamma*self.q_table[next_state][index]-self.q_table[self.state][index])
        self.state+=action
        if(reward==1) :
            self.done=1
    
environment = Environment(5,1)
environment.reset()
print(environment.states)
agent = Agent()
agent.q_table_generate(2,5)



sesions = 300

for i in range(sesions):
    while agent.done!=1:
        action = agent.get_action()
        next_state, reward, done = environment.step(action,agent.state, agent.q_table)
        agent.update(action, next_state, reward, done)
    agent.state=0
    agent.done=0

agent.q_table_display()