from mdp import MDP
import collections
import operator


class MixtureModel:

    def __init__(self, path='data', alpha=1, k=3, discount_factor=0.999, verbose=True, save_path="mixture-models"):
        self.k = k
        self.df = discount_factor
        self.alpha = alpha
        self.path = path
        self.verbose = verbose
        self.save_path = save_path

    def generate_model(self):
        for i in range(1, self.k+1):
            mm = MDP(path='data-mini', alpha=self.alpha, k=i,
                     discount_factor=self.df, verbose=self.verbose, save_path=self.save_path)
            mm.initialise_mdp()
            mm.policy_iteration(max_iteration=1000)

    def predict(self, user_id):
        recommendations = []
        for i in range(1, self.k+1):
            mm = MDP(path='data-mini', alpha=self.alpha, k=i,
                     discount_factor=self.df, verbose=False, save_path=self.save_path)
            mm.load_policy("mdp-model_k=" + str(i) + ".pkl")
            recommendations.append(mm.recommend(user_id))

        votes = collections.Counter(recommendations)
        return max(votes.items(), key=operator.itemgetter(1))[0]


if __name__ == '__main__':
    rs = MixtureModel(path='data-mini')
    rs.generate_model()
    print(rs.predict('151603712'))
