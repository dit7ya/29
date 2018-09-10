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


deck = [Card('Ace', 'Spades', 3, 1, 1),
        Card('King', 'Spades', 5, 0, 2),
        Card('Queen', 'Spades', 6, 0, 3),
        Card('Jack', 'Spades', 1, 3, 4),
        Card('10', 'Spades', 4, 1, 5),
        Card('9', 'Spades', 2, 2, 6),
        Card('8', 'Spades', 8, 0, 7),
        Card('7', 'Spades', 7, 0, 8),

        Card('Ace', 'Clubs', 3, 1, 9),
        Card('King', 'Clubs', 5, 0, 10),
        Card('Queen', 'Clubs', 6, 0, 11),
        Card('Jack', 'Clubs', 1, 3, 12),
        Card('10', 'Clubs', 4, 1, 13),
        Card('9', 'Clubs', 2, 2, 14),
        Card('8', 'Clubs', 8, 0, 15),
        Card('7', 'Clubs', 7, 0, 16),

        Card('Ace', 'Hearts', 3, 1, 17),
        Card('King', 'Hearts', 5, 0, 18),
        Card('Queen', 'Hearts', 6, 0, 19),
        Card('Jack', 'Hearts', 1, 3, 20),
        Card('10', 'Hearts', 4, 1, 21),
        Card('9', 'Hearts', 2, 2, 22),
        Card('8', 'Hearts', 8, 0, 23),
        Card('7', 'Hearts', 7, 0, 24),

        Card('Ace', 'Diamonds', 3, 1, 25),
        Card('King', 'Diamonds', 5, 0, 26),
        Card('Queen', 'Diamonds', 6, 0, 27),
        Card('Jack', 'Diamonds', 1, 3, 28),
        Card('10', 'Diamonds', 4, 1, 29),
        Card('9', 'Diamonds', 2, 2, 30),
        Card('8', 'Diamonds', 8, 0, 31),
        Card('7', 'Diamonds', 8, 0, 32)
        ]