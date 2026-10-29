from ui.comingsoon import ComingSoonScreen


# Campaign mode: play through the story and beat the bosses. Replace this class with the real screen
class CampaignScreen(ComingSoonScreen):
    def __init__(self, parent, onBack):
        super().__init__(parent, "Campaign", "Follow the story and take on the bosses one by one.", onBack)
