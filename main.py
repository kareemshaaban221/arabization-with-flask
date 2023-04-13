from flask import Flask, render_template, request
import functions as func
import pickle
import warnings
from flask_babel import Babel, gettext

warnings.filterwarnings("ignore")
app = Flask(__name__)

app.config['BABEL_DEFAULT_LOCALE'] = 'en';
app.config['LANGUAGES'] = {'en': 'English', 'ar': 'Arabic'}
babel = Babel(app)

def get_locale():
    return request.args.get('lang')
babel.init_app(app, locale_selector=get_locale)

app.jinja_env.globals['get_locale'] = get_locale

# * home page
@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", page_title=gettext("Summariza"))


# * summarization route
@app.route("/summarize", methods=['POST'])
def analyze_text():
    # * form data
    input_language = request.form['lang']
    input_text = request.form['original']
    sentences_number = 1 if request.form['no_sent'] == '' or request.form['no_sent'] == None or int(request.form['no_sent']) <= 0 else request.form['no_sent']
    
    # * summarization action
    if input_language == 'en':
        classifier_model = pickle.load(open('models/en_ridge_model.pkl', 'rb'))
        text_summary, text_category = func.summarize_category(input_text, sentences_number, classifier_model, False)
    else:
        classifier_model = pickle.load(open('models/ar_ridge_model.pkl', 'rb'))
        text_summary, text_category = func.summarize_category(input_text, sentences_number, classifier_model, True)
    
    # * returning page
    return render_template("index.html", page_title=gettext("Summariza | Done"), input_text=input_text, text_summary=text_summary, text_category=text_category, no_sent=sentences_number)


# * program run
if __name__ == "__main__":
    app.run()