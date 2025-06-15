# wishes

A wish calculator for Genshin. Main functions:<br>
* analytic calculations of probabilities for the next 5*
* analytic calculations of probabilities for target 5*s
* wishing simulations 
* all the above accounts for capturing radience and weapon banners
To run on the command-line, use wish.py--usage described below. The calculator has also been implemented as a [flask app](https://ricardoshillyshally.pythonanywhere.com/), with source code in app.py.


### assumptions
1. *5* character probabilities*. 0.6% at pity<74, +5.85% for each pity after 73. [reference](https://genshin-impact.fandom.com/f/p/4400000000000308779).
2. *target char probabilities*. 50% on non-guaranteed 5*; CR prob=0% for CR<2, 50% for CR=2, 100% otherwise. [reference](https://www.reddit.com/r/Genshin_Impact/comments/1f3ykny/capturing_radiance_details_observations_and/)
3. *5* weapon probabilities*. 0.7% at pity<63, +7% for each pity after 62. [reference](https://library.keqingmains.com/general-mechanics/gacha#featured-weapon-banner)
4. *target weapon probabilities*. 37.5% on non-guaranteed 5*; no CR. [reference](https://genshin-impact.fandom.com/wiki/Wish)


###

analytic probabilities of target 5* in 10 5*
