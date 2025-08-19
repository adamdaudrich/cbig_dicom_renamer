import requests

status_messages = {
    200: "Connection to API successful",
    401: "Invalid credentials", 
    403: "Access forbidden",
    404: "Endpoint not found",
    500: "Server error occurred"
}

def connect_to_api(config):
    """
    use config file to login and authorize in CBIGR API
    arg: json
    returns: str 
    """

    login_resp = requests.post(cfg["login_url"], data = config["credentials"])
        
    message = status_messages.get(login_resp.status_code, f"Unexpected status code: {login_resp.status_code}")
    
    print(f"Status {login_resp.status_code}: {message}")
    
    if login_resp.status_code == 200:
        token = login_resp.json().get("token")
        return token
    else:
        return None 

def fetch_candidates(token, config):
    """
    Fetches candidate json string from CBIGR API 
    args: str, str
    returns: str
    """

    headers = {
        "Authorization": f"Bearer{token}"
    }
    candidates_resp = requests.get(config["candidates_url"], headers=headers),
    message = status_messages.get(candidates_resp.status_code, f"Unexpected status code: {candidates_resp.status_code}")
    
    print(f"Status {candidates_resp.status_code}: {message}")
    
    if candidates_resp.status_code == 200:
        candidates = candidates_resp.json().get("Candidates", [])
        return candidates
    else:
        return None
