from configuration import get_config, Config
from log_util import now
from pythonping import ping
from send_mail import send_email
import time


def is_ip_reachable(ip):
    # Timeout is in seconds
    response = ping(ip, timeout=1, count=5)
    return response.success()


def main():
    config: Config = get_config()
    failures = 0
    warning_email_sent = False
    while True:
        if not is_ip_reachable(config.monitoring.target_ip):
            failures += 1
            print(f"[{now()}] IP {config.monitoring.target_ip} is not reachable.")
            if failures > config.monitoring.failures_allowed:
                print(f"[{now()}] Will send email to {len(config.email.recipients)} recipients.")
                for recipient in config.email.recipients:
                    send_email(
                        config.email.sender,
                        recipient,
                        "Freezer plug is offline!",
                        "Go check it!",
                        config,
                    )
                    warning_email_sent = True
                    failures = 0
        else:
            failures = 0
            print(f"[{now()}] IP {config.monitoring.target_ip} is reachable.")
            if warning_email_sent:
                for recipient in config.email.recipients:
                    send_email(
                        config.email.sender,
                        recipient,
                        "Freezer plug has come back online.",
                        "Phew.",
                    )
                    warning_email_sent = False
        if failures == 0:
            print(f"[{now()}] Sleeping for {config.monitoring.check_interval}s.")
            time.sleep(config.monitoring.check_interval)


if __name__ == "__main__":
    main()
