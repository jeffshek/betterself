RT_VERY_DISTRACTING_TIME_LABEL = 'Very Distracting Time'
RT_DISTRACTING_TIME_LABEL = 'Distracting Time'
RT_NEUTRAL_TIME_LABEL = 'Neutral Time'
RT_PRODUCTIVE_TIME_LABEL = 'Productive Time'
RT_VERY_PRODUCTIVE_TIME_LABEL = 'Very Productive Time'
# 1-Off Header for Productivity Pulse (we don't get this data from RescueTime)
PRODUCTIVITY_PULSE = 'Productivity Pulse'

RESCUETIME_EFFICIENCY_HEADERS = [
    RT_VERY_DISTRACTING_TIME_LABEL,
    RT_DISTRACTING_TIME_LABEL,
    RT_NEUTRAL_TIME_LABEL,
    RT_PRODUCTIVE_TIME_LABEL,
    RT_VERY_PRODUCTIVE_TIME_LABEL
]

RESCUETIME_MAPPING_TO_INTERNAL_MODEL = {
    RT_VERY_DISTRACTING_TIME_LABEL: 'very_distracting_time_minutes',
    RT_DISTRACTING_TIME_LABEL: 'distracting_time_minutes',
    RT_NEUTRAL_TIME_LABEL: 'neutral_time_minutes',
    RT_PRODUCTIVE_TIME_LABEL: 'productive_time_minutes',
    RT_VERY_PRODUCTIVE_TIME_LABEL: 'very_productive_time_minutes',
}


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


def calculate_rescue_time_pulse_from_dataframe(dataframe):
    # for days that rescuetime doesn't have any data ... the label won't be in the data
    very_distracting_time = dataframe.get(RT_VERY_DISTRACTING_TIME_LABEL, 0)
    distracting_time = dataframe.get(RT_DISTRACTING_TIME_LABEL, 0)
    neutral_time = dataframe.get(RT_NEUTRAL_TIME_LABEL, 0)
    productive_time = dataframe.get(RT_PRODUCTIVE_TIME_LABEL, 0)
    very_productive_time = dataframe.get(RT_VERY_PRODUCTIVE_TIME_LABEL, 0)

    pulse = calculate_rescue_time_pulse(
        very_distracting=very_distracting_time,
        distracting=distracting_time,
        neutral=neutral_time,
        productive=productive_time,
        very_productive=very_productive_time,
    )

    return pulse
