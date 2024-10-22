from plotly.graph_objs import XAxis
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.elements import progress
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import sqlite3
from query import *
import time

st.set_page_config(page_title="Dashboard", page_icon="🌎", layout="wide")
st.subheader("🔔 Insurance Descriptive Analysis")
st.markdown("##");

res = view_data()
df = pd.DataFrame(res, columns=["Policy", "Expiry", "Location", "State", "Region", "Investment", "Construction", "Business Type", "Earthquake", "Flood", "Rating"])
st.sidebar.image("images/logo.png", caption="DataMaster")

st.sidebar.header("Please filter")
region = st.sidebar.multiselect(
		"Select Region",
		options = df["Region"].unique(),
		default = df["Region"].unique()

	)

location = st.sidebar.multiselect(
		"Select Location",
		options = df["Location"].unique(),
		default = df["Location"].unique()

	)

construction = st.sidebar.multiselect(
		"Select Construction",
		options = df["Construction"].unique(),
		default = df["Construction"].unique()

	)

df_selection = df.query(
		"Region==@region & Location==@location & Construction==@construction"
	)

def home():
	with st.expander("Tabular"):
		showData = st.multiselect('Filter: ', df_selection.columns, default=[])
		st.write(df_selection[showData])

	totalInvestment = df_selection["Investment"].astype(float).sum()
	modeInvestment = df_selection["Investment"].astype(float).mode()
	medianInvestment = df_selection["Investment"].astype(float).median()
	meanInvestment = df_selection["Investment"].astype(float).mean()
	rating = df_selection["Rating"].astype(float).sum()

	total1, total2, total3, total4, total5 = st.columns(5, gap="large")

	with total1:
		st.info("Total investment", icon="💰")
		st.metric(label="Sum TZS", value=f"{totalInvestment:,.0f}")

	with total2:
		st.info("Most frequent", icon="💰")
		st.metric(label="Mode TZS", value=f"{modeInvestment.iloc[0]:,.0f}")

	with total3:
		st.info("Average investment", icon="💰")
		st.metric(label="Average TZS", value=f"{meanInvestment:,.0f}")

	with total4:
		st.info("Central earnings", icon="💰")
		st.metric(label="Median TZS", value=f"{medianInvestment:,.0f}")

	with total5:
		st.info("Ratings", icon="💰")
		st.metric(label="Rating", value=numerize(rating), help=f""" Total Rating: {rating} """)

	st.markdown("""---""")

def graphs():
	# totalInvestment = df_selection["Investment"].astype(int).sum()
	# averageRating = df_selection["Rating"].astype(int).mean()

	investmentByBusinessType = df_selection.groupby(by=["Business Type"]).count()[["Investment"]]

	figInvestment = px.bar(

			investmentByBusinessType,
			x="Investment",
			y=investmentByBusinessType.index,
			orientation="h",
			title="<b>  Investment by Bussiness Type  </b>",
			color_discrete_sequence=["#0083b8"] * len(investmentByBusinessType),
			template="plotly_white"

		)

	figInvestment.update_layout(

			plot_bgcolor="rgb(0,0,0,0)",
			xaxis=(dict(showgrid=False))

		)

	investmentByState = (df_selection.groupby(by=["State"]).count()["Investment"].sort_values(ascending=True))

	figState = px.line(

			investmentByState,
			x=investmentByState.index,
			y="Investment",
			orientation="v",
			title="<b>  Investment by State  </b>",
			color_discrete_sequence=["#0083b8"] * len(investmentByState),
			template="plotly_white"

		)

	figState.update_layout(

			xaxis=dict(tickmode="linear"),
			plot_bgcolor="rgb(0,0,0,0)",
			yaxis=(dict(showgrid=False)) 

		)

	l, r = st.columns(2)
	l.plotly_chart(figState, use_container_width=True)
	r.plotly_chart(figInvestment, use_container_width=True)

def progressBar():
	st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True)
	target = 3000000000
	current = df_selection["Investment"].sum()
	percent = round((current/target*100))
	myBar = st.progress(0)

	if percent > 100:
		st.subheader("Target done !")
	else:
		st.write("You have ", percent, "% ", "of ", (format(target, 'd')), " TZS")
		for percentComplete in range(percent):
			time.sleep(0.1)
			myBar.progress(percentComplete + 1, text="Target Percentage")


def sideBar():
	with st.sidebar:
		selected = option_menu(
				menu_title="Main Menu",
				options=["Home", "Progress"],
				icons=["house", "eye"],
				menu_icon="cast",
				default_index=0
			)

	if selected == "Home":
		st.subheader(f"Page: {selected}")
		home()
		graphs()

	elif selected == "Progress":
		st.subheader(f"Page: {selected}")
		progressBar()
		graphs()
	

sideBar()

