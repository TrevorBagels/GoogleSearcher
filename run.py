from main import Bot
import time, random, signal
b = Bot()
signal.signal(signal.SIGINT, b.exit)
while True:
	b.run(b.config["searchterm"], b.config["targetlink"])
	waitTime = max(b.config["averageinterval"] + random.randrange(-b.config["intervalrange"], b.config["intervalrange"]), b.config['mininterval'])
	b.log(f"Waiting for {waitTime} second(s) before running again.", verbosity=1)
	time.sleep(waitTime)
