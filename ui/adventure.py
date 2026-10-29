from ui.comingsoon import ComingSoonScreen


# Adventure mode: explore a map, level up and create new moves. Replace this class with the real screen
class AdventureScreen(ComingSoonScreen):
    def __init__(self, parent, onBack):
        super().__init__(parent, "Adventure", "Explore the map, level up your fighters and create your own moves.", onBack)
