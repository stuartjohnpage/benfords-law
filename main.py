import sys
import math
from collections import defaultdict
import matplotlib.pyplot as plt

BENFORD_FIRST = [30.1, 17.6, 12.5, 9.7, 7.9, 6.7, 5.8, 5.1, 4.6]
BENFORD_SECOND = [11.9, 11.3, 10.8, 10.4, 10.0, 9.67, 9.3, 9.0, 8.7, 8.5]

def load_data(filename):
    """Open a text file & return a list of strings"""
    with open(filename) as f:
        return f.read().strip().split('\n')

def count_first_digits(data_list):
    first_digits = defaultdict(int)
    for sample in data_list:
        if sample == '':
            continue
        try:
            int(sample)
        except ValueError as e:
            print(e, file=sys.stderr)
            print("Sample must be integers. Exiting...", file=sys.stderr)
            sys.exit(1)
        first_digits[sample[0]] += 1
    first_digits.pop("0", None)
    data_count = [v for (k, v) in sorted(first_digits.items())]

    total_count = sum(data_count)
    data_pct = [(i / total_count) * 100 for i in data_count]
    return data_count, data_pct, total_count

def count_second_digits(data_list):
    second_digits = defaultdict(int)
    for sample in data_list:
        if sample == '':
            continue
        try:
            int(sample)
        except ValueError as e:
            print(e, file=sys.stderr)
            print("Sample must be integers. Exiting...", file=sys.stderr)
            sys.exit(1)
        second_digits[sample[1]] += 1
    data_count = [v for (k, v) in sorted(second_digits.items())]

    total_count = sum(data_count)
    data_pct = [(i / total_count) * 100 for i in data_count]
    return data_count, data_pct, total_count


def get_expected_counts(total_count, method):
    if method == 'first':
        return [round(p * total_count / 100) for p in BENFORD_FIRST]
    else:
        return [round(p * total_count / 100) for p in BENFORD_SECOND]

def chi_square_test(data_count, expected_counts, method):
    if method == "first":
        chi_square_stat = 0
        for data, expected in zip(data_count, expected_counts):
            chi_square = math.pow(data - expected, 2)
            chi_square_stat += chi_square / expected
        print("\nChi Squared Test Statistic = {:.3}".format(chi_square_stat))
        print("Critical value at a P-value of 0.05 is 15.51.")

        return chi_square_stat < 15.51
    else:
        chi_square_stat = 0
        for data, expected in zip(data_count, expected_counts):
            chi_square = math.pow(data - expected, 2)
            chi_square_stat += chi_square / expected
        print("\nChi Squared Test Statistic = {:.3}".format(chi_square_stat))
        print("Critical value at a P-value of 0.05 is 16.92.")

        return chi_square_stat < 16.92

def bar_chart(data_pct, method):
    fig, ax = plt.subplots()
    index = [i + 1 for i in range(len(data_pct))]

    fig.canvas.manager.set_window_title('Percentage {} Digits'.format(method))
    ax.set_title('Data vs Benford Values', fontsize=15)
    ax.set_ylabel('Frequency (%)', fontsize=16)
    ax.set_xticks(index)
    ax.set_xticklabels(index, fontsize=14)

    rects = ax.bar(index, data_pct, width=0.95, color='black', label='Data')

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2, height,
                '{:0.1f}'.format(height), ha='center', va='bottom', fontsize=13)

    if method =="first":
        ax.scatter(index, BENFORD_FIRST, s=150, c='red', zorder=2, label='Benford {}'.format(method))
    else:
        ax.scatter(index, BENFORD_SECOND, s=150, c='red', zorder=2, label='Benford {}'.format(method))

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.legend(prop={'size':15}, frameon=False)

    plt.show()

def main():
    while True:
        filename = input("\nPlease enter the name of the file with COUNT data: ")
        try:
            data_list = load_data(filename)
        except IOError as e:
            print("{}. Try again.".format(e), file=sys.stderr)
        else:
            break
    data_count, data_pct, total_count = count_first_digits(data_list)
    second_data_count, second_data_pct, second_total_count = count_second_digits(data_list)

    first_expected_counts = get_expected_counts(total_count, "first")
    second_expected_counts = get_expected_counts(second_total_count, "second")
    print("\nObserved first counts = {}".format(data_count))
    print("Expected counts = {}".format(first_expected_counts), "\n")

    print("\nObserved second counts = {}".format(second_data_count))
    print("Expected counts = {}".format(second_expected_counts), "\n")

    print("First Digit Probabilities")
    for i in range(1, 10):
        print("{}: observed: {:.3f} expected: {:.3f}".
              format(i, data_pct[i - 1] / 100, BENFORD_FIRST[i - 1] / 100))
    if chi_square_test(data_count, first_expected_counts, "first"):
        print("Observed distribution matches expected distribution")
    else:
        print("Observed distribution does not match expected.", file=sys.stderr)

    print("Second Digit Probabilities")
    for i in range(0, 10):
        print("{}: observed: {:.3f} expected: {:.3f}".
              format(i, second_data_pct[i - 1] / 100, BENFORD_SECOND[i - 1] / 100))
    if chi_square_test(second_data_count, second_expected_counts, "second"):
        print("Observed distribution matches expected distribution")
    else:
        print("Observed distribution does not match expected.", file=sys.stderr)

    bar_chart(data_pct, "first")
    bar_chart(second_data_pct, "second")
    sys.exit(0)


if __name__ == '__main__':
    main()


def data_wrangler():
    while True:
        filename = input("\nPlease enter the name of the file you would like to wrangle ")
        try:
            data_list = load_data(filename)
        except IOError as e:
            print("{}. Try again.".format(e), file=sys.stderr)
        else:
            break
    wrangled_data = []

    for i in range(0, len(data_list), 3 ):
        wrangled_data.append(data_list[i])
    print(wrangled_data)

    with open('orleans_2008_votes.txt', 'w') as f:
        for item in wrangled_data:
            f.write("%s\n" % item)