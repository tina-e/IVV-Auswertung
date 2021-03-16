import os
import statistics


# each topic has its own dict:
# (snippet_num, isTrunc): [ratings]
# Example: (0, True): [3, 2, 4, ...]
def fill_list():
    topic_0 = {}
    topic_1 = {}
    topic_2 = {}
    topic_3 = {}
    topic_4 = {}
    topic_5 = {}
    topics = [topic_0, topic_1, topic_2, topic_3, topic_4, topic_5]

    for topic in topics:
        for i in range(0, 8):
            key = (i, True)
            topic[key] = []
            key = (i, False)
            topic[key] = []
    return topics


# order topics how the participants retrieved them
def get_topics_in_user_oder(order, topics):
    topics = [x for _, x in sorted(zip(order, topics))]
    return topics


# go back to original order of topics
def get_topics_ordered_back(order, topics):
    reverse_order = [5 - x for x in order]
    topics = [x for _, x in sorted(zip(reverse_order, topics))]
    topics.reverse()
    return topics


# get ratings from data
def get_ratings_per_user(lines, topics):
    sorter = []
    ratings = []
    truncs = []
    topic_counter = 0
    for value_array in lines:
        if len(value_array) == 8 and 7 in value_array:
            sorter = value_array
        elif len(value_array) == 8 and 7 not in value_array:
            ratings = value_array
        elif len(value_array) == 4:
            truncs = value_array

        if len(sorter) != 0 and len(ratings) != 0 and len(truncs) != 0:
            ratings = [x for _, x in sorted(zip(sorter, ratings))]
            for snippet_id, rating in enumerate(ratings):
                is_trunc = False
                if snippet_id in truncs:
                    is_trunc = True
                topics[topic_counter][(snippet_id, is_trunc)].append(rating)

            ratings.clear()
            sorter.clear()
            truncs.clear()
            topic_counter += 1
    return topics


# iterate all files for general ratings
def get_all_ratings():
    topics = fill_list()
    folder = "sessions-cleaned"
    for filename in os.listdir(folder):
        file = open(folder + "/" + filename, "rt")
        lines = [[int(value) for value in line.split(",") if value != "\n"] for line in file]

        topic_order = []
        for value_array in lines:
            if len(value_array) == 6:
                topic_order = value_array
                lines.remove(value_array)
                break

        topics = get_topics_in_user_oder(topic_order, topics)
        topics = get_ratings_per_user(lines, topics)
        topics = get_topics_ordered_back(topic_order, topics)

    return topics


def print_results(ratings):
    print("presentation:    (snippet_num, isTruncated): [ratings]")
    for topic_num, topic_ratings in enumerate(ratings):
        print(topic_ratings)


def print_number_of_ratings(ratings):
    rating_nums = []
    for topic_num, topic_ratings in enumerate(ratings):
        # print("Topic", topic_num)
        for key, snippet_ratings in topic_ratings.items():
            # print("#ratings for ", key, "\t", len(snippet_ratings))
            rating_nums.append(len(snippet_ratings))
    print("avg #ratings per item:", statistics.mean(rating_nums))

def print_avg_of_ratings(ratings, is_trunc):
    ratings_to_calc = []
    for topic_num, topic_ratings in enumerate(ratings):
        for key, snippet_ratings in topic_ratings.items():
            if key[1] == is_trunc:
                ratings_to_calc += snippet_ratings
    print("avg rating for truncated(", is_trunc, "):", statistics.mean(ratings_to_calc), "/ 4")

def print_checking(ratings, correctness):
    sum = 0
    for rating_dict in ratings:
        for key, value in rating_dict.items():
            sum += len(value)
    print("alle:", sum)

    sum = 0
    for rating_dict in ratings:
        for key, value in rating_dict.items():
            if key[1]:
                sum += len(value)
    print("truncs:", sum)

    sum = 0
    for rating_dict in ratings:
        for key, value in rating_dict.items():
            if not key[1]:
                sum += len(value)
    print("fulls:", sum)

    sum = 0
    for topic_num, rating_dict in enumerate(ratings):
        for key, value in rating_dict.items():
            snippet_num = key[0]
            if correctness[topic_num][snippet_num] == 1:
                sum += len(value)
    print("corrects(gt):", sum)

    sum = 0
    for topic_num, rating_dict in enumerate(ratings):
        for key, value in rating_dict.items():
            snippet_num = key[0]
            if correctness[topic_num][snippet_num] == 2:
                sum += len(value)
    print("incorrects(gt):", sum)

    sum = 0
    for topic_num, rating_dict in enumerate(ratings):
        for key, value in rating_dict.items():
            snippet_num = key[0]
            if correctness[topic_num][snippet_num] == 1 and key[1]:
                sum += len(value)
    print("corrects(gt) AND trunc:", sum)

    sum = 0
    for topic_num, rating_dict in enumerate(ratings):
        for key, value in rating_dict.items():
            snippet_num = key[0]
            if correctness[topic_num][snippet_num] == 1 and not key[1]:
                sum += len(value)
    print("corrects(gt) AND full:", sum)

def print_comparison_by_correctness(ratings, correctness):
    correct_trunc = [0, 0, 0, 0, 0]
    correct_full = [0, 0, 0, 0, 0]
    incorrect_trunc = [0, 0, 0, 0, 0]
    incorrect_full = [0, 0, 0, 0, 0]
    for topic_num, rating_dict in enumerate(ratings):
        for key, value in rating_dict.items():
            snippet_num = key[0]
            is_trunc = key[1]
            if correctness[topic_num][snippet_num] == 1:  # correct GT
                for rating in value:
                    if is_trunc:
                        correct_trunc[rating] += 1
                    else:
                        correct_full[rating] += 1
            elif correctness[topic_num][snippet_num] == 2:  # incorrect GT
                for rating in value:
                    if is_trunc:
                        incorrect_trunc[rating] += 1
                    else:
                        incorrect_full[rating] += 1
    print(correct_trunc)
    print(correct_full)
    print(incorrect_trunc)
    print(incorrect_full)


    all_truncs = [correct_trunc[i] + incorrect_trunc[i] for i in range(len(correct_trunc))]
    all_fulls = [correct_full[i] + incorrect_full[i] for i in range(len(correct_full))]

    from scipy.stats import wilcoxon, chi2_contingency, shapiro
    print(shapiro(all_fulls))
    print(shapiro(all_truncs))
    w, p1 = wilcoxon(all_truncs, all_fulls)
    print(w)
    print(p1)

    data = [all_truncs, all_fulls]
    stat, p, dof, expected = chi2_contingency(data)
    print(p)




ratings = get_all_ratings()
correctness = [[2, 2, 2, 2, 1, 1, 1, 1], [1, 1, 2, 2, 1, 1, 2, 2],
               [2, 2, 2, 2, 1, 1, 1, 1], [1, 2, 1, 1, 0, 2, 2, 2],
               [2, 2, 2, 1, 2, 1, 1, 1], [2, 2, 1, 2, 1, 1, 1, 2]]


print_results(ratings)
print(" ")
print("----For Checking------")
print_checking(ratings, correctness)

print(" ")
print("------Statistics (may be not usefull)------")
print_number_of_ratings(ratings)
print_avg_of_ratings(ratings, True)
print_avg_of_ratings(ratings, False)

print(" ")
print("------Compared with Labels-------")
print_comparison_by_correctness(ratings, correctness)




########################################################################################################

def print_comparison(ratings, correctness):
    CORRECT = 1
    NOT_CORRECT = 2

    num_correct_judgement_trunc = 0
    num_correct_judgement_trunc_sure = 0
    num_correct_judgement_trunc_semisure = 0
    num_correct_judgement_full = 0
    num_correct_judgement_full_sure = 0
    num_correct_judgement_full_semisure = 0

    num_unsure_judgement_trunc = 0
    num_unsure_judgement_full = 0

    num_incorrect_judgement_trunc = 0
    num_incorrect_judgement_trunc_sure = 0
    num_incorrect_judgement_trunc_semisure = 0
    num_incorrect_judgement_full = 0
    num_incorrect_judgement_full_sure = 0
    num_incorrect_judgement_full_semisure = 0

    for topic_num, topic_ratings in enumerate(ratings):
        current_topic_correctness = correctness[topic_num]
        for key, snippet_ratings in topic_ratings.items():
            current_snippet_num = key[0]

            # correct judgements for "correct" labeled snippets
            if current_topic_correctness[current_snippet_num] == CORRECT and snippet_ratings[current_snippet_num] < 2:
                if key[1]: # is truncated
                    num_correct_judgement_trunc += 1
                    if snippet_ratings[current_snippet_num] == 1:
                        num_correct_judgement_trunc_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 0:
                        num_correct_judgement_trunc_sure += 1
                else:
                    num_correct_judgement_full += 1
                    if snippet_ratings[current_snippet_num] == 1:
                        num_correct_judgement_full_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 0:
                        num_correct_judgement_full_sure += 1

            # correct judgements for "incorrect" labeled snippets
            elif current_topic_correctness[current_snippet_num] == NOT_CORRECT and snippet_ratings[current_snippet_num] > 2:
                if key[1]:  # is truncated
                    num_correct_judgement_trunc += 1
                    if snippet_ratings[current_snippet_num] == 3:
                        num_correct_judgement_trunc_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 4:
                        num_correct_judgement_trunc_sure += 1
                else:
                    num_correct_judgement_full += 1
                    if snippet_ratings[current_snippet_num] == 3:
                        num_correct_judgement_full_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 4:
                        num_correct_judgement_full_sure += 1

            # incorrect judgements for "correct" labeled snippets
            elif current_topic_correctness[current_snippet_num] == CORRECT and snippet_ratings[current_snippet_num] > 2:
                if key[1]: # is truncated
                    num_incorrect_judgement_trunc += 1
                    if snippet_ratings[current_snippet_num] == 3:
                        num_incorrect_judgement_trunc_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 4:
                        num_incorrect_judgement_trunc_sure += 1
                else:
                    num_incorrect_judgement_full += 1
                    if snippet_ratings[current_snippet_num] == 3:
                        num_incorrect_judgement_full_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 4:
                        num_incorrect_judgement_full_sure += 1

            # incorrect judgements for "incorrect" labeled snippets
            elif current_topic_correctness[current_snippet_num] == NOT_CORRECT and snippet_ratings[current_snippet_num] < 2:
                if key[1]: # is truncated
                    num_incorrect_judgement_trunc += 1
                    if snippet_ratings[current_snippet_num] == 1:
                        num_incorrect_judgement_trunc_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 0:
                        num_incorrect_judgement_trunc_sure += 1
                else:
                    num_incorrect_judgement_full += 1
                    if snippet_ratings[current_snippet_num] == 1:
                        num_incorrect_judgement_full_semisure += 1
                    elif snippet_ratings[current_snippet_num] == 0:
                        num_incorrect_judgement_full_sure += 1

            # handle "unsure"-judgements
            elif snippet_ratings[current_snippet_num] == 2:
                if key[1]: # is truncated
                    num_unsure_judgement_trunc += 1
                else: # is full-sentence
                    num_unsure_judgement_full += 1

    print("#correct judgements with truncated:", num_correct_judgement_trunc, "// semi-sure:", num_correct_judgement_trunc_semisure, "| sure:", num_correct_judgement_trunc_sure)
    print("#correct judgements with full-sent:", num_correct_judgement_full, "// semi-sure:", num_correct_judgement_full_semisure, "| sure:", num_correct_judgement_full_sure)

    print("#incorrect judgements with truncated:", num_incorrect_judgement_trunc, "// semi-sure:", num_incorrect_judgement_trunc_semisure, "| sure:", num_incorrect_judgement_trunc_sure)
    print("#incorrect judgements with full-sent:", num_incorrect_judgement_full, "// semi-sure:", num_incorrect_judgement_full_semisure, "| sure:", num_incorrect_judgement_full_sure)

    print("#unsure judgements with truncated:", num_unsure_judgement_trunc)
    print("#unsure judgements with full-sent:", num_unsure_judgement_full)
#print_comparison(ratings, correctness)
