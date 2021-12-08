from enum import unique
from flask import Flask, render_template, request, url_for, redirect, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, numbers, json, re
import hubspot
from pprint import pprint
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


client = hubspot.Client.create(api_key=os.getenv('API_KEY'))


properties = {
    "company": "Biglytics",
    "email": "bcooper@biglytics.net",
    "firstname": "Bryan",
    "lastname": "Cooper",
    "phone": "(877) 929-0687",
    "website": "biglytics.net"
}


simple_public_object_input = SimplePublicObjectInput(properties=properties)


try:
    api_response = client.crm.contacts.basic_api.create(simple_public_object_input=simple_public_object_input)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling basic_api->create: %s\n" % e)


def check(obj):
  regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
  return re.search(regex, obj)

class Contatos(db.Model):
  id = db.Column(db.Integer)
  nome = db.Column(db.String(200), nullable=False)
  sobrenome = db.Column(db.String(200), nullable=False)
  email = db.Column(db.String(200), primary_key=True, nullable=False, unique=True)
  fone = db.Column(db.String(20), nullable=False)
  data_nasc = db.Column(db.Date, default=datetime.utcnow)
  peso = db.Column(db.Float, nullable=False)

  def __repr__(self):
    return f'<Task {self.email}>'

class HubSpot:
  key = os.getenv('API_KEY')
  endpoint = os.getenv('CONTACT_ENDPOINT')
  headers = {'Content-Type': 'application/json'}
  params = {"hapikey": os.getenv('API_KEY')}


  def get_contact_by_email(self, email):
    if check(email):
      url = f"{self.endpoint}/email/{email}/profile"
      r = request.get(url=url, params=self.params)
      return r
    else:
      raise Exception("Por favor, disponibilize um endereço de e-mail.")


  def create_contact(self, arr):
    data = hs_templates(arr)
    url = f'{self.endpoint}/'
    r = request.post(url=url, headers=self.headers, params=self.params, data=json.dumps(data))
    return r



  def update_property(self, email, arr):
    if check(email):
      data = hs_templates(arr)
      url = f'{self.endpoint}/email/{email}/profile'
      r = request.post(url, headers=self.headers, params=self.params, data=json.dumps(data))
      return r
    else:
      raise Exception("E-mail inválido.")

    
  def del_contact(self, id):
    if isinstance(id, numbers.Number):
      url = f'{self.endpoint}/vid/{id}'
      r = request.delete(url=url, params=self.params)
      return r
    else:
      raise Exception("O ID deve ser um número inteiro.")


@app.route("/", methods=["POST", "GET"])
def index():
  return render_template('index.html')


@app.route("/send_form", methods=["POST"])
def send_form():
  usuario = request.form['usuario']
  if usuario != '':
    try:
      pass
      return render_template('index.html', usuario=usuario)
    except:
      pass
      return render_template('index.html', usuario=usuario)


if __name__ == '__main__':
  app.run(debug=True, port=5000)