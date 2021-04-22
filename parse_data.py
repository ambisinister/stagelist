import pandas as pd
import numpy as np

def get_data():
    data = pd.read_csv('./mus.csv')

    # The High Tiers, in order
    chars = ['Fox', 'Marth', 'Puff', 'Falco', 'Sheik', 'Falcon', 'Peach']
    mu_chart = {}

    for x in chars:
        char_data = data[data['Which character do you main?'] == x]
        char_chart = {}

        for y in chars:
            stage_chart = {}
            for col in char_data.columns:
                if col.split(' ')[0] == 'Your' and col.split(' ')[3] == y:
                
                    ratios = char_data[col]

                    rat_vals = []

                    for j in ratios:
                        if type(j) == str:
                            try:
                                rat_vals.append(int(j.split('-')[0]))
                            except:
                                if j.split(' ')[0] == 'Better':
                                    rat_vals.append(80)
                                else:
                                    rat_vals.append(20)

                    if len(col.split(' ')[-1]) == 0:
                        stage_here = col.split(' ')[-2]
                    else:
                        stage_here = col.split(' ')[-1]

                    stage_chart[stage_here] = np.mean(rat_vals)
                
            char_chart[y] = stage_chart

        mu_chart[x] = char_chart
    
    return mu_chart
