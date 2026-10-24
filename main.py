def call_gemini_api(prompt, inventory_context, training_context, rules, api_key):
    key_to_use = api_key or default_api_key
    if not key_to_use:
        return "⚠️ Please enter your API Key / Token in the Settings tab!"
    
    try:
        system_instruction = f"{rules}\n\nMANUAL TRAINING / FAQ:\n{training_context}\n\nINVENTORY:\n{inventory_context}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_instruction}\n\nCustomer Message: {prompt}"}
                    ]
                }
            ]
        }

        # Route AQ... enterprise tokens through the Vertex AI endpoint for project 532407509088
        if key_to_use.startswith("AQ."):
            url = "https://aiplatform.googleapis.com/v1/projects/532407509088/locations/us-central1/publishers/google/models/gemini-1.5-flash:generateContent"
            headers = {
                'Authorization': f'Bearer {key_to_use}',
                'Content-Type': 'application/json'
            }
            response = requests.post(url, headers=headers, json=payload)
        else:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
            headers = {'Content-Type': 'application/json'}
            params = {'key': key_to_use}
            response = requests.post(url, headers=headers, params=params, json=payload)
            
        res_data = response.json()
        
        if response.status_code == 200:
            candidates = res_data.get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"]
            return "No response generated."
        else:
            error_msg = res_data.get("error", {}).get("message", response.text)
            return f"API Error ({response.status_code}): {error_msg}"
            
    except Exception as e:
        return f"Error connecting to Gemini API: {e}"
