# AB test sample size calculator

An AB test sample size calculator. Calculations come through basic SciPy.stats methods, the web app is built with Streamlit and hosted on Heroku.

See the [app live here](https://ab-test-samplesize.streamlit.app/).

<p align="center">
  <img src="./img/samplesize-demofull.gif" width="400px" alt="example usage of the sample size calculator">
</p>

See also my [AB test significance calculator](https://github.com/rjjfox/ab-test-calculator).

## Table of Contents

- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Built With](#built-with)
- [Features](#features)
- [License](#license)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Installing

### Clone Repository

Clone/fork the repo onto your local machine.

It is then recommended to use a virtual environment to install the dependencies using the requirements.txt file.

```cli
pip install -r requirements.txt
```

With these installed, you simply need to run

```cli
streamlit run app.py
```

### Docker

Alternatively, with Docker, use the following command and then navigate to localhost.

```
docker run -dp 80:8080 ryanfox212/samplesize
```

## Deployment

I utilised Streamit's Community Cloud service to host the app.

## Built With

- [Streamlit](https://www.streamlit.io/) - The web application framework used and deployment service
- [SciPy](https://www.scipy.org/) - For the statistical methods
- [Seaborn](https://seaborn.pydata.org/) - For vizualisations

## Features

### Minimal inputs

The calculator asks for daily observations and conversions and the number of variants that you would like to test.

Optional inputs:

- business value
- significance level (1-alpha)
- statistical power
- maximum runtime

### Useful output

A notable exception from the possible inputs is minimum detectable effect that you hope to achieve through the change made. Instead, this sample size calculator outputs a range of MDEs based on how long you run the test.

Personally, I have found this form of output more useful when scoping out tests to understand the level of precision that might be achieved.

The number of visitors I need in my test to achieve the required sample by itself does not tell me very much. It is this number relative to my traffic levels that gives me the information I need.

### Understanding business impact

Adding the business value of a conversion helps to understand what is the potential benefit/risk behind the change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
