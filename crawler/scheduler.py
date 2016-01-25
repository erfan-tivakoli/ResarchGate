__author__ = 'Rfun'
import queue
from pprint import pprint


class Scheduler():
    def __init__(self):
        self.history = set({})
        initial_articles_url = [
            "https://www.researchgate.net/publication/285458515_A_General_Framework_for_Constrained_Bayesian_Optimization_using_Information-based_Search",
            "https://www.researchgate.net/publication/284579255_Parallel_Predictive_Entropy_Search_for_Batch_Global_Optimization_of_Expensive_Objective_Functions",
            "https://www.researchgate.net/publication/283658712_Sandwiching_the_marginal_likelihood_using_bidirectional_Monte_Carlo",
            "https://www.researchgate.net/publication/281895707_Dirichlet_Fragmentation_Processes",
            "https://www.researchgate.net/publication/273488773_Variational_Infinite_Hidden_Conditional_Random_Fields",
            "https://www.researchgate.net/publication/279848500_mcclustext-manual",
            "https://www.researchgate.net/publication/279848498_mcclustext_10tar",
            "https://www.researchgate.net/publication/279633530_Subsampling-Based_Approximate_Monte_Carlo_for_Discrete_Distributions",
            "https://www.researchgate.net/publication/279309917_An_Empirical_Study_of_Stochastic_Variational_Algorithms_for_the_Beta_Bernoulli_Process",
            "https://www.researchgate.net/publication/278332447_MCMC_for_Variationally_Sparse_Gaussian_Processes"]

        self.q = queue.Queue(maxsize=0)
        for link in initial_articles_url:
            self.q.put(link)
            self.history.add(link)

    def check_duplication(self, new_url):
        if new_url in self.history:
            print('the link %s is duplicated' % (new_url))
            return True
        return False

    def add(self, new_url):
        if not self.check_duplication(new_url):
            self.q.put(new_url)
            self.history.add(new_url)


def main():
    a = Scheduler()


if __name__ == '__main__':
    main()