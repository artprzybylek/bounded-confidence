import pickle
import matplotlib.pyplot as plt
import matplotlib as mp


mp.rcParams['font.size'] = 15


def plot_cg_compare(num_of_agents, legend, style='*-'):
    legend.append('CG')
    filename = 'cg_' + num_of_agents + '.pkl'
    with open(filename, 'rb') as f:
        consensus_frequencies = pickle.load(f)
    results = sorted(consensus_frequencies.items(), key=lambda x: x[0])
    results_eps = [x[0] for x in results]
    results_values = [x[1] for x in results]
    plt.plot(results_eps, results_values, style)


def plot_cg():
    output_path = 'plots/'
    network = 'cg'
    plt.figure()
    for num_of_agents in ['100', '200', '500']:
        filename = network + '_' + num_of_agents + '.pkl'
        with open(filename, 'rb') as f:
            consensus_frequencies = pickle.load(f)
        results = sorted(consensus_frequencies.items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    legend = list('n=' + str(n) for n in ['100', '200', '500'])
    plt.legend(legend)
    plt.title('Network: complete graph')
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}.pdf'.format(output_path, network)
    plt.savefig(output_file)


def plot_ws_changing_k():
    output_path = 'plots/'
    network = 'ws'
    num_of_agents = '200'
    p = '0.3'
    filename = network + '_' + num_of_agents + '_' + p + '.pkl'
    with open(filename, 'rb') as f:
        consensus_frequencies = pickle.load(f)
    plt.figure()
    for arg in consensus_frequencies:
        results = sorted(consensus_frequencies[arg].items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    legend = list('k='+str(k) for k in consensus_frequencies.keys())
    plot_cg_compare(num_of_agents, legend)
    plt.legend(legend)
    plt.title('Network: Watts-Strogatz, n={0}, p={1}'.format(num_of_agents, p))
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}_{2}_p={3}.pdf'.format(output_path, network, num_of_agents,
                                                               str(p).replace('.', ','))
    plt.savefig(output_file)


def plot_ws_changing_num():
    output_path = 'plots/'
    network = 'ws'
    num_of_agents = '200'
    p = '0.3'
    filename = network + '_' + num_of_agents + '_' + p + '.pkl'
    with open(filename, 'rb') as f:
        consensus_frequencies = pickle.load(f)
    plt.figure()
    for arg in consensus_frequencies:
        results = sorted(consensus_frequencies[arg].items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    legend = list('k='+str(k) for k in consensus_frequencies.keys())
    plot_cg_compare(num_of_agents, legend)
    plt.legend(legend)
    plt.title('Network: Watts-Strogatz, n={0}, p={1}'.format(num_of_agents, p))
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}_{2}_p={3}.pdf'.format(output_path, network, num_of_agents,
                                                               str(p).replace('.', ','))
    plt.savefig(output_file)


def plot_ws_changing_p():
    output_path = 'plots/'
    network = 'ws'
    num_of_agents = '200'
    k = 20
    plt.figure()
    for p in ['0.1', '0.2', '0.3', '0.4', '0.5']:
        filename = network + '_' + num_of_agents + '_' + p + '.pkl'
        with open(filename, 'rb') as f:
            consensus_frequencies = pickle.load(f)
        results = sorted(consensus_frequencies[k].items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    legend = list('p=' + p for p in ['0.1', '0.2', '0.3', '0.4', '0.5'])
    # plot_cg_compare(num_of_agents, legend)
    plt.legend(legend)
    plt.title('Network: Watts-Strogatz, n={0}, k={1}'.format(num_of_agents, k))
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}_{2}_k={3}.pdf'.format(output_path, network, num_of_agents, k)
    plt.savefig(output_file)


def plot_ws_changing_n():
    output_path = 'plots/'
    network = 'ws'
    p = '0.3'
    k = 30
    plt.figure()
    for num_of_agents in ['100', '200', '500']:
        filename = network + '_' + num_of_agents + '_' + p + '.pkl'
        with open(filename, 'rb') as f:
            consensus_frequencies = pickle.load(f)
        results = sorted(consensus_frequencies[k].items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    plt.legend(list('n=' + n for n in ['100', '200', '500']))
    plt.title('Network: Watts-Strogatz, k={0}, p={1}'.format(k, p))
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}_k={2}_p={3}.pdf'.format(output_path, network, k, str(p).replace('.', ','))
    plt.savefig(output_file)


def plot_ba_changing_m():
    output_path = 'plots/'
    network = 'ba'
    num_of_agents = '200'
    plt.figure()
    filename = network + '_' + num_of_agents + '.pkl'
    with open(filename, 'rb') as f:
        consensus_frequencies = pickle.load(f)
    for arg in consensus_frequencies:
        results = sorted(consensus_frequencies[arg].items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    legend = list('m='+str(m) for m in consensus_frequencies.keys())
    plot_cg_compare(num_of_agents, legend)
    plt.legend(legend)
    plt.title('Network: Barabasi-Albert, n={0}'.format(num_of_agents))
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}_{2}.pdf'.format(output_path, network, num_of_agents)
    plt.savefig(output_file)


def plot_ba_changing_n():
    output_path = 'plots/'
    network = 'ba'
    m = 6
    plt.figure()
    for num_of_agents in ['100', '200', '500']:
        filename = network + '_' + num_of_agents + '.pkl'
        with open(filename, 'rb') as f:
            consensus_frequencies = pickle.load(f)
        results = sorted(consensus_frequencies[m].items(), key=lambda x: x[0])
        results_eps = [x[0] for x in results]
        results_values = [x[1] for x in results]
        plt.plot(results_eps, results_values, '.-')
    plt.legend(list('n='+n for n in ['100', '200', '500']))
    plt.title('Network: Barabasi-Albert, m={0}'.format(m))
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    output_file = '{0}freq_consensus_{1}_m={2}.pdf'.format(output_path, network, m)
    plt.savefig(output_file)


def help_plot(filename, k):
    with open(filename, 'rb') as f:
        consensus_frequencies = pickle.load(f)
    results = sorted(consensus_frequencies[k].items(), key=lambda x: x[0])
    results_eps = [x[0] for x in results]
    results_values = [x[1] for x in results]
    plt.plot(results_eps, results_values, '.-')


def plot_comparison():
    output_path = 'plots/'
    plt.figure()
    files_v = [('1_ws_200_0.2.pkl', 4),
               ('1_ws_200_0.2.pkl', 6),
               ('ba_200.pkl', 4),
               ('ba_200.pkl', 6)]
    legend = []
    plot_cg_compare('200', legend, style='.-')
    for f, v in files_v:
        help_plot(f, v)
    legend = ['CG', 'WS: k=4, p=0.2', 'WS: k=6, p=0.2', 'BA: m=4', 'BA: m=6']
    plt.legend(legend)
    plt.xlabel('confidence level')
    plt.ylabel('frequency')
    plt.title('n=200')
    output_file = '{0}freq_consensus_compare.pdf'.format(output_path)
    plt.savefig(output_file)


if __name__ == "__main__":
    plot_comparison()
    plot_cg()
    plot_ws_changing_k()
    plot_ws_changing_p()
    plot_ws_changing_n()
    plot_ba_changing_m()
    plot_ba_changing_n()
