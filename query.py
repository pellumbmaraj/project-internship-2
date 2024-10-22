import sqlite3
import streamlit as st


conn = sqlite3.connect("data.db")

cursor = conn.cursor()

def view_data():
	cursor.execute("SELECT * FROM Data;")
	data = cursor.fetchall()
	return data





