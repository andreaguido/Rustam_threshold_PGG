from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


class Constants(BaseConstants):
    name_in_url = 'TPG_inequality_mechanism'
    players_per_group = 5
    num_others_per_group = 4
    num_rounds = 10
    endowment = c(10)
    threshold = 110
    payoff_after_threshold= c(10)
    remain_th = c(50)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):

    total_group_contribution = models.IntegerField(initial=0)
    total_group_contribution_in_all_rounds = models.IntegerField(initial=0)
    threshold_reached = models.BooleanField(initial=False)
    threshold_reached_previous = models.BooleanField(initial=False)
    total_group_plcontribution = models.CurrencyField(initial=0)
    total_group_plcontribution_in_all_rounds = models.CurrencyField(initial=0)
    remaining_to_treshold = models.CurrencyField(initial=110)
    remaining_to_treshold_check = models.BooleanField(initial = False)
    roundwanted = models.IntegerField(initial = 11)
    remains = models.IntegerField(initial = 110)
    a = models.IntegerField(initial = 0)
    b = models.IntegerField(initial = 0)
    c = models.IntegerField(initial=0)
    d = models.IntegerField(initial=0)
    e = models.IntegerField(initial=0)

    def other_contributions(self):
        for p in self.get_players():
            for i in range(Constants.players_per_group-1):
                id = p.get_others_in_group()[i]
                if i == 0:
                    p.other_id0 = id.id_in_group
                    p.other_plcontribution0 = id.pledged_cont
                    p.other_contribution0 = id.contribution
                elif i == 1:
                    p.other_id1 = id.id_in_group
                    p.other_plcontribution1 = id.pledged_cont
                    p.other_contribution1 = id.contribution
                elif i == 2:
                    p.other_id2 = id.id_in_group
                    p.other_plcontribution2 = id.pledged_cont
                    p.other_contribution2 = id.contribution
                elif i == 3:
                    p.other_id3 = id.id_in_group
                    p.other_plcontribution3 = id.pledged_cont
                    p.other_contribution3 = id.contribution

    def set_payoffs(self):

        # First, check if the group reached the threshold in the previous round, and check it in the current round
        import random
        self.total_group_contribution = sum([p.contribution for p in self.get_players()])
        self.total_group_contribution_in_all_rounds = sum([self.total_group_contribution for self in self.in_all_rounds()])
        self.total_group_plcontribution = sum([p.pledged_cont for p in self.get_players()])
        self.total_group_plcontribution_in_all_rounds = sum([self.total_group_plcontribution for self in self.in_all_rounds()])
        self.remaining_to_treshold = Constants.threshold - self.total_group_contribution_in_all_rounds
        self.remains = int(self.remaining_to_treshold)

        if self.round_number > 1:
            self.threshold_reached_previous = self.in_round(self.round_number - 1).threshold_reached


        while (self.a == self.b) or (self.c == self.b) or (self.c == self.d) or (self.e == self.d) or (self.a == self.e) or (self.c == self.e) or (self.e == self.b) or (self.c == self.a) or (self.d == self.b) or (self.d == self.a):
                self.a = random.randint(1, 5)
                self.b = random.randint(1, 5)
                self.c = random.randint(1, 5)
                self.d = random.randint(1, 5)
                self.e = random.randint(1, 5)

        if self.remaining_to_treshold < Constants.remain_th:
            self.remaining_to_treshold_check = True

        #self.remaining_contribution_to_threshold = Constants.threshold - self.total_group_contribution_in_all_rounds

        if self.total_group_contribution_in_all_rounds >= Constants.threshold:
            self.threshold_reached = True
            for p in self.get_players():
                p.participant.vars['threshold_reached'] = True
        else:
            self.threshold_reached = False
            for p in self.get_players():
                p.participant.vars['threshold_reached'] = False


        players = self.get_players()

        for p in players:
                p.total_payoff = sum([p.payoff for p in p.in_all_rounds()])



        for p in self.get_players():
            if p.participant.vars['threshold_reached'] is True and self.threshold_reached_previous is True:
                p.payoff = Constants.payoff_after_threshold + Constants.endowment
            else:
                p.payoff = Constants.endowment - p.contribution

        print("Total group contribution:", self.total_group_contribution)
        print("Total group contribution in all rounds:", self.total_group_contribution_in_all_rounds)
        print("Threshold reached:", self.threshold_reached)
        for p in players:
            print("Round number:", self.round_number)
            print("Player", p.id_in_group, "contribution is:", p.contribution)
            print("Player", p.id_in_group, "remaining endowment:", p.remaining_endowment)
            print("Player", p.id_in_group, "payoff is:", p.payoff)
            print("Player", p.id_in_group, "claims to contribute:", p.pledged_cont)


class Player(BasePlayer):

    remaining_endowment = models.IntegerField(initial=0)
    total_remaining_endowment = models.IntegerField(initial=Constants.endowment)
    total_payoff = models.CurrencyField()
    other_contribution0 = models.IntegerField()
    other_contribution1 = models.IntegerField()
    other_contribution2 = models.IntegerField()
    other_contribution3 = models.IntegerField()
    other_id0 = models.IntegerField()
    other_id1 = models.IntegerField()
    other_id2 = models.IntegerField()
    other_id3 = models.IntegerField()
    other_plcontribution0 = models.IntegerField()
    other_plcontribution1 = models.IntegerField()
    other_plcontribution2 = models.IntegerField()
    other_plcontribution3 = models.IntegerField()

    pledged_cont = models.IntegerField(
        choices=[0, 5, 10],
        initial=0,
        label="Out of your 10 units, how much do you pledge to contribute to TPG account?"
    )

    contribution = models.IntegerField(
        choices=[0, 5, 10],
        initial=0,
        label="Out of your 10 units, how much will you actually contribute to TPG account?"
    )


    # def contribution_max(self):
    #     return self.total_remaining_endowment

    # def calculate_endowment(self):
    #
    #     self.remaining_endowment = Constants.endowment-self.contribution
    #     self.total_remaining_endowment = sum([self.remaining_endowment in self.in_all_rounds()])
    #     self.contribution_in_all_rounds = sum([self.contribution in self.in_all_rounds()])
    #
    #     print("Player:", self.id_in_group, "remaining endowment:", self.remaining_endowment)
    #     print("Player:", self.id_in_group, "total remaining endowment:", self.total_remaining)
    #     print("Player:", self.id_in_group, "contribution in all rounds:", self.contribution_in_all_rounds)


