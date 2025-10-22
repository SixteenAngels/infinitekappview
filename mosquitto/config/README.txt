Provide TLS files in this directory:
- ca.crt
- server.crt
- server.key

Create credentials with:
  docker run --rm -it -v $(pwd)/mosquitto/config:/work eclipse-mosquitto:2 mosquitto_passwd -c /work/passwords.txt youruser

Update API env vars MQTT_USERNAME and MQTT_PASSWORD accordingly.
