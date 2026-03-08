import os

os.environ['DEMO_MODE'] = 'true'

from discord_alert import alert_sweep_detected

alert_sweep_detected("Test alert")

print("Test completed")