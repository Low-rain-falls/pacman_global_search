class Performance:
    def __init__(self):
        self.searchTime = 0
        self.expandedNodes = 0
        self.memory = 0
    
    # update info
    def update(self, aspect, data):
        if aspect == "searchTime":
            self.searchTime = data
        elif aspect == "expandedNodes":
            self.expandedNodes = data
        elif aspect == "memory":
            self.memory = data
    
    # print curent
    def printPer(self):
        print(f"Searching time: {self.searchTime}ms, memory used: {self.memory}, expanded nodes: {self.expandedNodes}")