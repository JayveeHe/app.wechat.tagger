__author__ = 'jayvee'


class Reaction:
    def __init__(self, reaction_id, reaction_type, reaction_a_id, reaction_user_id, reaction_date, is_checked=False):
        self.reaction_id = reaction_id
        self.reaction_type = reaction_type
        self.reaction_a_id = reaction_a_id
        self.reaction_user_id = reaction_user_id
        self.reaction_date = reaction_date
        self.is_checked = is_checked
