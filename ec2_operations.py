import os
import json
import argparse
import datetime
import sys
import sh
import logging
import time

polls = 10
interval = 10  # seconds


# ---------------- LOGGING ----------------
def setup_logging():
    timestamp = datetime.datetime.now().strftime("%H_%M_%S")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - line %(lineno)d - %(message)s"
    )

    file_handler = logging.FileHandler(f"ec2_operations_{timestamp}.log")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# ---------------- AUTH ----------------
def authentication(params):
    try:
        logging.info("Starting AWS authentication")

        for key in ["key_id", "access_key", "region"]:
            if not params.get(key):
                raise ValueError(f"Missing parameter: {key}")

        os.environ["AWS_ACCESS_KEY_ID"] = params["key_id"]
        os.environ["AWS_SECRET_ACCESS_KEY"] = params["access_key"]
        os.environ["AWS_DEFAULT_REGION"] = params["region"]
        os.environ["AWS_PAGER"] = ""

        logging.info("AWS authentication successful")

    except Exception:
        logging.exception("AWS authentication failed")
        sys.exit(1)


# ---------------- TAG HELPER ----------------
def get_instance_name(tags):
    if not tags:
        return "N/A"
    for tag in tags:
        if tag.get("Key") == "Name":
            return tag.get("Value", "N/A")
    return "N/A"


# ---------------- STATE CHECK ----------------
def describe_instance_states(params):
    try:
        logging.info(f"Checking state for instances: {params['instance_id']}")

        result = sh.aws(
            "ec2", "describe-instances",
            "--instance-ids", *params["instance_id"]
        )

        data = json.loads(str(result))
        states = {}

        for reservation in data.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                states[instance["InstanceId"]] = instance["State"]["Name"]

        logging.info(f"Current states: {states}")
        return states

    except Exception:
        logging.exception("Failed to fetch instance states")
        return {}


# ---------------- MONITOR ----------------
def monitor(params, out, desired_state):
    try:
        for _ in range(polls):
            states = describe_instance_states(params)

            if states and all(
                state.lower() == desired_state.lower()
                for state in states.values()
            ):
                logging.info(f"All instances reached state: {desired_state}")
                describe_instances(params, out)
                return True

            logging.info(f"Waiting... current={states}, target={desired_state}")
            time.sleep(interval)

        logging.warning("Timeout waiting for desired state")
        return False

    except Exception:
        logging.exception("Monitoring failed")
        return False


# ---------------- OPERATIONS ----------------
def operation_instances(params, out, desired_state):
    try:
        logging.info(
            f"Performing '{params['operation']}' on instances {params['instance_id']}"
        )

        sh.aws(
            "ec2",
            f"{params['operation']}-instances",
            "--instance-ids", *params["instance_id"]
        )

        return monitor(params, out, desired_state)

    except Exception:
        logging.exception("EC2 operation failed")
        return False


# ---------------- DESCRIBE ----------------
def describe_instances(params, out):
    try:
        logging.info("Fetching EC2 instance details")

        result = sh.aws(
            "ec2", "describe-instances",
            "--instance-ids", *params["instance_id"]
        )

        data = json.loads(str(result))

        for reservation in data.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                info = {
                    "InstanceId": instance.get("InstanceId", "N/A"),
                    "Name": get_instance_name(instance.get("Tags")),
                    "State": instance.get("State", {}).get("Name", "N/A"),
                    "Private IP": instance.get("PrivateIpAddress", "N/A"),
                    "Public IP": instance.get("PublicIpAddress", "N/A"),
                }
                out.append(info)
                logging.info(f"Instance found: {info['InstanceId']}")

    except Exception:
        logging.exception("Failed to describe instances")


# ---------------- MAIN ----------------
def main():
    try:
        parser = argparse.ArgumentParser(
            description="EC2 operations using AWS CLI"
        )

        parser.add_argument("--key_id", required=True)
        parser.add_argument("--access_key", required=True)
        parser.add_argument("--region", required=True)
        parser.add_argument(
            "--operation",
            required=True,
            choices=["start", "stop", "reboot", "terminate"]
        )
        parser.add_argument(
            "--instance_id",
            nargs="+",
            required=True,
            help="One or more EC2 instance IDs"
        )

        params = vars(parser.parse_args())
        out = []

        setup_logging()
        logging.info("Script started")

        STATE_MAP = {
            "start": "running",
            "stop": "stopped",
            "reboot": "running",
            "terminate": "terminated"
        }

        desired_state = STATE_MAP[params["operation"]]

        authentication(params)
        operation_instances(params, out, desired_state)

        logging.info("Execution completed")
        print(json.dumps(out, indent=4))

    except Exception:
        logging.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
