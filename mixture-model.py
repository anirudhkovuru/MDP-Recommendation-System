from mdp import MDP
import collections


class MixtureModel:
    """
    Class to implement mixture models of multiple MDPs.
    """

    def __init__(self, path='data', alpha=1, k=3, discount_factor=0.999, verbose=True, save_path="mixture-models"):
        """
        The constructor for the MixtureModel class.
        :param path: path to data
        :param alpha: the proportionality constant when considering transitions
        :param k: the number of models
        :param discount_factor: the discount factor for each MDP
        :param verbose:flag to show steps
        :param save_path: the path to which models should be saved and loaded from
        """

        self.k = k
        self.df = discount_factor
        self.alpha = alpha
        self.path = path
        self.verbose = verbose
        self.save_path = save_path

    def generate_model(self):
        """
        Method to generate and save the various models.
        :return: None
        """

        # Generate models whose n-gram values change from 1...k
        for i in range(1, self.k+1):
            # Initialise the MDP
            mm = MDP(path='data-mini', alpha=self.alpha, k=i,
                     discount_factor=self.df, verbose=self.verbose, save_path=self.save_path)
            mm.initialise_mdp()
            # Run the policy iteration and save the model
            mm.policy_iteration(max_iteration=1000)

    def predict(self, user_id):
        """
        Method  to provide recommendations.
        :param user_id: the id of the user
        :return: an ordered dictionary with the recommendations and their corresponding votes
        """

        recommendations = []
        for i in range(1, self.k+1):
            # Initialise each MDP
            mm = MDP(path='data-mini', alpha=self.alpha, k=i,
                     discount_factor=self.df, verbose=False, save_path=self.save_path)
            # Load its corresponding policy
            mm.load_policy("mdp-model_k=" + str(i) + ".pkl")
            # Append the recommendation into the list
            recommendations.append(mm.recommend(user_id))

        # Count the votes given by each model with equal weight
        votes = collections.Counter(recommendations)
        return collections.OrderedDict(sorted(votes.items(), key=lambda x: x[1], reverse=True))


if __name__ == '__main__':
    rs = MixtureModel(path='data-mini', k=4)
    rs.generate_model()
    print(rs.predict('151603712'))
