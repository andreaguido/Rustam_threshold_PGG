
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

    # timeout_seconds =10


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):
        self.participant.vars['threshold_reached'] = False


class PledgedContribution(Page):
    def is_displayed(self):
        return self.participant.vars['threshold_reached'] is False

    form_model = 'player'
    form_fields = ['pledged_cont']


class PledgedResults(Page):
    def is_displayed(self):
        return self.participant.vars['threshold_reached'] is False

    def vars_for_template(self):
        return dict(remaining_to_treshold=Constants.threshold - self.group.total_group_contribution_in_all_rounds)
    def vars_for_template(self):
             return dict(
            p1plcontribution=self.group.get_player_by_id(1).pledged_cont,
            p2plcontribution=self.group.get_player_by_id(2).pledged_cont,
            p3plcontribution=self.group.get_player_by_id(3).pledged_cont,
            p4plcontribution=self.group.get_player_by_id(4).pledged_cont,
            p5plcontribution=self.group.get_player_by_id(5).pledged_cont
        )

class Contribute2(Page):
    def vars_for_template(self):
        import random
        return dict(
            remaining_to_treshold=Constants.threshold - self.group.total_group_contribution_in_all_rounds,
            a=random.randint(1, 3)
        )
    def is_displayed(self):
        return self.group.remaining_to_treshold_check is True and self.participant.vars['threshold_reached'] == 0


class Contribute(Page):
    def is_displayed(self):
        return self.participant.vars['threshold_reached'] is False

    form_model = 'player'
    form_fields = ['contribution']


class AfterThreshold(Page):
    def is_displayed(self):
        return self.participant.vars['threshold_reached'] is True and self.group.threshold_reached_previous is False


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.other_contributions()


class Results(Page):

    def vars_for_template(self):
        return dict(
            remaining_to_treshold=Constants.threshold - self.group.total_group_contribution_in_all_rounds,
            group_contribution=self.group.total_group_contribution,
            player_round_payoff = Constants.endowment - self.player.contribution + self.player.payoff,
            p1plcontribution=self.group.get_player_by_id(1).pledged_cont,
            p2plcontribution=self.group.get_player_by_id(2).pledged_cont,
            p3plcontribution=self.group.get_player_by_id(3).pledged_cont,
            p4plcontribution=self.group.get_player_by_id(4).pledged_cont,
            p5plcontribution=self.group.get_player_by_id(5).pledged_cont,
            p1contribution=self.group.get_player_by_id(1).contribution,
            p2contribution=self.group.get_player_by_id(2).contribution,
            p3contribution=self.group.get_player_by_id(3).contribution,
            p4contribution=self.group.get_player_by_id(4).contribution,
            p5contribution=self.group.get_player_by_id(5).contribution,
            private_contribution=Constants.endowment - self.player.contribution,
            perc_contribution=self.group.total_group_contribution_in_all_rounds/Constants.threshold,
            other_contribution0 = self.player.other_contribution0,
            other_contribution1 = self.player.other_contribution1,
            other_contribution2 = self.player.other_contribution2,
            other_contribution3 = self.player.other_contribution3,
            other_plcontribution0 = self.player.other_plcontribution0,
            other_plcontribution1 = self.player.other_plcontribution1,
            other_plcontribution2 = self.player.other_plcontribution2,
            other_plcontribution3 = self.player.other_plcontribution3,
            other_id0 = self.player.other_id0,
            other_id1 = self.player.other_id1,
            other_id2 = self.player.other_id2,
            other_id3 = self.player.other_id3
        )

    def is_displayed(self):
        return self.participant.vars['threshold_reached'] is False

class ResultsAfterThr(Page):

    def vars_for_template(self):
        return dict(
            remaining_to_treshold=Constants.threshold - self.group.total_group_contribution_in_all_rounds
        )

    def is_displayed(self):
        return self.participant.vars['threshold_reached'] is True


page_sequence = [Start,
                 Introduction,
                 PledgedContribution,
                 ResultsWaitPage,
                 PledgedResults,
                 Contribute,
                 ResultsWaitPage,
                 AfterThreshold,
                 Results,
                 ResultsAfterThr,
                 Contribute2,
                 ]
