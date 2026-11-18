import os

import redis
from flask import Flask, jsonify

app = Flask(__name__)

redis_client = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    decode_responses=True,
)


@app.get("/api/data")
def get_data():
    message = "Hello from Docker Compose"
    redis_client.set("message", message)
    stored_message = redis_client.get("message")

    return jsonify(
        {
            "message": stored_message,
            "status": "Success",
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
