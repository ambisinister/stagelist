import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from parse_data import get_data
from simulate_set import simulate_set

mu_chart = get_data()

chars = ['Fox', 'Marth', 'Puff', 'Falco', 'Sheik', 'Falcon', 'Peach']
stages = ['Destination', 'Battlefield', 'Dreamland', 'Dreams', 'Story', 'Stadium']
#stages = ['Stadium', 'Battlefield', 'Dreamland', 'Dreams', 'Story', 'Destination']


def make_chart_with_params(bestof, ban, dsr):
    first_to = int(bestof/2) + 1

    all_mus = []
    for x in chars:
        my_mus = []
        for y in chars:
            stagevector = [mu_chart[x][y][stage] for stage in stages]
            stagevector = [x / 100 for x in stagevector]
            my_mus.append(simulate_set(stagevector, dsr=dsr, ft=first_to, ban=ban))

        all_mus.append(my_mus)

    sns.set()
    g = sns.heatmap(all_mus, annot=True)
    g.set_xticklabels(chars)
    g.set_yticklabels(chars)

    plt.title('Matchup Ratios in Best of {}{}{}'.format(bestof, '' if ban==False else ', with bans',
                                                        '' if dsr==True else ', no DSR'))
    plt.ylabel("Character")
    plt.xlabel("Character (opponent)")

    plt.savefig("/home/ambi/Dropbox/code/site/planetbanatt/org/images/stagelist/{}.png".
                format("bo{}{}".format(bestof, '_bans' if ban==True else '')))
    plt.clf()


    my_pov = np.mean(all_mus, axis=1)
    ur_pov = np.mean(all_mus, axis=0)

    print("*******")
    print("BEST OF {}".format(bestof))
    for i, char in enumerate(chars):
        print("{} POV: {:.3f}, Opponent POV: {:.3f}".format(char, my_pov[i], 1-ur_pov[i]))
    
    print("Tier List (player pov): {}".
          format([x for _, x in sorted(zip(my_pov, chars))][::-1]))
    
    print("Tier List (opponent pov): {}".
          format([x for _, x in sorted(zip(ur_pov, chars))]))


make_chart_with_params(bestof=5, ban=False, dsr=True)
make_chart_with_params(bestof=3, ban=True, dsr=True)
make_chart_with_params(bestof=5, ban=True, dsr=True)
