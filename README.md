# network-alerts

## Setup
* Use chocolatey to install python
* Make a virtual environment: `python -m venv env`
* Activate in windows: `.\env\Scripts\activate`
* Install dependency requirements: `pip install -r requirements.txt`
* Update dependency requirements: `pip freeze > requirements.txt`

# Design 

### Let's let GPT pick the language...

```
I want to start a new personal coding project for myself.

Its purpose is to monitor network devices. Specifically, I have an issue with an electrical breaker in my garage on which my chest freezer relies for power. It tends to trip for no apparent reason and cut power to the freezer (and lights in the garage, etc).

I will place a WiFi smart-plug onto the same circuit as the freezer. I will use network configuration to ensure it always has the same IP. On the same network, I have a "closet PC" that I use to automate various tasks and host media for internal use. When that PC starts up (or maybe as part of a scheduled task) this project will begin execution.

Here's a list of what it should do:
  * Run on Windows startup (or a scheduled task)
  * Stay alive, keep running unless interrupted
  * At an interval, check if a configured IP address can be reached
  * Log results a visible console/window
  * If the configured IP is unreachable, use googleapis to send an email from a configured account to a configured address.

My first question for you is, which programming/scripting language do you think would lend itself best to this project?
```

### It's Python (surprise)

```
Given the requirements and the environment (Windows, network monitoring, email notifications), Python stands out as an ideal choice for several reasons:

*blah blah blah*
```

### High level design

* Language: Python
* Configuration: File
* Core Components:
  * Network Monitoring: socket library
  * Logging: logging library
  * Notification System: smtplib (nah, gonna stick with known googleapis workflow)
* Logic: Loop, check, alert, continue

### Result

Yeah, no surprises there. Thanks GPT.
