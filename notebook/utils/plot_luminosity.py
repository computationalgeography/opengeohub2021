import matplotlib.pyplot as plt

import lue.data_model as ldm
import campo

def plot_luminosity():
    dataset = ldm.open_dataset('daisy_world.lue')
    prop = campo.dataframe.select(dataset.climate, property_names=['solar_luminosity'])

    values = prop['climate']['surface']['solar_luminosity'][0].data[:,0,0]

    plt.plot(values)
    plt.ylabel('Solar luminosity (-)')
    plt.xlabel('Time step')
    plt.show()


if __name__ == '__main__':
  plot_luminosity()
