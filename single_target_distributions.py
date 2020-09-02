from coin_string import RandomCoinString
import numpy as np
import matplotlib.pyplot as plt
from colors import colors
import set_operations


def run_many_single_target_games(target, n_runs):
    samples = []
    for i in range(n_runs):
        cs = RandomCoinString()
        samples.append(cs.find_first_occurrence([target])[0])
    return samples


def get_single_target_distribution(target_str, bin_error):
    print("calculating probability distribution for {}".format(target_str))
    num_of_samples = 5000
    accumulating_samples = None
    accumulating_samples_hist = None
    b_errors_are_small = False
    error_arr = np.nan
    while not b_errors_are_small:
        samples = run_many_single_target_games(target_str, num_of_samples)
        samples_hist = np.histogram(samples, range(max(samples)), density=True)[0]
        if accumulating_samples is None:
            accumulating_samples = samples
            accumulating_samples_hist = samples_hist
        else:
            n_bins = max(len(accumulating_samples_hist), len(samples_hist))
            samples_hist = np.concatenate([samples_hist, [0] * (n_bins - len(samples_hist))])
            accumulating_samples_hist = np.concatenate([accumulating_samples_hist, [0] * (n_bins - len(accumulating_samples_hist))])
            error_arr = np.abs(accumulating_samples_hist - samples_hist) * 2
            error = np.max(error_arr)
            print("{} random runs, std is : {}".format(num_of_samples, error))
            b_errors_are_small = error < bin_error
            num_of_samples *= 2
            accumulating_samples_hist += samples_hist
            accumulating_samples_hist /= sum(accumulating_samples_hist)
    return accumulating_samples_hist, error_arr

def get_targets_histograms_dict_with_errors(target_arr,bin_error):
    targets_histograms_dict = {}
    targets_histograms_dict_bin_errors = {}
    for target_str in target_arr:
        targets_histograms_dict[target_str],targets_histograms_dict_bin_errors[target_str] = get_single_target_distribution(target_str,bin_error)
    return targets_histograms_dict,targets_histograms_dict_bin_errors

def plot_single_target_distribution(hist, error_arr, color=None, axes=None,label=None):
    if axes is None:
        axes = plt.gca()
    if color is None:
        color = next(colors)
    axes.bar(range(len(hist)), hist, width=1, color=color,label=label)
    axes.errorbar(range(len(hist)), hist, error_arr / 2, fmt="none", ecolor=color)
    axes.vlines(get_com(hist), 0, max(hist), color=color,linestyles="--")


def get_target_str_hierarchy(targets_histograms_dict, targets_histograms_dict_bin_errors):
    segments_dict = {}
    for target_str in targets_histograms_dict:
        hist, error_arr = targets_histograms_dict[target_str],targets_histograms_dict_bin_errors[target_str]
        mean, mean_error = get_com_with_error(hist, error_arr)
        segments_dict[target_str] = (mean - mean_error, mean + mean_error)
    return split_into_hierarchies(segments_dict)


def split_into_hierarchies(segments_dict):
    hierarchies = []
    keys_sorted = sorted(segments_dict.keys(), key=lambda key: segments_dict[key][0])
    upper_buond_of_hierarchy = segments_dict[keys_sorted[0]][1]
    keys_in_hierarchy = [key for key in keys_sorted if segments_dict[key][0] < upper_buond_of_hierarchy]
    hierarchies.append(keys_in_hierarchy)
    left_over_segments_dict = {key: segments_dict[key] for key in segments_dict.keys() if key not in keys_in_hierarchy}
    if len(left_over_segments_dict) != 0:
        hierarchies += split_into_hierarchies(left_over_segments_dict)
    return hierarchies


def get_com(P):
    return np.sum(P * np.arange(len(P)))


def get_com_with_error(P, bin_errors):
    """
    :param bin_errors: bin_errors as the 95% confidence level error of each bin
    :return: returns ( the center-of-mass of P, the 95% confidence level error of the com of P with regards to bin_errors)
    """
    num_of_random_realisations = 1000
    random_realisations = np.random.normal(np.tile(P, (num_of_random_realisations, 1)), np.tile(bin_errors / 2, (num_of_random_realisations, 1)))
    possible_coms = [get_com(random_realisation) for random_realisation in random_realisations]
    com_error = np.std([possible_coms], ddof=1) * 2
    return get_com(P), com_error


if __name__ == "__main__":
    hist_dat_011 = get_single_target_distribution("011", 0.01)
    hist_dat_111 = get_single_target_distribution("111",0.01)

    plot_single_target_distribution(*hist_dat_011, label="011")
    plot_single_target_distribution(*hist_dat_111,label="111")

    plt.legend()
    # hierarchies = get_target_str_hierarchy(set_operations.get_all_n_digit_strings(3), 0.01)
