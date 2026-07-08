def analyze_ticket(text):

    text = text.lower()

    if "ransomware" in text:
        return {
            "priority": "High",
            "category": "Ransomware",
            "reply": (
                " Possible ransomware detected.\n\n"
                "Disconnect the affected computer from the network immediately.\n"
                "Do not pay the ransom.\n"
                "Wait for a CyberShield analyst."
            ),
        }

    elif "phishing" in text:
        return {
            "priority": "High",
            "category": "Phishing",
            "reply": (
                " Possible phishing attack.\n\n"
                "Avoid clicking any links.\n"
                "Do not enter passwords.\n"
                "Forward the suspicious email to our analysts."
            ),
        }

    elif "virus" in text or "malware" in text:
        return {
            "priority": "Medium",
            "category": "Malware",
            "reply": (
                "Possible malware infection.\n\n"
                "Disconnect from the internet.\n"
                "Run a trusted antivirus scan.\n"
                "Our analysts will investigate."
            ),
        }

    else:
        return {
            "priority": "Low",
            "category": "General Support",
            "reply": (
                "Thank you for contacting CyberShield.\n"
                "Your ticket has been received and will be reviewed shortly."
            ),
        }