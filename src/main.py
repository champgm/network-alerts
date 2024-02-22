from configuration import get_config, Config
from log_util import now
from pythonping import ping
from send_mail import send_email
import time


def ip_is_reachable(ip):
    # Timeout is in seconds
    response = ping(ip, timeout=1, count=5)
    return response.success()


def send_warning(config: Config):
    print(f"[{now()}] Will send WARNING email to {len(config.email.recipients)} recipients.")
    for recipient in config.email.recipients:
        send_email(
            config.email.sender,
            recipient,
            "Freezer plug is offline!",
            "Go check it!",
            config,
        )


def send_all_clear(config: Config):
    print(f"[{now()}] Will send ALL CLEAR email to {len(config.email.recipients)} recipients.")
    for recipient in config.email.recipients:
        send_email(
            config.email.sender,
            recipient,
            "Freezer plug has come back online.",
            "Phew.",
            config,
        )


def main():
    config: Config = get_config()
    failures = 0
    warning_email_sent = False
    while True:
        if not ip_is_reachable(config.monitoring.target_ip):
            print(f"[{now()}] IP {config.monitoring.target_ip} is not reachable.")
            failures += 1
            if failures > config.monitoring.failures_allowed:
                send_warning(config)
                warning_email_sent = True
                failures = 0
        else:
            print(f"[{now()}] IP {config.monitoring.target_ip} is reachable.")
            failures = 0
            if warning_email_sent:
                send_all_clear(config)
                warning_email_sent = False

        if failures == 0:
            print(f"[{now()}] Sleeping for {config.monitoring.check_interval}s.")
            time.sleep(config.monitoring.check_interval)


if __name__ == "__main__":
    main()
