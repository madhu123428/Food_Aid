from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from datetime import datetime
timestamp = datetime.now().isoformat()


app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def index():
    print("ROUTE: Accessing the index page.")
    return render_template('index.html')

@app.route('/donate', methods=['GET', 'POST'])
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'food_type': request.form['food_type'],
            'quantity': request.form['quantity'],
            'location': request.form['location'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'timestamp': timestamp
        }

        # Replace with the URL of your new consolidated Relay workflow
        relay_url = "https://hook.relay.app/api/v1/playbook/cme0xo9bu0i1b0olwaf5j04n5/trigger/pPmE1gcSrsXrO_njjiB5hw" 

        try:
            # Make a single POST request to the Relay workflow
            res = requests.post(relay_url, json=data)
            if res.status_code == 200:
                response_data = res.json()
                if response_data.get('status') == 'sent':
                    # Redirect to a success page for sent emails
                    return render_template('confirmation.html')
                elif response_data.get('status') == 'not sent':
                    # Redirect to a different page for not-sent emails
                    return render_template('not_sent.html')

        except Exception as e:
            flash("❌ Error contacting Relay: " + str(e))
        
        return redirect(url_for('donate'))

    return render_template('donate.html')



@app.route('/register-ngo', methods=['GET', 'POST'])
def register_ngo():
    if request.method == 'POST':
        ngo_data = {
            "Name": request.form['name'],
            "Location": request.form['location'],
            "Need": request.form['need'],
            "ContactEmail": request.form['email'],
            "ContactPhone": request.form['phone'],
            "Timestamp": timestamp
        }

        # 🔗 Send to Relay to add to Google Sheet
        relay_url = 'https://hook.relay.app/api/v1/playbook/cmdyx7w7d06hb0pm264aoh8k7/trigger/1ydLcNDGueHxsd8rt-qt3A'
        try:
            res = requests.post(relay_url, json=ngo_data)
            if res.status_code == 200:
                response_data = res.json()
                flash("NGO Registered Successfully!")
                if response_data.get('status') == 'sent':
                    # Redirect to a success page for sent emails
                    return render_template('ngo_confirmation.html')
                elif response_data.get('status') == 'not sent':
                    # Redirect to a different page for not-sent emails
                    return render_template('ngo_not_sent.html')
            else:
                flash("Relay Error: " + res.text)
        except Exception as e:
            flash("Error: " + str(e))
        return redirect(url_for('register_ngo'))

    return render_template('ngo_register.html')

@app.route('/requests', methods=['GET'])
def view_requests():
    # Example: render a template showing requests
    return render_template('requests.html')  # make sure this file exists

# @app.route('/accept-donation', methods=['POST'])
# def accept_donation():
#     donor = request.form['donor_name']
#     food_type = request.form['food_type']
#     location = request.form['location']
#     quantity = request.form['quantity']

#     print(f"ROUTE: /accept-donation")
#     print(f"STEP: Accepted donation details:")
#     print(f"  Donor: {donor}")
#     print(f"  Food Type: {food_type}")
#     print(f"  Location: {location}")
#     print(f"  Quantity: {quantity}")

#     flash(f"You accepted the donation from {donor}.")
#     print("STEP: Flashed message to user.")
#     print("STEP: Redirecting to index page.")
#     return redirect(url_for('index'))

# @app.route('/notify-ngo', methods=['POST'])
# def notify_ngo():
#     data = {
#         'ngo_email': request.form['ngo_email'],
#         'ngo_name': request.form['ngo_name'],
#         'donor_name': request.form['donor_name'],
#         'food_type': request.form['food_type'],
#         'quantity': request.form['quantity'],
#         'location': request.form['location']
#     }
#     print(f"ROUTE: /notify-ngo")
#     print(f"STEP: Data prepared for Relay webhook: {data}")
#     # 🔗 Replace this with your actual Relay email notification webhook
#     relay_notify_url = "https://hook.relay.app/api/v1/playbook/cme0yfpvh0nc10om38wzb03ui/trigger/G5LItRJ8_kPguA2LF7RVaw"
#     print(f"STEP: Posting data to Relay URL: {relay_notify_url}")
#     try:
#         response = requests.post(relay_notify_url, json=data)
#         print(f"STEP: Received status code from Relay: {response.status_code}")
#         print(f"STEP: Relay response text: {response.text}")
#         if response.status_code == 200:
#             flash("✅ NGO has been notified via email.")
#             print("STEP: Flashed success message.")
#         else:
#             print(f"ERROR: Exception occurred while contacting Relay: {str(e)}")
#             flash("❌ Relay error while notifying NGO: " + response.text)
            
#     except Exception as e:
#         print("STEP: Flashed error message.")
#         flash("❌ Error contacting Relay: " + str(e))
#         print("STEP: Flashed exception message.")
#     print("STEP: Redirecting to index page after notifying NGO.")
#     return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
