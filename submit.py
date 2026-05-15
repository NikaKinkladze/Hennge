import hmac
import hashlib
import struct
import time
import base64
import urllib.request
import urllib.error
import json


def generate_totp(secret: str) -> str:
    """
    Generate a 10-digit TOTP using HMAC-SHA-512.
    - Time step: 30 seconds
    - T0: 0
    - Secret: email + "HENNGECHALLENGE004"
    """
    # Current time step (RFC6238: T = floor((Current Unix time - T0) / X))
    t = int(time.time()) // 30

    # Pack time step as big-endian 8-byte unsigned int (as per RFC4226/6238)
    msg = struct.pack(">Q", t)

    # Secret is the raw UTF-8 bytes of the shared secret string
    key = secret.encode("utf-8")

    # Compute HMAC-SHA-512
    h = hmac.new(key, msg, hashlib.sha512).digest()

    # Dynamic truncation (RFC4226 Section 5.3)
    # Use the low-order 4 bits of the last byte as the offset
    offset = h[-1] & 0x0F

    # Extract 4 bytes starting at offset, mask the most significant bit
    code = struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF

    # 10-digit OTP (mod 10^10)
    otp = code % (10 ** 10)

    return str(otp).zfill(10)


def main():
    # -------------------------------------------------------------------------
    # FILL IN YOUR DETAILS BELOW
    # -------------------------------------------------------------------------

    # Your contact email address (the one you want HENNGE to reach you at)
    email = "your_email@example.com"  # <-- Replace with your actual email

    # The full URL of your secret GitHub gist containing main.py
    github_url = "https://gist.github.com/YOUR_ACCOUNT/GIST_ID"  # <-- Replace with your gist URL

    # The language you used: either "golang" or "python"
    solution_language = "python"  # <-- Change to "golang" if you used Go

    # -------------------------------------------------------------------------

    # Build the token shared secret: email + "HENNGECHALLENGE004"
    totp_secret = email + "HENNGECHALLENGE004"

    # Generate the 10-digit TOTP password
    totp_password = generate_totp(totp_secret)

    # Build HTTP Basic Auth header: base64(email:totp_password)
    credentials = base64.b64encode(f"{email}:{totp_password}".encode("utf-8")).decode("utf-8")

    # Build the JSON payload
    payload = json.dumps({
        "github_url": github_url,
        "contact_email": email,
        "solution_language": solution_language
    }).encode("utf-8")

    # Target API endpoint
    url = "https://api.challenge.hennge.com/challenges/backend-recursion/004"

    # Build and send the POST request
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {credentials}"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            body = response.read().decode("utf-8")
            print(f"Status: {response.status}")
            print(f"Response: {body}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response: {body}")


if __name__ == "__main__":
    main()