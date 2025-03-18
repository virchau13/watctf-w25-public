from flask import Flask, request, render_template_string, redirect, url_for, make_response
import jwt, os
from Crypto.PublicKey import RSA

app = Flask(__name__)

# RSA key pair
RSA_KEY = RSA.generate(2048)
PUBLIC_KEY = RSA_KEY.public_key().export_key().decode('utf-8')

FLAG = os.environ["FLAG"] if "FLAG" in os.environ else "don't hardcode secrets in source code!"

@app.route('/debug')
# def debug():
#     # Debugging JWT signing (COMMENT OUT IN PRODUCTION)
#     return RSA_KEY.export_key().decode('utf-8')

def get_hmac_secret():
    """Strip the header/footer and newlines from RSA_PUBLIC_KEY to form the HMAC secret."""
    lines = PUBLIC_KEY.strip().splitlines()
    return "".join(line for line in lines if "-----" not in line)

@app.route("/")
def index():
    # Dashboard page with a list of tasks (no token form).
    return render_template_string(index_template)

@app.route("/admin")
def admin():
    # ------------------------------------------------------------------
    # /admin endpoint: JWT is validated here.
    # Returns:
    #   - "Invalid Token" if token is missing or invalid.
    #   - "Access Denied" if token is valid but role is not 'admin'.
    #   - Success with the flag if the token is valid and role is 'admin'.
    # ------------------------------------------------------------------
    token = request.cookies.get("token")
    if not token:
        return render_template_string(error_template, error="Invalid Token")
    
    try:
        # Retrieve the token header without verification.
        unverified_header = jwt.get_unverified_header(token)
        if unverified_header.get("alg") == "HS384":
            # Use the stripped public key as the HMAC secret.
            secret = get_hmac_secret()
            payload = jwt.decode(token, secret, algorithms=["HS384"])
        else:
            # For tokens not using HS384, verify normally using RS256.
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
    except Exception as e:
        return render_template_string(error_template, error="Invalid Token")
    
    if payload.get("role") != "admin":
        return render_template_string(error_template, error="Access Denied")
    else:
        return render_template_string(admin_template, flag=FLAG)

# HTML templates

index_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Goose Inc. Intern Portal - Dashboard</title>
    <style>
        body {
            background: #f7f7f7;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            width: 700px;
            margin: 50px auto;
            background: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h2, h3 {
            color: #0073e6;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        ul li {
            background: #e3f2fd;
            margin: 8px 0;
            padding: 10px;
            border-radius: 4px;
        }
        .info {
            margin-top: 20px;
            font-size: 0.9em;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Welcome to Goose Inc. Intern Portal</h2>
        <h3>Dashboard</h3>
        <p>Your tasks for today:</p>
        <ul> <li>Complete your JWT configuration paperwork</li> <li>Review JWT authentication and authorization policies</li> <li>Set up your development environment for JWT implementation</li> <li>Attend the security briefing on token handling and storage</li> </ul>

        
        <!-- <p>To access the Admin Panel, send your JWT token in a cookie named <code>token</code> to the <code>/admin</code> endpoint.</p> -->
    </div>
</body>
</html>
"""

admin_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Goose Inc. Admin Panel</title>
    <style>
        body {
            background: #e0f7fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            width: 600px;
            margin: 50px auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        }
        h2 {
            color: #00796b;
        }
        .flag {
            background: #b2dfdb;
            padding: 20px;
            border-radius: 4px;
            font-weight: bold;
            text-align: center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- /admin endpoint: JWT is validated here. On success, the secret flag is revealed below. -->
        <h2>Admin Panel</h2>
        <p>Welcome, Admin Intern. Here is your secret:</p>
        <div class="flag">{{ flag }}</div>
    </div>
</body>
</html>
"""

error_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Error</title>
    <style>
        body {
            background: #ffebee;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .container {
            width: 400px;
            margin: 100px auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        h2 {
            color: #d32f2f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>{{ error }}</h2>
        <p>Please check your token and try again.</p>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
