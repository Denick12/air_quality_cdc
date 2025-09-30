import json
import os
import psycopg2
from kafka import KafkaConsumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC", "airquality.public.air_quality")

TS_HOST = os.getenv("TIMESCALE_HOST", "timescaledb")
TS_DB = os.getenv("TIMESCALE_DB", "metrics")
TS_USER = os.getenv("TIMESCALE_USER", "grafana")
TS_PASSWORD = os.getenv("TIMESCALE_PASSWORD", "grafana")

conn = psycopg2.connect(
    host=TS_HOST,
    dbname=TS_DB,
    user=TS_USER,
    password=TS_PASSWORD,
)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS air_quality_timescale (
    id SERIAL PRIMARY KEY,
    location TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    elevation DOUBLE PRECISION,
    utc_offset_seconds INT,
    current_time TIMESTAMP,
    pm10 DOUBLE PRECISION,
    pm2_5 DOUBLE PRECISION,
    ozone DOUBLE PRECISION,
    carbon_monoxide DOUBLE PRECISION,
    nitrogen_dioxide DOUBLE PRECISION,
    sulphur_dioxide DOUBLE PRECISION,
    uv_index DOUBLE PRECISION
);
""")
conn.commit()

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
)

print(f"✅ Listening to Kafka topic: {KAFKA_TOPIC}")

for message in consumer:
    payload = message.value
    after = payload.get("payload", {}).get("after")
    if after:
        cur.execute("""
        INSERT INTO air_quality_timescale (
            location, latitude, longitude, elevation, utc_offset_seconds,
            current_time, pm10, pm2_5, ozone, carbon_monoxide,
            nitrogen_dioxide, sulphur_dioxide, uv_index
        ) VALUES (
            %(location)s, %(latitude)s, %(longitude)s, %(elevation)s, %(utc_offset_seconds)s,
            %(current_time)s, %(pm10)s, %(pm2_5)s, %(ozone)s, %(carbon_monoxide)s,
            %(nitrogen_dioxide)s, %(sulphur_dioxide)s, %(uv_index)s
        )
        """, after)
        conn.commit()
        print(f"Inserted record at {after.get('current_time')}")
