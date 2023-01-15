from flask import Flask, render_template, request
import openai

app = Flask(__name__)
app.static_folder = 'static'
openai.api_key = "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"

@app.route("/")
def index():
    return render_template("index.html")

def get_description_response(prompt):
    return openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"opisz mi czym jest nawyk {prompt} i wymień pozytywne efekty z jego budowy",
        temperature=0.5,
        max_tokens=500
    )["choices"][0]["text"]

def get_habit_list_response(prompt):
    return openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"stwórz dokładny, 15 punktowy plan, napisany w przyjacielskim tonie /"
               f" abym zbudował nawyk: {prompt}. Zadbaj, aby zawsze miał co najmniej 10 punktów, wraz z przykładem",
        temperature=0.5,
        max_tokens=1000
    )["choices"][0]["text"]

def get_example_response(prompt):
    return openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"stwórz praktyczny przykład budowania nawyku {prompt} zaczynający się od słów 'Jeżeli chcesz zbudować nawyk {prompt}'",
        temperature=0.5,
        max_tokens=500
    )["choices"][0]["text"]

def get_motivation_response(prompt):
    return openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Napisz mi krótki, motywacyjny cytat, odnoszący się do zbudowania nawyku {prompt}",
        temperature=0.5,
        max_tokens=200
    )["choices"][0]["text"]

@app.route("/response", methods=["POST"])
def response():
    try:
        prompt = request.form["prompt"]
        first_part = get_description_response(prompt)
        if first_part.isupper():
            pass
        else:
            first_part = first_part[1:]
        try:
            second_part = '1.' + get_habit_list_response(prompt).split('1.')[1]
        except IndexError:
            second_part = get_habit_list_response(prompt)
        if second_part.endswith('.'):
            pass
        else:
            second_part = second_part[:-1]

        third_part = get_example_response(prompt)
        try:
            fourth_part = get_motivation_response(prompt).split('"')[1]
            if fourth_part[-1] != '"':
                fourth_part = fourth_part + '"'
        except IndexError:
            fourth_part = get_motivation_response(prompt)


        return f'Oto twój plan na zbudowanie nawyku {prompt} {first_part}\n\n{second_part}\n\n{third_part}\n\n"{fourth_part}'
    except:
        f"Niestety wystąpił błąd. Spróbuj wygenerować plan jeszcze raz, lub odczekaj chwilę i spróbuj ponownie."

if __name__ == "__main__":
    app.run(debug=True)

