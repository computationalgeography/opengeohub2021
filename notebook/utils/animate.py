import sys
import warnings

from matplotlib import animation
from matplotlib import colors as cls
from matplotlib import pyplot as plt
from matplotlib import colorbar as cb
from matplotlib import cm as cm
import matplotlib
import numpy as np

from IPython.display import display, Image, HTML

import lue.data_model as ldm
import campo


warnings.filterwarnings("ignore", category=matplotlib.MatplotlibDeprecationWarning)


def animate(show_notebook=True):

    # import data
    dataset = ldm.open_dataset('daisy_world.lue')
    field_dataframe = campo.dataframe.select(dataset.climate, property_names=[\
        'temperature'])
    daisy_dataframe = campo.dataframe.select(dataset.daisies, property_names=[\
        'age', 'mask', 'breed'])
    x_coords = daisy_dataframe['daisies']['site']['breed']['coordinates'][:,0].data
    y_coords = daisy_dataframe['daisies']['site']['breed']['coordinates'][:,1].data


    nr_timesteps = field_dataframe['climate']['surface']['temperature'][0].shape[0]

    field_property = field_dataframe['climate']['surface']['temperature']

    # get metadata
    cellsize = 10
    minx = field_property[0].xcoord[0].data
    miny = field_property[0].ycoord[0].data
    maxx = field_property[0].xcoord[-1].data + cellsize
    maxy = field_property[0].ycoord[-1].data + cellsize
    extent = (minx, maxx, miny, maxy)


    #########

    # create the figure
    f = plt.figure()
    # [left, bottom, width, height]
    ax1 = f.add_axes([0.8, 0.05, 0.1, 0.9])
    ax2 = f.add_axes([0.05, 0.05, 0.7, 0.9])
    plt.axis('off')

    # making normalization scheme between -30 and 80 degrees Celcius
    norm = cls.Normalize(vmin=-30, vmax=80)
    cmap = cm.coolwarm
    # and corresponding legend
    leg = cb.ColorbarBase(ax1, cmap=cmap, norm=norm, orientation='vertical')
    leg.set_label('Temperature (degrees Celcius)')

    # no agent colour receives full transparency
    ##acmap = cm.get_cmap("binary").copy()  # DID NOT WORK FOR ME (MY MPL VERSION?)
    acmap = cm.binary
    acmap.set_under('green',alpha=0.0)

    # use imshow to plot the field over time
    # and scatter to plot the agents
    def init():
        # temperature field
        field_values = field_dataframe['climate']['surface']['temperature'][0][0].data
        im = ax2.imshow(field_values, norm=norm, \
                        extent=extent, cmap=cmap, animated=True)

        # daisies, mask the alives
        agent_values = daisy_dataframe['daisies']['site']['breed']['values'][:,0]
        agent_active = daisy_dataframe['daisies']['site']['mask']['values'][:,0]
        agent_values = np.where(agent_active==1,agent_values,-99)
        agents = ax2.scatter(x_coords, y_coords, marker='o', c=agent_values,\
                              s=50, cmap=acmap, vmin=0, vmax=1, animated=True)

        # time label
        month = ax2.text(0.02, 0.975, 'step = 0', transform=ax2.transAxes, fontsize=10)
        return im, agents, month

    def animate_ts(i):
        ax2.clear()
        ax2.axis('off')

        # temperature field
        field_values = field_dataframe['climate']['surface']['temperature'][0][i].data
        im = ax2.imshow(field_values, norm=norm, \
                        extent=extent, cmap=cmap, animated=True)

        # daisies, mask the alives
        agent_values = daisy_dataframe['daisies']['site']['breed']['values'][:,i]
        agent_active = daisy_dataframe['daisies']['site']['mask']['values'][:,i]
        agent_values = np.where(agent_active==1,agent_values,-99)

        agents = ax2.scatter(x_coords, y_coords, marker='o', c=agent_values,\
                              s=50, cmap=acmap, vmin=0, vmax=1, animated=True)

        # time label
        month = ax2.text(0.02, 0.975, f'step = {i+1}', transform=ax2.transAxes, fontsize=10)

        return im, agents, month

    im_ani = animation.FuncAnimation(f, animate_ts, interval=75, \
                                      blit=True, frames = nr_timesteps,\
                                      init_func=init)
    #im_ani.save('im.mp4', dpi=100,  metadata={'artist':'Judith Verstegen'})

    if show_notebook:
        plt.close(im_ani._fig)
        return HTML(im_ani.to_html5_video())
    else:
        plt.show()



if __name__ == '__main__':
    animate(False)
