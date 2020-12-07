# AB test sample size calculator

An AB test sample size calculator, built with Streamlit.

- Powered by Python
- Built with Streamlit
- Hosted on Heroku

Suitable for binomial metrics only, i.e. metrics with binary outcomes such as conversion rate.

<p align="center">
  <img src="./img/samplesize-demofull.gif" width="400px">
</p>

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

## Run locally

### Clone repository

Clone the repository and run the following within the command line to run the Streamlit app on your localhost

```
streamlit run app.py
```

### Docker

Alternatively, with Docker, use the following command and then navigate to localhost.

```
docker run -dp 80:8080 ryanfox212/samplesize
```
