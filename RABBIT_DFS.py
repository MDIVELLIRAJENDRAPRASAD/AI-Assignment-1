
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
                print(e.node)
            return 
        else:
            CLOSED.append(node_pair)
            children  = N.moveGen() 
            new_nodes  = removeSeen(children, OPEN, CLOSED)
            new_pairs = [(c, N) for c in new_nodes]
            OPEN = new_pairs + OPEN 
    return []            


class State:
    def __init__(self, node):
        self.node = node

    def goalTest(self):
        n=len(self.node)
        for i in range(len(self.node)):
            if(i<=n/2 and self.node[i]=='>'):
               return False
            elif(i>(n/2)+1 and self.node[i]=='<'):
               return False
        return True

    
    def moveGen(self):
        children = []
        for i in range(len(self.node)):
            if(i+2<len(self.node) and self.node[i]=='>' and self.node[i+2]=='_'):
              new_word = self.node[ :i] + '_' + self.node[i+1] + '>'+self.node[i+3: ]
              child_obj = State(new_word)
              children.append(child_obj)
            if i+1<len(self.node) and self.node[i]=='>' and self.node[i+1]=='_':
              new_word=self.node[ :i]+'_' + '>'+self.node[i+2: ]
              child_obj = State(new_word)
              children.append(child_obj)
            if  i-2>=0 and self.node[i]=='<' and self.node[i-2]=='_':
              new_word = self.node[ :i-2]+'<'+self.node[i-1]+'_'+self.node[i+1: ]
              child_obj = State(new_word)
              children.append(child_obj)
            if i-1>=0 and  self.node[i]=='<' and self.node[i-1]=='_':
               new_word = self.node[ :i-1]+'<'+'_'+self.node[i+1: ]
               child_obj = State(new_word)
               children.append(child_obj)

        return children  
    def __str__(self):
        return self.node
    def __eq__(self, other):
       return isinstance(other, State) and self.node == other.node

    def __hash__(self):
       return hash(self.node)

              

start = State(">>>_<<<") 
bfs(start) 
