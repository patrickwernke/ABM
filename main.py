from model import DuckModel, FemaleDuckAgent, MaleDuckAgent
import matplotlib.pyplot as plt

def plot_ducks(plot_m, plot_f, model, pause=0.01):
    x_m = []
    y_m = []
    x_f = []
    y_f = []
    for agent in model.schedule.agents:
        if isinstance(agent, FemaleDuckAgent):
            x_f.append(agent.pos[0])
            y_f.append(agent.pos[1])
        else:
            x_m.append(agent.pos[0])
            y_m.append(agent.pos[1])

    plot_m.set_ydata(y_m)
    plot_m.set_xdata(x_m)
    plot_f.set_ydata(y_f)
    plot_f.set_xdata(x_f)

    plt.draw()
    plt.pause(pause)

if __name__ == '__main__':
    model = DuckModel(10, 10, 100, 100)

    plt.ion()
    fig=plt.figure()
    ax=fig.add_subplot(111)

    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    plot_m, = ax.plot([], [], 'o', color='b')
    plot_f, = ax.plot([], [], 'o', color='r')
    plt.show()
    plot_ducks(plot_m, plot_f, model, 0.05)
    for i in range(200):
        model.step()
        plot_ducks(plot_m, plot_f, model, 0.05)
