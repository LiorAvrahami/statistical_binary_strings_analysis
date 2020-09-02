from coin_string import RandomCoinString
from graphs_computations import VictoryGraph
import itertools
import set_operations

def get_2_player_game_statistics(target_string_1,target_string_2,expected_uncertainty):
    """
    :param expected_uncertainty: the 95% confidence rate (2-sigma) uncertainty of the output probability
    :return: the probability of target_string_1 winning against target_string_2 +- expected_uncertainty
    """
    """
        worst uncertainty possible is 2/sqrt(number_of_digits_in_strings) {it depends on p but we only need an upper bound}
        so: 2/sqrt(number_of_digits_in_strings) = expected_uncertainty => number_of_digits_in_strings = 4/(expected_uncertainty**2)
        num_of_rounds = 4/(expected_uncertainty**2)
    """
    num_of_rounds = int(4/(expected_uncertainty**2))
    num_of_1_wins = 0
    for i in range(num_of_rounds):
        if target_string_1 == RandomCoinString().find_first_occurrence((target_string_1,target_string_2))[1]:
            num_of_1_wins += 1
    return num_of_1_wins/num_of_rounds

class NPlayerGameStatistics(dict):
    uncertainty:float
    targets:list

    def __init__(self, uncertainty,targets):
        super().__init__()
        self.uncertainty = uncertainty
        self.targets = targets

    def get_victory_graph(self):
        graph = VictoryGraph()
        for p1 in self.targets:
            graph[p1] = {p2 for p2 in self.targets if
                         self[p1,p2] > 0.5 + self.uncertainty}
        return graph

    def __getitem__(self, item):
        try:
            return super().__getitem__(item)
        except KeyError:
            if item[1] == item[0]:
                return 0.5
            else:
                return 1-super().__getitem__((item[1],item[0]))

def get_n_player_game_statistics(target_strings,expected_uncertainty):
    game_statistics = NPlayerGameStatistics(expected_uncertainty,target_strings)
    all_couples = set_operations.get_all_couples_minimal(target_strings)
    for i,(target_string_1,target_string_2) in enumerate(all_couples):
        print("{}%".format(100*i/len(all_couples)))
        game_statistics[target_string_1,target_string_2] = get_2_player_game_statistics(target_string_1,target_string_2,expected_uncertainty)

    return game_statistics

if __name__ == "__main__":
    pass