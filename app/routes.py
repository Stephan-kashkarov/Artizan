from app import app
from flask import render_template, redirect, url_for


@app.route("/")
def welcome():
	return "hello, world"
