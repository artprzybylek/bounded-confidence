import pickle
import re
import matplotlib.pyplot as plt
from numpy import mean
import matplotlib as mp


mp.rcParams['font.size'] = 11


sizes = [100, 200, 500]

networks_results = {
    'Network: complete graph': ['cg_{}'.format(x) for x in sizes],
    'Network: Barabasi-Albert, m=6': ['ba_{}_6'.format(x) for x in sizes],
    'Network: Barabasi-Albert, n=200': ['ba_200_{}'.format(x) for x in [2, 4, 6, 8, 10]],
    'Network: Watts-Strogatz, k=20, p=0.3': ['ws_{}_20_0.3'.format(x) for x in sizes],
    'Network: Watts-Strogatz, n=200, p=0.3': ['ws_200_{}_0.3'.format(x) for x in [10, 20, 30, 40, 50]],
    'Network: Watts-Strogatz, n=200, p=0.2': ['ws_200_{}_0.2'.format(x) for x in [4, 6, 8, 10, 12]],
    'Network: Watts-Strogatz, n=200, k=20': ['ws_200_20_{}'.format(x) for x in [0.1, 0.2, 0.3, 0.4, 0.5]],
    'various': ['cg_200', 'ws_200_4_0.2', 'ws_200_6_0.2', 'ba_200_4', 'ba_200_6']
    }

legends = {
    'Network: complete graph': ['n={}'.format(x) for x in sizes],
    'Network: Barabasi-Albert, m=6': ['n={}'.format(x) for x in sizes],
    'Network: Barabasi-Albert, n=200': ['m={}'.format(x) for x in [2, 4, 6, 8, 10]],
    'Network: Watts-Strogatz, k=20, p=0.3': ['n={}'.format(x) for x in sizes],
    'Network: Watts-Strogatz, n=200, p=0.3': ['k={}'.format(x) for x in [10, 20, 30, 40, 50]],
    'Network: Watts-Strogatz, n=200, p=0.2': ['k={}'.format(x) for x in [4, 6, 8, 10, 12]],
    'Network: Watts-Strogatz, n=200, k=20': ['p={}'.format(x) for x in [0.1, 0.2, 0.3, 0.4, 0.5]],
    'various': ['CG', 'WS: k=4,\n p=0.2', 'WS: k=6,\n p=0.2', 'BA: m=4', 'BA: m=6']
    }

feature_labels = {
    'groups10': 'number of clusters',
    'changes': 'opinions change',
    'order': 'order',
    'steps': 'relaxation time'
    }


def plots1():
    for feature in feature_labels:
        for network in networks_results[:-1]:
            plt.figure()
            if feature in ['final_groups', 'groups10']:
                plt.axis([-0.01, 0.41, 0, 10])
            for res in networks_results[network]:
                file = 'results/{0}_{1}.pkl'.format(feature, res)
                with open(file, "rb") as f:
                    results = pickle.load(f)
                e = sorted(results.keys())
                avg_values = [mean(results[eps]) for eps in e]
                plt.plot(e, avg_values, '.-')
            legend = legends[network]
            if feature in ['changes', 'groups10'] and network == 'Network: Barabasi-Albert, n=200':
                add_cg_plot(feature)
                legend += ['CG']
            plt.legend(legend)
            plt.title(network)
            plt.grid(linestyle='--')
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
        if feature in ['final_groups', 'groups10']:
            plt.axis([-0.01, 0.41, 0, 10])
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
        plt.grid(linestyle='--')
        plt.title('n=200')
        file = 'plots/{0}_various.pdf'.format(feature)
        plt.savefig(file)


def plot_steps_changes():
    feature = 'steps_changes'
    mp.rcParams['figure.dpi'] = 150.0
    for net in networks_results:
        fig, axarr = plt.subplots(2, 2, sharey='row')
        for num, res in enumerate(networks_results[net]):
            file = 'results/{0}_{1}.pkl'.format(feature, res)
            with open(file, "rb") as f:
                results = pickle.load(f)
            e = sorted(results.keys())
            for index in range(4):
                eps = e[index]
                num_of_simulations = len(results[eps])
                max_steps = max([len(changes) for changes in results[eps]])
                avg_time_changes = {t: 0 for t in range(max_steps)}
                for changes in results[eps]:
                    for t, change in enumerate(changes):
                        avg_time_changes[t] += change
                for t in avg_time_changes:
                    avg_time_changes[t] /= num_of_simulations
                time_space = sorted(avg_time_changes.keys())
                values = [avg_time_changes[t] for t in time_space]
                time_space, values = cut_time_and_values(time_space, values)
                if index == 0:
                    axarr[index // 2, index % 2].plot(time_space, values, '.-', label=legends[net][num])
                else:
                    axarr[index // 2, index % 2].plot(time_space, values, '.-')
                axarr[index // 2, index % 2].set_title(r'$\epsilon={}$'.format(eps))
        for index in range(4):
            axarr[index // 2, index % 2].grid(linestyle='--')
        for ax in axarr.flat:
            ax.set(xlabel='time', ylabel='opinions changes')
        for ax in axarr.flat:
            ax.label_outer()
        fig.legend(legends[net])
        # fig.tight_layout()
        # fig.subplots_adjust(right=0.75)
        file_core = re.sub('(Network:)|\s', '', net)
        file = 'plots/{0}_{1}.pdf'.format(feature, re.sub('[,.]', '_', file_core))
        plt.savefig(file)


def cut_time_and_values(time_space, values, min_change=0.001):
    max_index = max(index for index in range(len(values)) if values[index] >= min_change)
    time_space = time_space[:max_index]
    values = values[:max_index]
    return time_space, values


def plot_ws_pairs():
    mp.rcParams['figure.dpi'] = 150.0
    for feature in feature_labels:
        plt.figure()
        for i, network in enumerate(['Network: Watts-Strogatz, n=200, p=0.2', 'Network: Watts-Strogatz, n=200, p=0.3']):
            for res in networks_results[network]:
                file = 'results/{0}_{1}.pkl'.format(feature, res)
                with open(file, "rb") as f:
                    results = pickle.load(f)
                e = sorted(results.keys())
                avg_values = [mean(results[eps]) for eps in e]
                plt.subplot(211 + i)
                if feature in ['final_groups', 'groups10']:
                    plt.axis([-0.01, 0.41, 0, 10])
                plt.plot(e, avg_values, '.-')
            plt.grid(linestyle='--')
            if i == 1:
                plt.xlabel('confidence level')
                add_cg_plot(feature)
            plt.legend(legends[network] + ['CG'], loc='right')
            if i == 0:
                plt.title(network)
            plt.ylabel(feature_labels[feature])
        file = 'plots/pairs_{0}_ws.pdf'.format(feature)
        plt.savefig(file)


def add_cg_plot(feature):
    file = 'results/{0}_cg_200.pkl'.format(feature)
    with open(file, "rb") as f:
        results = pickle.load(f)
    e = sorted(results.keys())
    avg_values = [mean(results[eps]) for eps in e]
    plt.plot(e, avg_values, '.-')


if __name__ == "__main__":
    # plots1()
    plots2()
    # plot_steps_changes()
    # plot_ws_pairs()
