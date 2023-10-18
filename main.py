from flask import Flask, request, jsonify, render_template
import json
import socket
import bible
import data_source


app = Flask(__name__)
theHost = '0.0.0.0'

@app.route("/")
def home():
  return render_template('index.html')


@app.route("/last")
def current():
    return data_source.get_status()

@app.route("/guildline")
def guildline():
    return jsonify(bible.BIBLE_INSTNACE.to_dict())

#  fetch('/content?bookName=' + bookName + '&charpterIndex=' + charpterIndex, { method: 'GET' })
@app.route("/content")
def content():
    bookName = request.args.get('bookName')
    charpterIndex = request.args.get('charpterIndex')
    print("get content: " + bookName + " " + charpterIndex)
    if bookName == None or charpterIndex == None or bookName == "" or charpterIndex == "":
        return ""
    return bible.BIBLE_INSTNACE.get_charpter_content(bookName, int(charpterIndex))

def is_port_in_use(thePort):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((theHost, int(thePort))) == 0

def get_unused_port():
    thePort = '5000'
    with open('port.txt', 'r') as file:
            thePort = file.read().strip()
            while is_port_in_use(thePort):
                thePort = str(int(thePort) + 1)
            file.close()
    # with open('port.txt', 'w') as file:
    #     file.write(thePort)
    #     file.close()
    return thePort


def flask_server():
        with open('port.txt', 'r') as file:
            thePort = get_unused_port()
            app.run(host=theHost, port=thePort, debug=True)


if __name__ == "__main__":
    flask_server()

