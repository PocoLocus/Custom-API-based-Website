import requests, os
from flask import Flask, render_template, redirect, request, flash, url_for
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
URL = "https://the-one-api.dev/v2"
header = {
    "Authorization" : f"Bearer {ACCESS_TOKEN}"
}

general_response = requests.get(url=f"{URL}/character", headers=header)
all_characters_data = general_response.json()["docs"]

def get_the_data(given_name):
    character = None
    for i in range(len(all_characters_data)):
        if all_characters_data[i]["name"] == given_name:
            character_id = all_characters_data[i]["_id"]

            response = requests.get(url=f"{URL}/character/{character_id}/quote", headers=header)
            character_quotes = response.json()["docs"]
            list_of_quotes = []
            for quote in character_quotes:
                list_of_quotes.append(quote["dialog"])

            character = {
                "id" : all_characters_data[i]["_id"],
                "name" : all_characters_data[i]["name"],
                "race" : all_characters_data[i]["race"],
                "gender" : all_characters_data[i]["gender"],
                "realm" : all_characters_data[i]["realm"],
                "spouse" : all_characters_data[i]["spouse"],
                "quotes" : list_of_quotes
            }
            break
    return character

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["name"]
        character = get_the_data(user_input)
        if character:
            return render_template("result.html", character=character)
        else:
            flash("This character does not exist, try again.")
            redirect(url_for("home"))
    return render_template("home.html")

if __name__ == "__main__":
    app.run()