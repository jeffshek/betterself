def calculate_rescue_time_pulse(very_distracting, distracting, neutral, productive, very_productive):
    """
    Per RescueTime API

    :param very_distracting: integer - number of seconds spent
    :param distracting: integer - number of seconds spent
    :param neutral: integer - number of seconds spent
    :param productive: integer - number of seconds spent
    :param very_productive: integer - number of seconds spent

    Per documentation, this is how the productive score is calculated.

    http://help.rescuetime.com/kb/rescuetime-website/how-is-my-productivity-pulse-calculated
    """
    # which is zero, lol
    very_distracting_score = very_distracting * 0
    distracting_score = distracting * 1
    neutral_score = neutral * 2
    productive_score = productive * 3
    very_productive_score = very_productive * 4

    total_score = very_distracting_score + distracting_score + neutral_score + productive_score + very_productive_score

    total_time_spent = very_distracting + distracting + neutral + productive + very_productive
    # final multiplier to even things out
    total_time_spent_scaled = total_time_spent * 4

    return total_score / total_time_spent_scaled

VERY_DISTRACTING_TIME_LABEL = 'Very Distracting Time'
DISTRACTING_TIME_LABEL = 'Distracting Time'
NEUTRAL_TIME_LABEL = 'Neutral Time'
PRODUCTIVE_TIME_LABEL = 'Productive Time'
VERY_PRODUCTIVE_TIME_LABEL = 'Very Productive Time'
# 1-Off Header for Productivity Pulse (we don't get this data from RescueTime)
PRODUCTIVITY_PULSE = 'Productivity Pulse'

RESCUETIME_EFFICIENCY_HEADERS = [
    VERY_DISTRACTING_TIME_LABEL,
    DISTRACTING_TIME_LABEL,
    NEUTRAL_TIME_LABEL,
    PRODUCTIVE_TIME_LABEL,
    VERY_PRODUCTIVE_TIME_LABEL
]


def calculate_rescue_time_pulse_from_dataframe(dataframe):
    pulse = calculate_rescue_time_pulse(
        very_distracting=dataframe[VERY_DISTRACTING_TIME_LABEL],
        distracting=dataframe[DISTRACTING_TIME_LABEL],
        neutral=dataframe[NEUTRAL_TIME_LABEL],
        productive=dataframe[PRODUCTIVE_TIME_LABEL],
        very_productive=dataframe[VERY_PRODUCTIVE_TIME_LABEL]
    )

    return pulse
