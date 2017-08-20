# Led

**run via docker**
```bash
docker run -d --device /dev/gpiomem -v /home/pi/pwm_led.py:/home/pwm_led.py -w /home raspbian-service:1.0 pwm_led .py
```
