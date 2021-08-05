import numpy
import matplotlib.pyplot as plt

import lue.data_model as ldm
import campo


def plot_temperature():
    dataset = ldm.open_dataset('daisy_world.lue')
    init_properties = campo.dataframe.select(dataset.area, property_names=['init_temp'])
    properties = campo.dataframe.select(dataset.area, property_names=[ 'temperature'])

    t_init = init_properties['area']['extent']['init_temp'][0].data
    t_init_mean = numpy.mean(t_init)

    values = properties['area']['extent']['temperature'][0].data

    nr_timesteps = values.shape[0]

    avg_temp = numpy.zeros(nr_timesteps + 1)

    avg_temp[0] = t_init_mean

    for ts in range(0, nr_timesteps):
      avg_temp[ts + 1] = numpy.mean(values[ts])

    plt.plot(avg_temp)
    plt.ylabel('Temperature (degrees Celcius)')
    plt.xlabel('Time step')
    plt.show()


if __name__ == '__main__':
  plot_temperature()
