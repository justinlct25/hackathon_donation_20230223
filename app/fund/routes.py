from fund import app, db
from flask import render_template, url_for, request, jsonify, redirect, flash, jsonify



@app.route('/')
def hello():
    return render_template('index.html')