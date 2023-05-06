import streamlit as st
import calendar
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")


file = open("watch-history.json", errors='replace')

text = file.read()

j=json.loads(text)

streaming_history = pd.DataFrame(j)

streaming_history.time = pd.to_datetime(streaming_history.time)

streaming_history["date"] = streaming_history["time"].dt.floor('d')

by_date = streaming_history.groupby("date")[["title"]].count()
by_date = by_date.sort_index()

by_date["weekday"] = by_date.index.weekday
by_date["week"] = by_date.index.week


week = 0
prev_week = by_date.iloc[0]["week"]
continuous_week = np.zeros(len(by_date)).astype(int)
sunday_dates = []
for i, (_, row) in enumerate(by_date.iterrows()):
    if row["week"] != prev_week:
        week += 1
        prev_week = row["week"]
    continuous_week[i] = week
by_date["continuous_week"] = continuous_week
by_date.head()

videos = np.full((7, continuous_week.max()+1), np.nan)

for index, row in by_date.iterrows():
    videos[row["weekday"]][row["continuous_week"]] = row["title"]

min_date = streaming_history["time"].min()
first_monday = min_date - timedelta(min_date.weekday())
mons = [first_monday + timedelta(weeks=wk) for wk in range(continuous_week.max())]
x_labels = [calendar.month_abbr[mons[0].month]]
x_labels.extend([
    calendar.month_abbr[mons[i].month] if mons[i-1].month != mons[i].month else ""
    for i in range(1, len(mons))])
x_labels.append("")
y_labels = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"]


fig = plt.figure(figsize=(50,10))
ax = plt.subplot()


ax.set_title("My year on Youtube", fontsize=20,pad=40)
ax.xaxis.tick_top()
ax.tick_params(axis='both', which='both',length=0)
ax.set_facecolor("#ebedf0")
fig.patch.set_facecolor('white')



sns.heatmap(data=videos, linewidths=5, linecolor='white', square=True,
            mask=np.isnan(videos), cmap="Reds",
            vmin=0, vmax=100, cbar=False, ax=ax)

ax.set_xticklabels(x_labels, ha="left")
ax.set_yticklabels(y_labels, rotation=0)



# Streamlit app page setup
st.set_page_config(
    page_title='Streamlit App showing my Youtube Watch history like Github Commits',
    page_icon='📺',
    layout='centered',
    initial_sidebar_state='expanded',
    menu_items={
        'About': """An interactive App that shows my Youtube Watch history
 ."""
    }
)

# Main header
st.header('Youtube Watch history Streamlit app')


# Add some blank space
st.markdown("##")


st.pyplot(fig)


