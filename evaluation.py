from mdp import MDP
import matplotlib.pyplot as plt


def evaluate_decay_score(alpha=10, k=3, path='data-mini', random_policy=False):
    """
    Function to evaluate the given MDP using exponential decay score
    :param alpha: a parameter in exponential decay score
    :param k: the number of items in a state
    :param path: data path
    :param random_policy: if the policy is to be random
    :return: the average score
    """

    rs = MDP(path=path, k=k)
    if random_policy:
        rs.initialise_mdp()
    else:
        rs.load("mdp-model_k=" + str(k) + ".pkl")
    transactions = rs.mdp_i.transactions.copy()

    user_count = 0
    total_score = 0
    # Generating a testing for each test case
    for user in transactions:
        total_list = len(transactions[user])
        if total_list == 1:
            continue

        score = 0
        for i in range(1, total_list):
            rs.mdp_i.transactions[user] = transactions[user][:i]

            rec_list = rs.recommend(user)
            rec_list = [rec[0] for rec in rec_list]
            m = rec_list.index(rs.mdp_i.games[transactions[user][i]]) + 1
            score += 2 ** ((1 - m) / (alpha - 1))

        score /= (total_list - 1)
        total_score += 100 * score
        user_count += 1

    return total_score / user_count


def evaluate_recommendation_score(m=10, k=3, path='data-mini', random_policy=False):
    """
    Function to evaluate the given MDP using exponential decay score
    :param m: a parameter in recommendation score score
    :param k: the number of items in a state
    :param path: data path
    :param random_policy: if the policy is to be random
    :return: the average score
    """

    rs = MDP(path=path, k=k)
    if random_policy:
        rs.initialise_mdp()
    else:
        rs.load("mdp-model_k=" + str(k) + ".pkl")
    transactions = rs.mdp_i.transactions.copy()

    user_count = 0
    total_score = 0
    # Generating a testing for each test case
    for user in transactions:
        total_list = len(transactions[user])
        if total_list == 1:
            continue

        item_count = 0
        for i in range(1, total_list):
            rs.mdp_i.transactions[user] = transactions[user][:i]

            rec_list = rs.recommend(user)
            rec_list = [rec[0] for rec in rec_list]
            rank = rec_list.index(rs.mdp_i.games[transactions[user][i]]) + 1
            if rank <= m:
                item_count += 1

        score = item_count / (total_list - 1)
        total_score += 100 * score
        user_count += 1

    return total_score / user_count


def graph_recommendation_score(scale, m, with_comparison):
    """
    Function to generate a graph for the recommendation score over a range of k
    :param scale: the limit to which k should vary
    :param m: a parameter in recommendation score computation
    :param with_comparison: plot a random policy's graph
    :return: None
    """

    fig = plt.figure()
    x = [i + 1 for i in range(scale)]
    y_recommendation = []
    for i in x:
        y_recommendation.append(evaluate_recommendation_score(m=m, k=i))

    plt.plot(x, y_recommendation, color=(0.2, 0.4, 0.6, 0.6), label="Our model, For m=" + str(m))
    plt.scatter(x, y_recommendation)

    plt.xticks(x)
    plt.yticks([i for i in range(40, 100, 10)])

    for x1, y in zip(x, y_recommendation):
        text = '%.2f' % y
        plt.text(x1, y, text)

    if with_comparison:
        y_recommendation_rand = []
        for i in x:
            y_recommendation_rand.append(evaluate_recommendation_score(m=m, k=i, random_policy=True))

        plt.plot(x, y_recommendation_rand, color=(0.2, 0.8, 0.6, 0.6), label="Random model, For m=" + str(m))
        plt.scatter(x, y_recommendation_rand)

        plt.xticks(x)
        plt.yticks([i for i in range(40, 100, 10)])

        for x1, y in zip(x, y_recommendation_rand):
            text = '%.2f' % y
            plt.text(x1, y, text)

    fig.suptitle('Recommendation Score vs Number of items in each state')
    plt.xlabel('K')
    plt.ylabel('Score')
    plt.legend()
    plt.show()


def graph_decay_score(scale, rand=False):
    """
    Function to generate a graph for the exponential decay score over a range of k
    :param scale: the limit to which k should vary
    :param rand: to use a random policy or not
    :return: None
    """

    fig = plt.figure()
    x = [i + 1 for i in range(scale)]
    y_decay = []
    for i in x:
        y_decay.append(evaluate_decay_score(k=i, random_policy=rand))

    plt.bar(x, y_decay, width=0.5, color=(0.2, 0.4, 0.6, 0.6))
    xlocs = [i + 1 for i in range(0, 10)]
    for i, v in enumerate(y_decay):
        plt.text(xlocs[i] - 0.46, v + 0.9, '%.2f' % v)

    plt.xticks(x)
    plt.yticks([i for i in range(0, 100, 10)])

    fig.suptitle('Avg Exponential Decay Score vs Number of items in each state')
    plt.xlabel('K')
    plt.ylabel('Score')
    plt.show()


# if __name__ == "__main__":
#     graph_decay_score(10, rand=True)
#     # graph_recommendation_score(10, 10, True)
