import random
import string
from jobpost.models import uniqueids

from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect


# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "jobpost/credentials.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/drive.metadata.readonly']

API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'

def generate_random_id():
    while True:
        letters = string.ascii_letters
        digits = string.digits
        
        # Generate a random word with length between 3 and 8 characters
        word = ''.join(random.choice(letters) for _ in range(random.randint(3, 4)))
        
        # Generate a random number with 4 digits
        number = ''.join(random.choice(digits) for _ in range(4))
        
        # Concatenate the word and number
        random_id = f"{word}{number}"
        
        # Retrieve existing unique IDs from the database
        existing_ids = uniqueids.objects.values_list('uniqueid', flat=True)
        
        if random_id not in existing_ids:
            return random_id
            break
        else:
            pass
    

def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)


    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    return state, authorization_url

def exchange_code_for_token(code, state, redirect_uri):
    # Load client secrets from the client_secrets.json file
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state, redirect_uri=redirect_uri)
    
    # Exchange the authorization code for a token
    flow.fetch_token(code=code)
    
    # Return the credentials object
    return flow.credentials

def oauth2callback(request):
    # Retrieve the state from the session
    state = request.session.pop('oauth_state', None)
    
    if state is None:
        # Handle the case where the state is missing
        # Redirect the user to an error page or handle it appropriately
        pass
    
    # Retrieve the authorization code from the query parameters
    code = request.GET.get('code')
    
    # Exchange the authorization code for an access token
    credentials = exchange_code_for_token(code, state)
    
    # Store the credentials in the session or database for future use
    # Note: Storing credentials in the session is not recommended for production
    request.session['credentials'] = credentials.to_json()
    
    # Redirect the user to the recruiter dashboard or any other page
    return redirect('recuiter_dashboard_page')
