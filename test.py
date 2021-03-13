topic_0 = {}
topic_1 = {}
topic_2 = {}
topic_3 = {}
topic_4 = {}
topic_5 = {}
topics = [topic_0, topic_1, topic_2, topic_3, topic_4, topic_5]

for topic in topics:
    for i in range(0,8):
        key = (i, True)
        topic[key] = []

        key = (i, False)
        topic[key] = []

print(topics)
print(topics[0])

topics[0][(2, True)].append(3)
print(topics[0])


# order topics how the participants retrieved them
def get_topics_in_user_oder(order, topics):
    topics = [x for _, x in sorted(zip(order, topics))]
    return topics


# go back to original order of topics
def get_topics_ordered_back(order, topics):
    #print(order)
    reverse_order = [5-x for x in order]
    #print(reverse_order)
    topics = [x for _, x in sorted(zip(order, topics))]
    #topics.reverse()
    return topics
    # [5-0, 5-5,    5-4,    5-3,  5-2,  5-1]
    # [5,   0,      1,      2,      3,    4]

beginning = [0,1,2,3,4,5]
order = [0,5,4,3,2,1]
after_order_1 = get_topics_in_user_oder(order, beginning)
print(beginning)
print(after_order_1)
after_order_2 = get_topics_in_user_oder(order, after_order_1)
print(after_order_2)
