from gevent import monkey
monkey.patch_all()

import json
import requests

from flask import Flask, jsonify, redirect, url_for, render_template, request

app=Flask(__name__)
app.secret_key = "supersecretkey"

BASE_IP = "0.0.0.0"
API_URL = "http://{0}:8000/api/v1/{1}"

@app.route('/')
def index():
    return redirect(url_for("cards"))

@app.route("/cards")
def cards():
    resp = requests.get(API_URL.format(BASE_IP, "events"))
    if resp.status_code == 200:
        cards = resp.json()
        return render_template("cards.html", cards=cards)
    
    return render_template("cards.html", cards=None)

@app.route("/card/new", methods=["POST"])
def newCard():
    if "new_card_submit" in request.form:
        cardName = request.form.get("card_name")
        resp = requests.get(API_URL.format(BASE_IP, "event?name={0}".format(cardName)))
        # flash message about creation after checking status code?????

    return redirect(url_for("cards"))

@app.route("/card/<cardID>")
def card(cardID):
    resp = requests.get(API_URL.format(BASE_IP, "event/{0}".format(cardID)))
    if resp.status_code == 200:
        card = resp.json()
        return render_template("card.html", card=card)

    return render_template("card.html", card=None)

@app.route("/card/<cardID>/delete")
def cardDelete(cardID):
    resp = requests.delete(API_URL.format(BASE_IP, "event/{0}".format(cardID)))
    
    return redirect(url_for("cards"))

@app.route("/card/<cardID>/subcard/<subcardID>/delete")
def subcardDelete(cardID, subcardID):
    resp = requests.delete(API_URL.format(BASE_IP, "event/{0}/content/{1}".format(cardID, subcardID)))
    
    return redirect(url_for("card", cardID=cardID))

@app.route("/card/<cardID>/subcard/new", methods=["POST"])
def newSubCard(cardID):
    if "new_subcard_submit" in request.form:
        cardName = request.form.get("subcard_name")
        resp = requests.get(API_URL.format(BASE_IP, "event/{0}/content?title={1}".format(cardID,cardName)))
        # flash message about creation after checking status code?????

    return redirect(url_for("card", cardID=cardID))

if __name__=='__main__':
    app.run(debug=True)