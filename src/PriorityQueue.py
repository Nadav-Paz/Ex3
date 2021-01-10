from DiGraph import DiGraph

class PriorityQueue(object):
    def __init__(self):
        self.queue = []


    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

        # for checking if the queue is empty

    def isEmpty(self):
        return len(self.queue) == 0
    def __sizeof__(self):
        return len(self.queue)

    # for inserting an element in the queue
    def insert(self, data: DiGraph.Node):
        self.queue.append(data)
        self.sort()
        # for popping an element based on Priority
    def sort(self):
        for i in range (0,len(self.queue)):
            for j in range(0,len(self.queue)):
                if (self.queue[i]<self.queue[j]):
                        self.sweep(i,j)


    def sweep(self,i : int,j: int):
        n = self.queue[i]
        self.queue[i]=self.queue[j]
        self.queue[j] = n

    def decrease(self):
        newqueue=[]
        for i in range(1,len(self.queue)):
            newqueue.append(self.queue[i])
        self.queue=newqueue

    def delete(self):
        try:
            self.sort()
            item = self.queue[0]
            self.decrease()
            return item
        except IndexError:
            print()
            exit()
