from mdp import MDP
import matplotlib.pyplot as plt


def graph_recommendation_score(scale=10, m=10, with_comparison=False):
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
    y_recommendation_rand = []
    for i in x:
        rs = MDP(path='data-mini', k=i)

        if with_comparison:
            rs.initialise_mdp()
            y_recommendation_rand.append(rs.evaluate_recommendation_score(m=m))

        rs.load('mdp-model_k=' + str(i) + '.pkl')
        y_recommendation.append(rs.evaluate_recommendation_score(m=m))

    plt.plot(x, y_recommendation, color=(0.2, 0.4, 0.6, 0.6), label="Our model, For m=" + str(m))
    plt.scatter(x, y_recommendation)

    if with_comparison:
        plt.plot(x, y_recommendation_rand, color=(0.2, 0.8, 0.6, 0.6), label="Random model, For m=" + str(m))
        plt.scatter(x, y_recommendation_rand)

    plt.xticks(x)
    plt.yticks([i for i in range(40, 100, 10)])

    for x1, y in zip(x, y_recommendation):
        text = '%.2f' % y
        plt.text(x1, y, text)

    if with_comparison:
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
        rs = MDP(path='data-mini', k=i)

        if rand:
            rs.initialise_mdp()
            y_decay.append(rs.evaluate_decay_score())
            continue

        rs.load('mdp-model_k=' + str(i) + '.pkl')
        y_decay.append(rs.evaluate_decay_score())

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


if __name__ == "__main__":
    graph_decay_score(10, rand=False)
    graph_decay_score(10, rand=True)
    graph_recommendation_score(scale=10, m=10, with_comparison=True)
