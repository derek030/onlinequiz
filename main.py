from flask import Flask, redirect, url_for, request, jsonify, Response
import json
import os

app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')

@app.route('/success/<name>')
def success(name):
   return {"name": "123"}

@app.route('/login',methods = ['POST', 'GET'])
def login():
   #print("122")
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(port=port)
