
def removeSeen(children, OPEN, CLOSED):
    open_nodes = [node for node, parent in OPEN]
    closed_nodes = [node for node, parent in CLOSED]
    new_nodes = [c for c in children if c not in open_nodes and c not in closed_nodes]
    return new_nodes

def reconstructPath(node_pair, CLOSED):
    path = []
    parent_map = {}
    for node, parent in CLOSED:
        parent_map[node] = parent

    node, parent = node_pair
    path.append(node)
    while parent is not None:
        path.append(parent)
        parent = parent_map[parent]

    return path

def bfs(start):
    OPEN = [(start, None)]
    CLOSED = [] 
    while OPEN:
        node_pair = OPEN.pop(0)
        N, parent = node_pair
        if N.goalTest():
            print("Goal is found")
            path = reconstructPath(node_pair, CLOSED)
            path.reverse()
            for e in path:
                print("-> ", e)
            return 
        else:
            CLOSED.append(node_pair)
            children  = N.moveGen() 
            new_nodes  = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(c, N) for c in new_nodes]
            OPEN = OPEN + new_pairs
    return []            


class State:
    def __init__(self, left, right, umbrella, crossing_time, people):
        self.left = left
        self.right =  right
        self.umbrella=umbrella
        self.crossing_time=crossing_time
        self.people=people

    def goalTest(self):
        mover=list(self.right)
        if len(mover) == 4 and self.crossing_time<=60:
            return True
        else:
            return False
    
    def moveGen(self):
        children = []
        mover=list(self.left)
        
        if self.umbrella=='L':
            for i in range(len(mover)):
                for j in range(i,len(mover)):
                    move_pair={mover[i],mover[j]}
                    new_left = self.left - move_pair
                    new_right= self.right|move_pair
                    child_obj = State(new_left, new_right, 'R', self.crossing_time+max(self.people[p] for p in move_pair),self.people)
                    children.append(child_obj)
        else:
            for i in self.right:
                new_left=self.left | {i}
                new_right=self.right-{i}
                child_obj= State(new_left,new_right,'L', self.crossing_time+self.people[i],self.people)
                children.append(child_obj)
        return children
        

    def __str__(self):
        if self.umbrella == 'R':
           return f"Right->Left   Left: {self.left}, Right: {self.right}, Umbrella: {self.umbrella}, Time: {self.crossing_time}"
        else:
           return f"Left->Right   Left: {self.left}, Right: {self.right}, Umbrella: {self.umbrella}, Time: {self.crossing_time}"

    def __eq__(self, other):
        return (self.left == other.left and self.right == other.right and self.umbrella == other.umbrella and self.crossing_time == other.crossing_time)

    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right), self.umbrella, self.crossing_time))


start_state = State({'amogh','ameya','grandmother','grandfather'},set(),'L', 0, {'amogh':5,'ameya':10,'grandmother':20,'grandfather':25}) 
bfs(start_state)