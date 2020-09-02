import pickle
import set_operations
import simulate_game
import single_target_distributions

n = 3
graph_acceptable_error = 0.01
single_player_distributions_bin_error = 0.001

targets = set_operations.get_all_n_digit_strings(n)
game_statistics_file_name = "n={}_grapherror={}.game_statistics".format(n,graph_acceptable_error)
single_player_distributions_file_name = "n={}_binerror={}.single_player_distributions".format(n, single_player_distributions_bin_error)
try:
    game_statistics = pickle.load(open(game_statistics_file_name, "rb"))
except:
    game_statistics = simulate_game.get_n_player_game_statistics(target_strings=targets, expected_uncertainty=graph_acceptable_error)
    pickle.dump((game_statistics), open(game_statistics_file_name, "wb"))

try:
    # raise Exception
    single_player_distributions,single_player_distributions_errors = pickle.load(open(single_player_distributions_file_name, "rb"))
except:
    single_player_distributions,single_player_distributions_errors = single_target_distributions.get_targets_histograms_dict_with_errors(targets,single_player_distributions_bin_error)
    pickle.dump((single_player_distributions,single_player_distributions_errors), open(single_player_distributions_file_name, "wb"))

hierarchies = single_target_distributions.get_target_str_hierarchy(single_player_distributions,single_player_distributions_errors)
victory_graph = game_statistics.get_victory_graph()
victory_graph.print()
victory_graph.plot(hierarchies)
print("number of loops is ",victory_graph.get_number_of_loops())