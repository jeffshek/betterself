
![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Travis](https://travis-ci.org/jeffshek/betterself.svg?branch=master)
![CookieCutter](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg)
![PyUp](https://img.shields.io/pypi/v/pyupio.svg)

Powered by [BrowserStack](https://BrowserStack.com) (Logo on button of README.md)

BetterSelf - Your Body's Dashboard
==============================
![Analytics](https://user-images.githubusercontent.com/392678/29753400-b58d00b4-8b3e-11e7-93eb-60c9eb206d16.png)

Figure out what works (and what doesn't) to be a better version of your self.

- Track events in 10 seconds on your phone (iPhone and Android support)
- Track your supplements / food intake / weather / locations to see what REALLY matters.
- Ever wonder if fish oil REALLY works? Correlations of your data across events like sleep and fitness (FitBit), productivity (RescueTime), or your personal tracker (whatever that may be). Intent is to become a dashboard of multiple vendors.
- Easy export of all your data. We have no intention to hold your data hostage.
- Easy import of data. Import your data via an Excel file, use our RESTful API, or use vendors (if provided).
- Allow different analytical methods to learn the usefulness of a supplement/events. Ever wonder if hangovers still impact you three days from the binge? Or if your productivity really takes a hit with only 5 hours of sleep?


![Overview](https://user-images.githubusercontent.com/392678/29753424-259da854-8b3f-11e7-8869-667aa6a12007.png)

![Fitbit And Sleep](https://user-images.githubusercontent.com/392678/29753405-ccc2ad06-8b3e-11e7-8536-75736ece9e9b.png)
        
For the nerds ...

- RESTful architecture (I'm just not convinced about Level 3). We eat our own dog food and use it to create all events you send us. All events and tracking is done through an API. Rest assured, it's meant to be developer friendly.
- Fully open sourced. Developer environments are easily deployed via Vagrant with pre/post commit hooks, tests + travis to maintain sanity. Pull Request friendly. Probably switch to Docker, eventually, stage two ...

Why are we doing this?

- Inspired by reddit nootropics (specifically Scott Alexander's survey), gwern's doubleblind studies, lots of anecdotal posts on Longecity / Reddit. Also partially motivated by the really bad posts (that time someone was convinced theanine made him a genius).
- There HAS GOT to be a better way for me to know supplements I'm taking is snake oil, placebo or meaningful.
- I don't want all my data to be held hostage (hence, the ease to export data).
- I want an app that doesn't care about my name and what I'm doing (we don't ask for anything besides email and a password to start). If you're scared, hit the big "delete all my data" button. We do have database backups, but those only go a month back.
- With enough data, we can build reports that show correlations across supplements, what is synergistic, what isn't.
- I want a app that is more robust than Excel, allow me to choose different correlation methods to productivity (Simple / Exponential / whatever I can think of)

Powered by [BrowserStack](https://www.browserstack.com/)

![BrowserStack Logo](https://d98b8t1nnulk5.cloudfront.net/production/images/layout/logo-header.png?1469004780) 

