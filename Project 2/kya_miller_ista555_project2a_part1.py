# import statements
from __future__ import division


# main
def main():
    # part 1
    # sentiment lexicon
    positive = ['dazzling', 'brilliant', 'phenomenal', 'excellent', 'fantastic', 'gripping', 'mesmerizing',
                'riveting', 'spectacular', 'cool', 'awesome', 'thrilling', 'badass', 'excellent', 'moving', 'exciting',
                'love', 'wonderful', 'best', 'great', 'superb', 'still', 'beautiful']

    negative = ['suck', 'terrible', 'awful', 'unwatchable', 'hideous', 'bad', 'cliched', 'sucks', 'boring',
                'stupid', 'slow', 'bad', 'worst', 'waste', '?', '!']

    filein_1 = open('project2a_test.txt', 'r')

    total = 0
    matches = 0

    rating_0 = 0
    rating_1 = 0
    rating_2 = 0

    result_0 = 0
    result_1 = 0
    result_2 = 0

    match_0 = 0
    match_1 = 0
    match_2 = 0

    for line in filein_1:
        total = total + 1

        rating = int(line[0])
        if rating == 0:
            rating_0 = rating_0 + 1
        if rating == 1:
            rating_1 = rating_1 + 1
        if rating == 2:
            rating_2 = rating_2 + 1

        poscount = 0
        negcount = 0

        linewords = line.split()
        for i in linewords:
            if i in positive:
                poscount = poscount + 1
            if i in negative:
                negcount = negcount + 1

        if poscount > negcount:
            result = 2
            result_2 = result_2 + 1
        if negcount > poscount:
            result = 0
            result_0 = result_0 + 1
        if poscount == negcount:
            result = 1
            result_1 = result_1 + 1

        if rating == result:
            matches = matches + 1
        if rating == result == 0:
            match_0 = match_0 + 1
        if rating == result == 1:
            match_1 = match_1 + 1
        if rating == result == 2:
            match_2 = match_2 + 1

    accuracy = matches / total
    pos_f1 = 2 * (((match_2 / result_2) * (match_2 / rating_2)) / ((match_2 / result_2) + (match_2 / rating_2)))
    neg_f1 = 2 * (((match_0 / result_0) * (match_0 / rating_0)) / ((match_0 / result_0) + (match_0 / rating_0)))
    neut_f1 = 2 * (((match_1 / result_1) * (match_1 / rating_1)) / ((match_1 / result_1) + (match_1 / rating_1)))

    print("Part 1: Lexicon-Based Movie Rating Detector")
    print("Overall Accuracy: " + str(matches) + "/" + str(total) + ", " + str(accuracy * 100))
    print("\n")

    print("Positive:")
    print("\tPrecision: " + str(match_2 / result_2))
    print("\tRecall: " + str(match_2 / rating_2))
    print("\tF1 Score: " + str(pos_f1))
    print("\n")

    print("Negative:")
    print("\tPrecision: " + str(match_0 / result_0))
    print("\tRecall: " + str(match_0 / rating_0))
    print("\tF1 Score: " + str(neg_f1))
    print("\n")

    print("Neutral:")
    print("\tPrecision: " + str(match_1 / result_1))
    print("\tRecall: " + str(match_1 / rating_1))
    print("\tF1 Score: " + str(neut_f1))
    print("\n")


if __name__ == '__main__':
    main()
