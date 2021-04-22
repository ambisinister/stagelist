import numpy as np

# comment out for stadium/FD starter
stages = ['Destination', 'Battlefield', 'Dreamland', 'Dreams', 'Story', 'Stadium']
#stages = ['Stadium', 'Battlefield', 'Dreamland', 'Dreams', 'Story', 'Destination']


def simulate_set(stagevector, dsr=True, ft=3, ban=False):

    def next_game(my_stagevector, opp_stagevector, games_won, games_lost,
                  counterpick=True, ft=3, ban=False, dsr=True):
        
        ## Which function should be used to pick the stage?
        if counterpick == True and ban == False:
            pickedstage = np.nanmin(my_stagevector)
        elif counterpick == False and ban == False:
            pickedstage = np.nanmax(opp_stagevector)
        # Ban logic a little hacky looking but it's just the second minimum/maximum without nans
        elif counterpick == True and ban == True:
            pickstage = lambda x: sorted(list(np.array(x)[~np.isnan(np.array(x))]))[1]
            pickedstage = pickstage(my_stagevector)
        elif counterpick == False and ban == True:
            pickstage = lambda x: sorted(list(np.array(x)[~np.isnan(np.array(x))]))[-2]
            pickedstage = pickstage(opp_stagevector)

        ## Base Cases
        if games_lost == ft:
            return 0
        elif games_won == ft:
            return 1
        elif games_won == ft-1 and games_lost == ft-1:
            return pickedstage
        else:
            if dsr: # if dsr, stage you won on becomes unpickable
                # My list of eligible stages isn't the same as their list of eligible stages
                
                my_new_stagevector = my_stagevector.copy()
                opp_new_stagevector = opp_stagevector.copy()

                if pickedstage in my_new_stagevector: #handle winning twice on counterpicks
                    my_new_stagevector[my_new_stagevector.index(pickedstage)] = np.nan
                if pickedstage in opp_new_stagevector:
                    opp_new_stagevector[opp_new_stagevector.index(pickedstage)] = np.nan

            wingame = pickedstage * next_game(my_new_stagevector, opp_stagevector,
                                              games_won+1,games_lost,
                                              counterpick=False,
                                              ft=ft, ban=ban, dsr=dsr)
            losegame = (1 - pickedstage) * next_game(my_stagevector, opp_new_stagevector,
                                                     games_won, games_lost+1,
                                                     counterpick=True,
                                                     ft=ft, ban=ban, dsr=dsr)

            return wingame + losegame

    # Starter game is the median starter stage, nobody has a counterpick
    starter = np.median(stagevector[:-1]) #exclude last index for counterpick
    if dsr:
        new_stagevector = stagevector.copy() #winning is the same for both players
        new_stagevector[new_stagevector.index(starter)] = np.nan

    winstarterwin = starter * next_game(new_stagevector, stagevector,
                                        1, 0, counterpick=True,
                                        ft=ft, ban=ban, dsr=dsr)
    losestarterwin = (1-starter) * next_game(stagevector, new_stagevector,
                                             0, 1, counterpick=False,
                                             ft=ft, ban=ban, dsr=dsr)
    
    return winstarterwin + losestarterwin
