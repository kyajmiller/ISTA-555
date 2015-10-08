# project 2a part 2 Naive Bayes self implementation

from __future__ import division
import math


def log2(x):
    return math.log(x) / math.log(2)


def get_entropy(x, y, z):
    x_log2_x = x * log2(x)
    y_log2_y = y * log2(y)
    z_log2_z = z * log2(z)

    entropy = -x_log2_x - y_log2_y - z_log2_z

    return entropy


def get_gain(entropy_word, prob_word, entropy_classes):
    gain = entropy_classes - (prob_word * entropy_word)

    return gain


def main():
    # train
    filein_train = open('project2a_training.txt', 'r')

    stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't",
                 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below',
                 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does',
                 "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from',
                 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll",
                 "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how',
                 "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its',
                 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not',
                 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',
                 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't",
                 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then',
                 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this',
                 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd",
                 "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where',
                 "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would',
                 "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves',
                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '.', ':', '?', '!', '(', ')', '"', '/']

    # part 4
    negwords = ["aren't", "can't", 'cannot', "couldn't", "didn't", "doesn't", "don't", "hadn't", "hasn't", "haven't",
                "isn't", "musn't", 'no', 'not', "shan't", "shouldn't", "wasn't", "weren't",
                "won't", "wouldn't", 'neither', 'never', 'nobody', 'none']

    # part 4
    punctuation = ['.', '"', "'", ',', '?', '/', '!', '(', ')', ':', ';']

    words_total = {}
    rate_0 = {}
    rate_1 = {}
    rate_2 = {}
    ratings = {'0': 0, '1': 0, '2': 0}
    train_total = 0

    for line in filein_train:
        train_total = train_total + 1
        get_rate = int(line[0])

        linewords = line.split()

        '''
		#part 4, add negation 
		for i in range(len(linewords)):
			if linewords[i] in negwords:
				follow_words = 1
				if (i + follow_words) < len(linewords):
					while linewords[i + follow_words] not in punctuation:
						linewords[i + follow_words] = str('NOT_' + linewords[i + follow_words])
						follow_words = follow_words + 1
		'''

        '''
		#part 5, add bigrams
		words_bigrams = []
		for i in linewords:
			words_bigrams.append(i)
			
		for i in range(len(linewords))[1:]:
			if (i + 1) < len(linewords):
				words_bigrams.append(str(linewords[i] + linewords[i + 1]))
		'''

        # for i in words_bigrams:
        for i in linewords:
            if i not in stopwords:
                if i in words_total.iterkeys():
                    words_total[i] = words_total[i] + 1
                else:
                    words_total[i] = 1

        if get_rate == 0:
            ratings['0'] = ratings['0'] + 1
            for i in linewords:
                if i not in stopwords:
                    if i in rate_0:
                        rate_0[i] = rate_0[i] + 1
                    else:
                        rate_0[i] = 1
        elif get_rate == 1:
            ratings['1'] = ratings['1'] + 1
            for i in linewords:
                if i not in stopwords:
                    if i in rate_1:
                        rate_1[i] = rate_1[i] + 1
                    else:
                        rate_1[i] = 1
        elif get_rate == 2:
            ratings['2'] = ratings['2'] + 1
            for i in linewords:
                if i not in stopwords:
                    if i in rate_2:
                        rate_2[i] = rate_2[i] + 1
                    else:
                        rate_2[i] = 1

    filein_train.close()


    # part 3
    # get prob of ratings (rating/total)
    r_prob_0 = ratings['0'] / train_total
    r_prob_1 = ratings['1'] / train_total
    r_prob_2 = ratings['2'] / train_total

    cd_words_total = words_total.copy()

    # part 3 information gain
    # calculate entropy
    entropy_classes = get_entropy(r_prob_0, r_prob_1, r_prob_2)

    entropy_words = words_total.copy()
    for i in entropy_words:
        prob_word = words_total[i] / train_total

        if i in rate_0:
            if i in rate_1:
                if i in rate_2:

                    e0 = rate_0[i] / words_total[i]
                    e1 = rate_1[i] / words_total[i]
                    e2 = rate_2[i] / words_total[i]

                    entropy_word = get_entropy(e0, e1, e2)
                else:
                    entropy_word = 0
            else:
                entropy_word = 0
        else:
            entropy_word = 0

        gain = get_gain(entropy_word, prob_word, entropy_classes)

        entropy_words[i] = gain

    filter_entropy_words = entropy_words.copy()
    for i in filter_entropy_words.keys():
        if filter_entropy_words[i] != entropy_classes:
            if i in rate_0:
                del rate_0[i]
            if i in rate_1:
                del rate_1[i]
            if i in rate_2:
                del rate_2[i]
            del cd_words_total[i]


    # part 3 frequency edit based on conditional proportions

    # probability of feature total
    for i in cd_words_total:
        cd_words_total[i] = cd_words_total[i] / train_total

    # probability of feature given rating 0
    cd_rate_0 = rate_0.copy()
    for i in cd_rate_0:
        cd_rate_0[i] = cd_rate_0[i] / r_prob_0
    for i in cd_rate_0.keys():
        if cd_rate_0[i] < 0.25:
            del cd_rate_0[i]
    for i in cd_rate_0.keys():
        cd_rate_0[i] = math.log(cd_rate_0[i])

    # probability of feature given rating 1
    cd_rate_1 = rate_1.copy()
    for i in cd_rate_1:
        cd_rate_1[i] = cd_rate_1[i] / r_prob_1
    for i in cd_rate_1.keys():
        if cd_rate_1[i] < 0.25:
            del cd_rate_1[i]
    for i in cd_rate_1.keys():
        cd_rate_1[i] = math.log(cd_rate_1[i])

    # probability of feature given rating 2
    cd_rate_2 = rate_2.copy()
    for i in cd_rate_2:
        cd_rate_2[i] = cd_rate_2[i] / r_prob_2
    for i in cd_rate_2.keys():
        if cd_rate_2[i] < 0.25:
            del cd_rate_2[i]
    for i in cd_rate_2.keys():
        cd_rate_2[i] = math.log(cd_rate_2[i])


    # ========================================================================================

    # test
    matches_total = 0
    test_total = 0

    # stats for 0 match
    rating_0 = 0
    result_0 = 0
    matches_0 = 0

    # stats for 1 match
    rating_1 = 0
    result_1 = 0
    matches_1 = 0

    # stats for 2 match
    rating_2 = 0
    result_2 = 0
    matches_2 = 0

    filein_test = open('testNOTbigrams.txt', 'r')

    for line in filein_test:
        test_total = test_total + 1
        get_rate = int(line[0])

        if get_rate == 0:
            rating_0 = rating_0 + 1
        elif get_rate == 1:
            rating_1 = rating_1 + 1
        elif get_rate == 2:
            rating_2 = rating_2 + 1

        linewords = line.split()

        '''
		#part 4, add negation 
		for i in range(len(linewords)):
			if linewords[i] in negwords:
				follow_words = 1
				if (i + follow_words) < len(linewords):
					while linewords[i + follow_words] not in punctuation:
						linewords[i + follow_words] = str('NOT_' + linewords[i + follow_words])
						follow_words = follow_words + 1
		'''

        '''
		#part 5, add bigrams
		words_bigrams = []
		for i in linewords:
			words_bigrams.append(i)
			
		for i in range(len(linewords))[1:]:
			if (i + 1) < len(linewords):
				words_bigrams.append(str(linewords[i] + linewords[i + 1]))
		'''

        # get 0 prob
        num_prob_0 = 0
        prob_0 = 1
        for i in linewords:
            if i in cd_rate_0:
                num_prob_0 = num_prob_0 + cd_rate_0[i]
        prob_0 = num_prob_0 + r_prob_0


        # get 1 prob
        num_prob_1 = 0
        prob_1 = 1
        for i in linewords:
            if i in cd_rate_1:
                num_prob_1 = num_prob_1 + cd_rate_1[i]
        prob_1 = num_prob_1 + r_prob_1


        # get 2 prob
        num_prob_2 = 0
        prob_2 = 1
        for i in linewords:
            if i in cd_rate_2:
                num_prob_2 = num_prob_2 + cd_rate_2[i]
        prob_2 = num_prob_2 + r_prob_2

        # get result
        result = ''
        if prob_0 > prob_1 and prob_0 > prob_2:
            result = 0
            result_0 = result_0 + 1
        elif prob_1 > prob_0 and prob_1 > prob_2:
            result = 1
            result_1 = result_1 + 1
        elif prob_2 > prob_0 and prob_2 > prob_1:
            result = 2
            result_2 = result_2 + 1

        if result == get_rate == 0:
            matches_total = matches_total + 1
            matches_0 = matches_0 + 1
        elif result == get_rate == 1:
            matches_total = matches_total + 1
            matches_1 = matches_1 + 1
        elif result == get_rate == 2:
            matches_total = matches_total + 1
            matches_2 = matches_2 + 1

    accuracy = matches_total / test_total

    print("Part 2: Naive Bayes from Scratch")
    print("Overall Accuracy: " + str(accuracy * 100))
    print("\n")

    f1_2 = 2 * (((matches_2 / result_2) * (matches_2 / rating_2)) / ((matches_2 / result_2) + (matches_2 / rating_2)))
    f1_0 = 2 * (((matches_0 / result_0) * (matches_0 / rating_0)) / ((matches_0 / result_0) + (matches_0 / rating_0)))
    f1_1 = 2 * (((matches_1 / result_1) * (matches_1 / rating_1)) / ((matches_1 / result_1) + (matches_1 / rating_1)))

    prec_0 = matches_0 / result_0
    prec_1 = matches_1 / result_1
    prec_2 = matches_2 / result_2

    rec_0 = matches_0 / rating_0
    rec_1 = matches_1 / rating_1
    rec_2 = matches_2 / rating_2

    print("Positive:")
    print("\tPrecision: " + str(prec_2))
    print("\tRecall: " + str(rec_2))
    print("\tF1 Score: " + str(f1_2))
    print("\n")

    print("Negative:")
    print("\tPrecision: " + str(prec_0))
    print("\tRecall: " + str(rec_0))
    print("\tF1 Score: " + str(f1_0))
    print("\n")

    print("Neutral:")
    print("\tPrecision: " + str(prec_1))
    print("\tRecall: " + str(rec_1))
    print("\tF1 Score: " + str(f1_0))
    print("\n")

    print result_0
    print result_1
    print result_2


if __name__ == '__main__':
    main()
