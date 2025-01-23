import json
import http.client

def normalize_ateco(codice_raw):
    """
    Esempio di normalizzazione del codice ATECO:
      - Se un solo carattere, anteponi '0'
      - Se lunghezza >=2, inserisci '.' dopo la 2a e la 5a cifra
    """
    if not codice_raw:
        return ''
    codice_raw = codice_raw.strip()

    if len(codice_raw) == 1:
        return '0' + codice_raw

    chars = list(codice_raw)
    if len(chars) > 2:
        chars.insert(2, '.')
    if len(chars) > 5:
        chars.insert(5, '.')
    
    return "".join(chars)


def connection_openapi(tool, partitaiva):
    """
    Se tool == "1": utilizza Creditsafe (sandbox).
    Se tool == "2": utilizza OpenAPI (imprese.openapi.it).
    """
    data = None
    conn = None

    if tool == "1":
        # ========== CREDITSAFE ==========
        try:
            # 1) Autenticazione per ottenere token
            conn = http.client.HTTPSConnection("connect.sandbox.creditsafe.com")
            payload = json.dumps({
                "username": "r.decaro@psbsrl.it",
                "password": "3qJdeZkf6Tr-u3^05Ia2"
            })
            headers = {
                'Content-Type': 'application/json'
            }
            conn.request("POST", "/v1/authenticate", payload, headers)
            res = conn.getresponse()
            raw_data = res.read()
            data_auth = json.loads(raw_data)

            # Estraggo il token
            token = data_auth["token"]
        except Exception as e:
            raise Exception(f"Errore durante l'autenticazione Creditsafe: {e}")
        finally:
            if conn:
                conn.close()

        try:
            # 2) Chiamata successiva con token
            conn = http.client.HTTPSConnection("connect.sandbox.creditsafe.com")
            headers = {
                'Authorization': 'Bearer ' + token
            }
            endpoint = f"/v1/companies?countries=IT&vatNo={partitaiva}"
            conn.request("GET", endpoint, '', headers)
            res = conn.getresponse()
            raw_data = res.read()
            data = json.loads(raw_data)
        except Exception as e:
            raise Exception(f"Errore durante la richiesta Creditsafe: {e}")
        finally:
            if conn:
                conn.close()

    elif tool == "2":
        # ========== OPENAPI (imprese.openapi.it) ==========
        try:
            conn = http.client.HTTPSConnection("imprese.openapi.it")
            payload = ''
            headers = {
                'Accept': 'application/json',
                'OPENAPI_USERNAME': 'amministrazione@inforise.it',
                'OPENAPI_APIKEY': '3570453be4a544ec3e2193517bd562cd',
                'OPENAPI_TOKEN': '67922323176bf533dd0b766a',
                'Authorization': 'Bearer 67922323176bf533dd0b766a',
                # 'Cookie': 'avpayCustomerCookie=edafa7c38327e94557d79c6880e50189',
                # 'Host': 'imprese.openapi.it',  # se necessario
            }

            endpoint = f"/advance/{partitaiva}"
            conn.request("GET", endpoint, payload, headers)
            response = conn.getresponse()

            print("HTTP Status:", response.status)
            print("HTTP Reason:", response.reason)

            raw_data = response.read()
            print("Raw data from server:", raw_data)

            data = json.loads(raw_data)
        except Exception as e:
            raise Exception(f"Errore durante la richiesta OpenAPI: {e}")
        finally:
            if conn:
                conn.close()
    else:
        raise ValueError("Opzione 'tool' non valida (accetta solo '1' o '2').")

    return data
