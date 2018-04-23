import pickle
import re
import matplotlib.pyplot as plt
from numpy import mean
import matplotlib as mp


mp.rcParams['font.size'] = 15


sizes = [100, 200, 500]

networks_results = {
    'Network: complete graph': ['cg_{}'.format(x) for x in sizes],
    'Network: Barabasi-Albert, m=6': ['ba_{}_6'.format(x) for x in sizes],
    'Network: Barabasi-Albert, n=200': ['ba_200_{}'.format(x) for x in [2, 4, 6, 8, 10]],
    'Network: Watts-Strogatz, k=20, p=0.3': ['ws_{}_20_0.3'.format(x) for x in sizes],
    'Network: Watts-Strogatz, n=200, p=0.3': ['ws_200_{}_0.3'.format(x) for x in [10, 20, 30, 40, 50]],
    'Network: Watts-Strogatz, n=200, k=20': ['ws_200_20_{}'.format(x) for x in [0.1, 0.2, 0.3, 0.4, 0.5]]
    }

legends = {
    'Network: complete graph': ['n={}'.format(x) for x in sizes],
    'Network: Barabasi-Albert, m=6': ['n={}'.format(x) for x in sizes],
    'Network: Barabasi-Albert, n=200': ['m={}'.format(x) for x in [2, 4, 6, 8, 10]],
    'Network: Watts-Strogatz, k=20, p=0.3': ['n={}'.format(x) for x in sizes],
    'Network: Watts-Strogatz, n=200, p=0.3': ['k={}'.format(x) for x in [10, 20, 30, 40, 50]],
    'Network: Watts-Strogatz, n=200, k=20': ['p={}'.format(x) for x in [0.1, 0.2, 0.3, 0.4, 0.5]]
    }

feature_labels = {
    'groups10': 'number of clusters',
    'changes': 'opinions change',
    'final_groups': 'number of clusters',
    'order': 'order',
    'steps': 'relaxation time'
    }


def plots1():
    for feature in feature_labels:
        for network in networks_results:
            plt.figure()
            if feature in ['final_groups', 'groups10']:
                plt.axis([-0.01, 0.41, 0, 20])
            for res in networks_results[network]:
                file = 'results/{0}_{1}.pkl'.format(feature, res)
                with open(file, "rb") as f:
                    results = pickle.load(f)
                e = sorted(results.keys())
                avg_values = [mean(results[eps]) for eps in e]
                plt.plot(e, avg_values, '.-')
            plt.legend(legends[network])
            plt.title(network)
            plt.xlabel('confidence level')
            plt.ylabel(feature_labels[feature])
            file_core = re.sub('(Network:)|\s', '', network)
            file = 'plots/{0}_{1}.pdf'.format(feature, re.sub('[,.]', '_', file_core))
            plt.savefig(file)


def plots2():
    nets = ['cg_200', 'ws_200_4_0.2', 'ws_200_6_0.2', 'ba_200_4', 'ba_200_6']
    legend = ['CG', 'WS: k=4, p=0.2', 'WS: k=6, p=0.2', 'BA: m=4', 'BA: m=6']
    for feature in feature_labels:
        plt.figure()
        mp.rcParams['font.size'] = 15
        if feature in ['final_groups', 'groups10']:
            plt.axis([-0.01, 0.41, 0, 20])
        for res in nets:
            file = 'results/{0}_{1}.pkl'.format(feature, res)
            with open(file, "rb") as f:
                results = pickle.load(f)
            e = sorted(results.keys())
            avg_values = [mean(results[eps]) for eps in e]
            plt.plot(e, avg_values, '.-')
        plt.legend(legend)
        plt.xlabel('confidence level')
        plt.ylabel(feature_labels[feature])
        plt.title('n=200')
        file = 'plots/{0}_various.pdf'.format(feature)
        plt.savefig(file)


if __name__ == "__main__":
    plots1()
    plots2()
