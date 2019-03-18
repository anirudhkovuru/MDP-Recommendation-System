import operator
import pickle
import os

from mdp_handler import MDPInitializer


class MDP:
    """
    Class to run the MDP.
    """

    def __init__(self, path='data', alpha=1, k=3, discount_factor=0.999, verbose=True, save_path="saved-models"):
        """
        The constructor for the MDP class.
        :param path: path to data
        :param alpha: the proportionality constant when considering transitions
        :param k: the number of items in each state
        :param discount_factor: the discount factor for the MDP
        :param verbose: flag to show steps
        :param save_path: the path to which models should be saved and loaded from
        """

        # Initialize the MDPInitializer
        self.mdp_i = MDPInitializer(path, k, alpha)
        self.df = discount_factor
        self.verbose = verbose
        self.save_path = save_path
        # The set of states
        self.S = {}
        # The set of state values
        self.V = {}
        # The set of actions
        self.A = []
        # The set of transitions
        self.T = {}
        # The policy of the MDP
        self.policy = {}

    def print_progress(self, message):
        if self.verbose:
            print(message)

    def initialise_mdp(self):
        """
        The method to initialise the MDP.
        :return: None
        """

        # Initialising the actions
        self.print_progress("Getting set of actions.")
        self.A = self.mdp_i.actions
        self.print_progress("Set of actions obtained.")

        # Initialising the states, state values, policy
        self.print_progress("Getting states, state-values, policy.")
        self.S, self.V, self.policy = self.mdp_i.generate_initial_states()
        self.print_progress("States, state-values, policy obtained.")

        # Initialise the transition table
        self.print_progress("Getting transition table.")
        self.T = self.mdp_i.generate_transitions(self.S, self.A)
        self.print_progress("Transition table obtained.")

    def one_step_lookahead(self, state):
        """
        Helper function to calculate state-value function.
        :param state: state to consider
        :return: action values for that state
        """

        # Initialise the action values and set to 0
        action_values = {}
        for action in self.A:
            action_values[action] = 0

        # Calculate the action values for each action
        for action in self.A:
            for next_state, P_and_R in self.T[state][action].items():
                if next_state not in self.V:
                    self.V[next_state] = 0
                # action_value +=  probability * (reward + (discount * next_state_value))
                action_values[action] += P_and_R[0] * (P_and_R[1] + (self.df * self.V[next_state]))

        return action_values

    def update_policy(self):
        """
        Helper function to update the policy based on the value function.
        :return: None
        """

        for state in self.S:
            action_values = self.one_step_lookahead(state)

            # The action with the highest action value is chosen
            self.policy[state] = max(action_values.items(), key=operator.itemgetter(1))[0]

    def policy_eval(self):
        """
        Helper function to evaluate a policy
        :return: estimated value of each state following the policy and state-value
        """

        # Initialise the policy values
        policy_value = {}
        for state in self.policy:
            policy_value[state] = 0

        # Find the policy value for each state and its respective action dictated by the policy
        for state, action in self.policy.items():
            for next_state, P_and_R in self.T[state][action].items():
                if next_state not in self.V:
                    self.V[next_state] = 0
                # policy_value +=  probability * (reward + (discount * next_state_value))
                policy_value[state] += P_and_R[0] * (P_and_R[1] + (self.df * self.V[next_state]))

        return policy_value

    def compare_policy(self, policy_prev):
        """
        Helper function to compare the given policy with the current policy
        :param policy_prev: the policy to compare with
        :return: a boolean indicating if the policies are different or not
        """

        for state in policy_prev:
            # If the policy does not match even once then return False
            if policy_prev[state] != self.policy[state]:
                return False
        return True

    def policy_iteration(self, max_iteration=1000, start_where_left_off=False, to_save=True):
        """
        Algorithm to solve the MDP
        :param max_iteration: maximum number of iterations to run.
        :param start_where_left_off: flag to load a previous model(set False if not and filename otherwise)
        :param to_save: flag to save the current model
        :return: None
        """

        # Load a previous model
        if start_where_left_off:
            self.load_policy(start_where_left_off)

        # Start the policy iteration
        policy_prev = self.policy.copy()
        for i in range(max_iteration):
            self.print_progress("Iteration" + str(i) + ":")

            # Evaluate given policy
            self.V = self.policy_eval()

            # Improve policy
            self.update_policy()

            # If the policy not changed over 10 iterations it converged
            if i % 10 == 0:
                if self.compare_policy(policy_prev):
                    self.print_progress("Policy converged at iteration " + str(i+1))
                    break
                policy_prev = self.policy.copy()

        # Save the model
        if to_save:
            self.save_policy("mdp-model_k=" + str(self.mdp_i.k) + ".pkl")

    def save_policy(self, filename):
        """
        Method to save the trained model
        :param filename: the filename it should be saved as
        :return: None
        """

        self.print_progress("Saving model to " + filename)
        os.makedirs(self.save_path, exist_ok=True)
        with open(self.save_path + "/" + filename, 'wb') as f:
            pickle.dump(self.policy, f, pickle.HIGHEST_PROTOCOL)

    def load_policy(self, filename):
        """
        Method to load a previous policy
        :param filename: the filename from which the model should be extracted
        :return: None
        """

        self.print_progress("Loading model from " + filename)
        try:
            with open(self.save_path + "/" + filename, 'rb') as f:
                self.policy = pickle.load(f)
        except Exception as e:
            print(e)

    def recommend(self, user_id):
        """
        Method to provide recommendation to the user
        :param user_id: the user_id of a given user
        :return: the game that is recommended
        """

        self.print_progress("Recommending for " + str(user_id))
        pre = []
        for i in range(self.mdp_i.k - 1):
            pre.append(None)
        games = pre + self.mdp_i.transactions[user_id]

        user_state = ()
        for i in range(len(games) - self.mdp_i.k, len(games)):
            user_state = user_state + (games[i],)

        return self.mdp_i.games[self.policy[user_state]]


# if __name__ == '__main__':
#     rs = MDP(path='data-mini')
#     rs.initialise_mdp()
#     rs.policy_iteration(max_iteration=1000)
#     for user in rs.mdp_i.transactions:
#         print(rs.recommend(user))
