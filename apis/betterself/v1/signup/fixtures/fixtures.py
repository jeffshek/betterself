"""
    everything is based in minutes where possible

    'quantity_range' - random number selected between this range to count how many times supplement/activity occurred
    for a day

    'net_productivity_impact_per_quantity' - how much did this activity improve / decrease productivity, net means
    even though meditation takes 30 minutes, it adds almost 120 minutes of productivity back.
    so net is 120 - 30 = 90 minutes

    'peak_threshold_quantity' - at some point, everything we do has diminishing returns and then is negative
    'post_threshold_impact_on_productivity_per_quantity' - at negative returns, how much time does this hurt.
    ie. anyone that drinks 10 cups of coffee is unlikely to get anything done

    'sleep_impact_per_quantity' - does this help/hurt the amount of sleep one gets?
"""

SUPPLEMENTS_FIXTURES = {
    'Caffeine': {
        'quantity_range': (0, 5),  # more than 5 cups is just unrealistic
        'net_productivity_impact_per_quantity': 60,
        'peak_threshold_quantity': 3,
        'post_threshold_impact_on_productivity_per_quantity': -30,
        'sleep_impact_per_quantity': -10,
    },
    'Theanine': {
        'quantity_range': (0, 3),
        'net_productivity_impact_per_quantity': 20,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 15,
    },
    'Magnesium': {
        'quantity_range': (0, 3),
        'net_productivity_impact_per_quantity': 0,
        'peak_threshold_quantity': 2,
        # taking more than the peak just causes stomach issues, so it goes from no impact negative
        'post_threshold_impact_on_productivity_per_quantity': -20,
        'sleep_impact_per_quantity': 20,
    },
    'Ibuprofen': {
        'quantity_range': (0, 2),
        'net_productivity_impact_per_quantity': -45,
        # correlation != causation here, ibuprofen is an indicator of being sick, etc.
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': -20,  # days you've been ibuprofen, you don't sleep as well
    },
    'Fish Oil': {
        'quantity_range': (0, 2),
        'net_productivity_impact_per_quantity': 0,
        # fish oil doesn't have a direct impact, but improves sleep so next day see one would see improvements
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 30,
    },
    'Choline': {
        'quantity_range': (0, 1),
        'net_productivity_impact_per_quantity': 10,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 30,
    },
    'Piracetam': {
        'quantity_range': (0, 4),
        'net_productivity_impact_per_quantity': 30,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 30,
    },
    'Oxiracetam': {
        'quantity_range': (0, 2),
        'net_productivity_impact_per_quantity': 20,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 30,
    },
    'Vitamin B': {
        'quantity_range': (0, 1),
        'net_productivity_impact_per_quantity': 15,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 0,
    },
    'Alcohol': {
        'quantity_range': (0, 3),
        'net_productivity_impact_per_quantity': -15,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': -15,
    },
    'Tylenol': {
        'quantity_range': (0, 2),
        'net_productivity_impact_per_quantity': -5,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': -5,
    },
    'Creatine': {
        'quantity_range': (0, 5),
        'net_productivity_impact_per_quantity': 5,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 5,
    },
    'Multivitamin': {
        # let's follow the conventional advice that multivitamins do nothing
        'quantity_range': (0, 2),
        'net_productivity_impact_per_quantity': 3,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 3,
    },
}

USER_ACTIVITY_EVENTS = {
    'Meditation': {
        'quantity_range': (0, 3),
        'duration': 30,
        'net_productivity_impact_per_quantity': 90,  # meditation has your been your # 1
        'peak_threshold_quantity': 3,
        'post_threshold_impact_on_productivity_per_quantity': 0,
        'sleep_impact_per_quantity': 30,
    },
    'Ate Fast Food': {
        'quantity_range': (0, 2),
        'duration': 0,
        'net_productivity_impact_per_quantity': -45,  # eating fast food has absolutely crushed you with food coma
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': -20,
    },
    'Running': {
        'quantity_range': (0, 2),
        'duration': 30,
        'net_productivity_impact_per_quantity': 30,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 15,
    },
    'Gym': {
        'quantity_range': (0, 2),
        'duration': 30,
        'net_productivity_impact_per_quantity': 30,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 15,
    },
    'Cold Shower': {
        'quantity_range': (0, 1),
        'duration': 10,
        'net_productivity_impact_per_quantity': 30,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 0,
    },
    'Nap': {
        'quantity_range': (0, 1),
        'duration': 20,
        'net_productivity_impact_per_quantity': 60,
        'peak_threshold_quantity': None,
        'post_threshold_impact_on_productivity_per_quantity': None,
        'sleep_impact_per_quantity': 0,
    },
}
