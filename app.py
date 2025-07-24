from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

NUMVERIFY_API_KEY = os.getenv('NUMVERIFY_API_KEY', '6a6984a4d5dbdfd93dba561c11e47211')  # your key as fallback

@app.route('/voice', methods=['POST'])
def voice_webhook():
    caller_number = request.form.get('From', None)
    if not caller_number:
        caller_number = 'unknown'
    print(f"Incoming call from: {caller_number}")

    api_url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={caller_number}&format=1"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get('valid'):
            country = data.get('country_name', 'Unknown country')
            location = data.get('location', 'Unknown location')
            carrier = data.get('carrier', 'Unknown carrier')
            line_type = data.get('line_type', 'Unknown line type')

            message = (
                f"Caller number {caller_number}. "
                f"Country: {country}. "
                f"Location: {location}. "
                f"Carrier: {carrier}. "
                f"Line type: {line_type}."
            )
        else:
            message = "Caller number information could not be found."
    except Exception as e:
        print(f"Error fetching number info: {e}")
        message = "Sorry, there was an error retrieving caller information."

    twiml = f"""
    <Response>
        <Say voice="alice">{message}</Say>
    </Response>
    """
    return Response(twiml, mimetype='text/xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
