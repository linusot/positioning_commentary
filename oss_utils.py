def anr_assignment(score):
    if 2 > score:
        return 'Strong Sell'
    if 2.5 > score >= 2:
        return 'Sell'
    if 4 > score >= 2.5:
        return 'Hold'
    if 4.5 > score >= 4:
        return 'Buy'
    if score >= 4.5:
        return 'Strong Buy'


def price_score_assignment(score):
    if score <= -10:
        return 0
    elif -10 < score <= 10:
        return (score+10)/5
    elif score > 10:
        return 4


def performance_score_assignment(score):
    if score <= -10:
        return 0
    elif -10 < score <= 10:
        return (score + 10) / 5
    elif score > 10:
        return 4


def rsi_score_assignment(score):
    if score <= 30:
        return 0
    elif 30 < score <= 45:
        return (score-30)/15
    elif 45 < score <= 55:
        return (score-40)/5
    elif 55 < score <= 70:
        return (score-10)/15
    elif score > 70:
        return 4
    else:
        return 2


def eps_score_assignment(score):
    if -200 < score <= -5:
        return 0
    elif -5 < score <= -1:
        return (score+5)/4
    elif -1 < score <= 1:
        return 2 + score
    elif 1 < score <= 5:
        return (score+11)/4
    elif 5 < score < 200:
        return 4
    else:
        return 2


def cds_score_assignment(score):
    if score <= 105:
        return 2
    elif 105 < score <= 210:
        return 1
    elif score > 210:
        return 0
    else:
        return 2


def si_score_assignment(score):
    if score <= 0.5:
        return 4
    elif 0.5 < score <= 1:
        return 5 - 2 * score
    elif 1 < score <= 3:
        return (7 - score) / 2
    elif 3 < score <= 5:
        return 5 - score
    elif score > 5:
        return 0
    else:
        return 2


def vol_score_assignment(score):
    if score == -1000:
        return 2
    elif score <= -1.99:
        return 4
    elif -1.99 < score <= -.99:
        return 2.01 - score
    elif -.99 < score <= .99:
        return (1.98 - score) / 0.99
    elif .99 < score <= 1.99:
        return 1.99 - score
    elif score > 1.99:
        return 0
    else:
        return 2


def valn_score_assignment(score):
    if score == -1000:
        return 2
    elif score <= -2:
        return 0
    elif -2 < score <= -1:
        return 1.99 + score
    elif -1 < score <= 1:
        return (1.98 + score) / 0.99
    elif 1 < score <= 2:
        return score + 2.01
    elif score > 2:
        return 4
    else:
        return 2


def yield_score_assignment(score):
    if score == -1000:
        return 2
    elif score <= -1.99:
        return 4
    elif -1.99 < score <= -.99:
        return 2.01 - score
    elif -.99 < score <= .99:
        return (1.98 - score) / 0.99
    elif .99 < score <= 1.99:
        return 1.99 - score
    elif score > 1.99:
        return 0
    else:
        return 2


def hold_pt_assignment(score):
    if -4 > score:
        return 0
    elif score in [-3, -4]:
        return 1
    elif 2 >= score >= -2:
        return 2
    elif score in [3, 4]:
        return 3
    elif score > 4:
        return 4


def sell_pt_assignment(score):
    if -4 > score:
        return 0
    elif score in [-3, -4]:
        return 1
    elif 0 >= score >= -2:
        return 2
    elif score > 0:
        return 3


def buy_pt_assignment(score):
    if 0 > score:
        return 0
    elif 2 >= score >= 0:
        return 1
    elif score in [3, 4]:
        return 2
    elif score > 4:
        return 3


def sector_rsi_assignment(score):
    if score >= 80:
        return 0
    elif 79 >= score >= 70:
        return 1
    elif 70 > score >= 60:
        return 2
    elif 60 > score >= 40:
        return 3
    elif 40 > score >= 30:
        return 4
    elif 30 > score >= 20:
        return 5
    elif 20 >= score:
        return 6
