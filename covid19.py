from flask import Flask, request, make_response
import requests
import json
from flask_cors import cross_origin
# from logger import logger
import os

app = Flask(__name__)


# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)

    # print("Request:")
    # print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

    # processing the request from dialogflow


def processRequest(req):
    # log = logger.Log()

    sessionID = req.get('responseId')

    result = req.get("queryResult")
    user_says = result.get("queryText")
    # log.write_log(sessionID, "User Says: " + user_says)
    parameters = result.get("parameters")
    state_name = parameters.get("state_name")
    intent = result.get("intent").get('displayName')
    if intent == 'no_of_covid19_cases':
        # getting data from covid19-api
        url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

        headers = {
            'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
            'x-rapidapi-key': "65a4901e97msh53dc5860f91c9d0p1c5d8fjsn1400fa81c935"
        }

        response = requests.request("GET", url, headers=headers)
        # print(response.text)
        # converting response from api into a python dictionary
        data = json.loads(response.text)
        # prints dictionary
        # print(data)
        # state_name = "Maharashtra"

        confirmed_cases = data['state_wise'][state_name]['confirmed']
        active_cases = data['state_wise'][state_name]['active']
        deaths = data['state_wise'][state_name]['deaths']
        time = data['state_wise'][state_name]['lastupdatedtime']

        # print(confirmed_cases)

        show = 'The number of corona cases in {} are as follows:'.format(state_name)
        a = 'The number of active cases are: {}'.format(active_cases)
        b = 'The number of confirmed cases are: {}'.format(confirmed_cases)
        c = 'The number of deaths is: {}'.format(deaths)
        d = 'The last updated time is: {}'.format(time)


        # log.write_log(sessionID, "Bot Says: " + no_of_cases)
        return show, a, b, c, d
    else:
        # log.write_log(sessionID, "Bot Says: " + result.no_of_cases)
        pass


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
