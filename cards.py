class Card:

    def __init__(self, name, suit, rank, point, ID):
        self.name  = name
        self.suit  = suit
        self.rank = rank
        self.point = point
        self.ID = ID
        if suit[0] == 'S' or suit[0] == 'C':
            self.color = 'Black'
        else:
            self.color = 'Red'

    def __str__(self):
        return "(%s of %s)" % (self.name, self.suit)

    def get_name(self):
        return self.name

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def get_point(self):
        return self.point

    def get_ID(self):
        return self.ID
