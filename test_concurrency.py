import threading
import requests
URL = "http://127.0.0.1:8000/booking"

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidHlwZSI6ImFjY2VzcyIsImV4cCI6MTc4NTIyMTQyOX0.tlh8LCfKKlrVs6fITFuYLC2bLNA5H2GMBdDjRdkaBcc"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

payload = {
    "seat_id": 3      # Use an unbooked seat
}


def book():
    response = requests.post(
        URL,
        headers=headers,
        json=payload,
    )

    print(
        threading.current_thread().name,
        response.status_code,
        response.text,
    )


threads = []

for i in range(10):
    t = threading.Thread(target=book)
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

print("Finished")