CREATE TABLE air_quality (
    id SERIAL PRIMARY KEY,
    location VARCHAR(100),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    elevation DOUBLE PRECISION,
    utc_offset_seconds INT,
    current_time TIMESTAMP WITH TIME ZONE,
    pm10 DOUBLE PRECISION,
    pm2_5 DOUBLE PRECISION,
    ozone DOUBLE PRECISION,
    carbon_monoxide DOUBLE PRECISION,
    nitrogen_dioxide DOUBLE PRECISION,
    sulphur_dioxide DOUBLE PRECISION,
    uv_index DOUBLE PRECISION
);

-- Optional: insert some seed rows
INSERT INTO air_quality 
(location, latitude, longitude, elevation, utc_offset_seconds, current_time, pm10, pm2_5, ozone, carbon_monoxide, nitrogen_dioxide, sulphur_dioxide, uv_index) 
VALUES
('Nairobi', -1.286389, 36.817223, 1795, 10800, NOW(), 45.2, 30.1, 12.5, 0.4, 18.2, 5.1, 8.0),
('Kisumu', -0.091702, 34.7680, 1131, 10800, NOW(), 60.3, 40.5, 15.7, 0.6, 22.4, 6.3, 9.1);
