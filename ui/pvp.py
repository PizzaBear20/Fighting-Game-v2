from ui.comingsoon import ComingSoonScreen


# PvP mode: two players fight each other in real time. Replace this class with the real screen
class PvPScreen(ComingSoonScreen):
    def __init__(self, parent, onBack):
        super().__init__(parent, "PvP", "Two players, one keyboard. Pick your fighters and battle in real time.", onBack)
