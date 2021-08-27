import numpy

import matplotlib.pyplot as plt

import lue.data_model as ldm
import campo

def plot_population():
    dataset = ldm.open_dataset('daisy_world.lue')

    daisy_dataframe = campo.dataframe.select(dataset.daisies, property_names=['mask', 'breed'])

    breed = daisy_dataframe['daisies']['site']['breed']['values']
    mask = daisy_dataframe['daisies']['site']['mask']['values']

    nr_timesteps = breed.shape[1]
    nr_agents = breed.shape[0]

    daisy_b = numpy.zeros(nr_timesteps)
    daisy_w = numpy.zeros(nr_timesteps)

    for ts in range(0, nr_timesteps):
        breed_ts = breed[:, ts]
        mask_ts = mask[:, ts]
        breeds_alive = numpy.ma.masked_where(mask_ts!=1, breed_ts)
        w = numpy.ma.masked_where(breeds_alive==1, numpy.ones(breed.shape[0]))
        b = numpy.ma.masked_where(breeds_alive==0, numpy.ones(breed.shape[0]))
        daisy_b[ts] = len(numpy.ma.compressed(b))
        daisy_w[ts] = len(numpy.ma.compressed(w))

    plt.plot(daisy_b, label='black daisies', color='k')
    plt.plot(daisy_w, label='white daisies', color='lightgrey')
    plt.ylim([0, nr_agents])
    plt.ylabel('Population size (#)')
    plt.xlabel('Time step')
    plt.legend()
    plt.show()


if __name__ == '__main__':
  plot_population()
