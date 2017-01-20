BetterSelf
==============================

.. image:: https://travis-ci.org/jeffshek/betterself.svg?branch=master
    :target: https://travis-ci.org/jeffshek/betterself
    
Figure out what works (and what doesn't) to be a better version of your self.

- Track events in 10 seconds on your phone (iPhone and Android support)
- Track your supplements / food intake / weather / locations to see what REALLY matters.
- Ever wonder if fish oil REALLY works? Correlations of your data across events like sleep and fitness (FitBit), productivity (RescueTime), or your personal tracker (whatever that may be). Intent is to become a dashboard of multiple vendors.
- Easy export of all your data. We have no intention to hold your data hostage.
- Easy import of data. Import your data via an Excel file, use our RESTful API, or use vendors (if provided).
- Allow different analytical methods to learn the usefulness of a supplement/events. Ever wonder if hangovers still impact you three days from the binge? Or if your productivity really takes a hit with only 5 hours of sleep?

For the nerds ...

- Full RESTful architecture. We eat our own dog food and use it to create all events you send us. Not dealing with half-baked APIs that are impossible to config.
- Fully open sourced. Developer environments are easily deployed via Docker with pre/post commit hooks, tests + travis to maintain sanity. Pull Request friendly.

Why are we (unfortunately, just me) doing this?

- Inspired by reddit nootropics (specifically Scott Alexander's survey), gwern's doubleblind studies, lots of anecdotal posts on Longecity / Reddit. Also partially motivated by the really bad posts (that time someone was convinced theanine made him a genius).
- There HAS GOT to be a better way for me to know supplements I'm taking is snake oil, placebo or meaningful.
- I don't want all my data to be held hostage (hence, the ease to export data).
- I want an app that doesn't care about my name and what I'm doing (we don't ask for anything besides email and a password to start). If you're scared, hit the big "delete all my data" button. We do have database backups, but those only go a month back.
- With enough data, we can build reports that show correlations across supplements, what is synergistic, what isn't.
- I want a app that is more robust than Excel, allow me to choose different correlation methods to productivity (Simple / Exponential / whatever I can think of)

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


LICENSE: MIT
