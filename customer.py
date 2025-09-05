import blind

class Customer:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.blindCount = 0
        self.blinds = []
    
    def addBlind(self, location, blind_type, fabric, width, height, control, controlMat, controlPos, bracket, quantity, price):
        self.blindCount += 1
        self.blinds.append(blind.Blind(location, blind_type, fabric, self.blindCount, width, height, control, controlMat, controlPos, bracket, quantity, price))
        
