import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy.stats import norm
import streamlit as st

st.set_page_config(
    page_title="AB test sample size calculator",
    page_icon="https://rfoxdata.co.uk/assets/favicon/favicon-32x32.png",
)

roboto = {"fontname": "Roboto", "size": "11"}
roboto_light = {"fontname": "Roboto", "size": "10", "weight": "light"}
roboto_title = {"fontname": "Roboto", "size": "12", "weight": "bold"}
roboto_small = {"fontname": "Roboto", "size": "7.5", "weight": "light"}

font = {"family": "sans-serif", "sans-serif": "roboto", "size": 11}

plt.rc("font", **font)

"""
# AB Test Sample Sizer

Input the expected daily observations and conversions to return a plot
containing potential runtimes and their associated minimum detectable effect.
"""

daily_obs = st.number_input("Daily observations", value=20000, step=100)
daily_cons = st.number_input("Daily conversions", value=1000, step=100)

f"Base conversion rate {daily_cons / daily_obs:.2%}"
n_variants = st.number_input("Number of variants (incl. the control)", value=2)

if st.checkbox("Add business value"):
    st.write(
        """This is for calculating the potential business value of the change,
        if successful and served to 100%."""
    )
    aov = st.number_input("Average conversion value", value=180)


def compute_sample_size(p0, mde, alpha=0.05, beta=0.2, tails="Two"):
    """
    Returns the sample size for a two-tailed AB test comparing conversion
    rates.

    The sample size equation is for binomial distributions only.

    Parameters
    ----------
    p0 : float
        Baseline conversion rate

    mde : float or int
        Minimum detectable effect. This is the 'sensitivity' of the test or
        the relative difference in conversion rates that you want to be able
        to detect.

    alpha : float
        The chances of a Type I error. Tests are normally run to a 95%
        significance meaning an alpha of 1 - 0.95 = 0.05. Default = 0.05.

    beta : float
        The chances of a Type II error. For sample sizing, a beta of 0.2 is
        acceptable and provides the test with 80% statistical power as is
        standard.

    tails : str
        One or two tails to specify what type of hypothesis test this is.

    Returns
    -------
    Minimum number of observations required per variant.
    """

    # Conditional alpha value based on whether one or two tail test
    if tails == "Two":
        computed_alpha = alpha / 2
    else:
        computed_alpha = alpha

    p1 = p0 * (1 + mde)
    N = (
        (norm.ppf(1 - computed_alpha) + norm.ppf(1 - beta)) ** 2
        * (p0 * (1 - p0) + p1 * (1 - p1))
        / ((p0 - p1) ** 2)
    )
    return int(N)


def create_mde_table(
    daily_observations, daily_conversions, n_variants, alpha=0.05, beta=0.2
):
    """Returns the sample sizes and runtimes for different impact sizes based
    on the daily observations and conversions input.

    Parameters
    ---------
    daily_observations : int/float
        Expected daily test subjects

    daily_conversions : int/float
        Expected daily conversions for test period

    n_variants:
        Number of variants tested

    Returns
    -------
    Dataframe populated with sample sizes and runtimes.
    """

    p0 = daily_conversions / daily_observations
    mde_range = np.arange(0.001, 2.001, 0.001)

    sample_sizes = [
        compute_sample_size(p0, mde, alpha, beta, num_tails) * n_variants
        for mde in mde_range
    ]
    p1 = [p0 * (1 + mde) for mde in mde_range]

    df = pd.DataFrame([mde_range, p1, sample_sizes]).transpose()
    df.columns = ["MDE", "New Conv. Rate", "Sample Size"]
    # We convert to np.int64 to round the number and also to avoid
    # hitting the int32 limit
    df["Sample Size"] = df["Sample Size"].astype(np.int64)
    df["Days"] = df["Sample Size"] / daily_observations
    df["Weeks"] = df["Days"] / 7
    df["Extra conversions (monthly)"] = round(
        p0 * df.MDE * daily_observations * 365 / 12
    )
    try:
        df["Extra revenue (monthly)"] = round(df["Extra conversions (monthly)"] * aov)
    except NameError:
        pass

    return df


# Sidebar - optional parameters
st.sidebar.markdown(
    """
### Significance level

95% is often used as the threshold before a result is declared as
statistically significant.
"""
)


def percentage_format(x):
    return f"{x:.0%}"


alpha = 1 - st.sidebar.slider(
    "Significance level",
    value=0.95,
    min_value=0.5,
    max_value=0.99,
)

st.sidebar.markdown(
    """
### Statistical power

80% is generally accepted as the minimum required power level.
"""
)
beta = 1 - st.sidebar.slider("Power", value=0.8, min_value=0.5, max_value=0.99)

st.sidebar.markdown(
    """
    ### One vs. two tails
"""
)
num_tails = st.sidebar.radio("Number of tails", ("One", "Two"), index=1)


st.sidebar.markdown(
    """
### Maximum runtime

To show increased runtimes on the plot.
"""
)
max_runtime = st.sidebar.number_input("Max runtime (weeks)", value=4, max_value=20)

df = create_mde_table(daily_obs, daily_cons, n_variants, alpha=alpha, beta=beta)


def plot_mde_marker(df, weeks, ax):
    days = weeks * 7
    ax.axhline(
        y=days,
        linestyle="--",
        xmax=(df[df["Weeks"] <= weeks]["MDE"].min() - ax.get_xlim()[0])
        / ax.get_xlim()[1]
        - 0.01,
    )
    if weeks > 1:
        week_text = "weeks"
    else:
        week_text = "week"
    ax.text(
        ax.get_xlim()[0],
        days + 1,
        f"{weeks} {week_text}",
        horizontalalignment="left",
        **roboto,
    )

    try:
        isLess = df["Weeks"] <= weeks
        mde_text = "MDE = {:.2%}, Monthly value = £{:,.0f}".format(
            df[isLess]["MDE"].min(), df[isLess]["Extra revenue (monthly)"].min()
        )
    except KeyError:
        mde_text = f"MDE = {df[isLess]['MDE'].min():.2%}"

    ax.text(
        df[df["Weeks"] <= weeks]["MDE"].min() * 1.05,
        days - 0.5,
        mde_text,
        horizontalalignment="left",
        **roboto,
    )


def y_format(x, pos):
    return f"{int(x):,}"


def mde_plot(data):
    fig, ax = plt.subplots(figsize=(10, 5), dpi=100)
    ax.plot(
        "MDE", "Days", data=data, linewidth=2, solid_capstyle="round", color="#014d64"
    )

    # Formatting the tick labels

    ax.yaxis.set_major_formatter(mtick.FuncFormatter(y_format))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    # Formatting the axes labels
    ax.set_xlabel("Minimum detectable effect", **roboto)
    ax.set_ylabel("")

    # Set limit to reasonable amount of time
    if ax.get_ylim()[1] > 60:
        ax.set_ylim([0, 7 * max_runtime * 1.2])

    # Set x-lim
    x_limit = data[data["Weeks"] <= 1]["MDE"].min() * 2
    ax.set_xlim([0, x_limit])

    for week in range(1, max_runtime + 1):
        plot_mde_marker(data, week, ax)

    # Clean up layout of graph, removing borders
    ax.yaxis.grid(True)
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    # Hiding the y-axis
    ax.axes.get_yaxis().set_visible(False)

    st.write(fig)


"""
## Test run times

Run times are plotted with their associated minimum detectable effect (MDE).
The longer a test runs, the smaller the impact size the test has the data to
detect. This is sometimes referred to as the accuracy of a test.

What is an acceptable MDE depends on how much of an impact you believe you
might see from your test.
"""

mde_plot(df)

if st.checkbox("Show table"):
    new = pd.DataFrame()
    for i in range(1, max_runtime + 1):
        if i > 1:
            week_text = "weeks"
        else:
            week_text = "week"
        new[f"{i} {week_text}"] = df[df["Weeks"] <= i].iloc[0]
    st.write(new)

# """
# ## Formula used
# """
# st.latex(r"""
# \left(\Phi\left(1 - \frac{\alpha}{2}\right)+\Phi(1-\beta)\right)^2
# \cdot \frac{p_0(1-p_0) + p_1(1-p_1)}{\left(p_0-p_1\right)^2}
# """)

"""
### See also

* [AB test significance calculator](https://abtestcalculator.herokuapp.com/)
* [Github Repository](https://github.com/rjjfox/ab-test-samplesize)
"""
