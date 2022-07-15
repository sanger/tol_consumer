import json
import os
import stat
import subprocess
import urllib.request

RABBITMQ_ADMIN_FILE = "rabbitmqadmin"

HOST = "localhost"
PORT = "8080"
USERNAME = "admin"
PASSWORD = "development"

VHOST = "tol"
EXCHANGE_TYPE = "topic"
AE_EXCHANGE_TYPE = "fanout"
DL_EXCHANGE_TYPE = "topic"
QUEUE_TYPE = "classic"

DL_EXCHANGE = "tol.dead-letters"
CRUD_DL_QUEUE = "tol.crud-operations.dead-letters"
FEEDBACK_DL_QUEUE = "tol.feedback.dead-letters"

TOL_TEAM_AE_EXCHANGE = "tol-team.tol.unrouted"
TOL_TEAM_UNROUTED_QUEUE = "tol-team.tol.unrouted"

TOL_TEAM_EXCHANGE = "tol-team.tol"
CRUD_QUEUE = "tol.crud-operations"
CRUD_ROUTING_KEY = "crud.#"

PSD_AE_EXCHANGE = "psd.tol.unrouted"
PSD_UNROUTED_QUEUE = "psd.tol.unrouted"

PSD_EXCHANGE = "psd.tol"
FEEDBACK_QUEUE = "tol.feedback"
FEEDBACK_ROUTING_KEY = "feedback.#"


def print_command_output(specific_command):
    command_parts = [
        f"./{RABBITMQ_ADMIN_FILE}",
        f"--host={HOST}",
        f"--port={PORT}",
        f"--username={USERNAME}",
        f"--password={PASSWORD}",
        f"--vhost={VHOST}",
        *specific_command,
    ]

    print(subprocess.run(command_parts, encoding="utf-8", stdout=subprocess.PIPE).stdout)


print(f"Downloading {RABBITMQ_ADMIN_FILE} tool and setting as executable for your user")
urllib.request.urlretrieve(f"http://{HOST}:{PORT}/cli/{RABBITMQ_ADMIN_FILE}", RABBITMQ_ADMIN_FILE)
st = os.stat(RABBITMQ_ADMIN_FILE)
os.chmod(RABBITMQ_ADMIN_FILE, st.st_mode | stat.S_IXUSR)
print()

print(f"Declaring vhost '{VHOST}'")
print_command_output(["declare", "vhost", f"name={VHOST}"])

print(f"Declaring dead letter exchange '{DL_EXCHANGE}'")
print_command_output(
    [
        "declare",
        "exchange",
        f"name={DL_EXCHANGE}",
        f"type={DL_EXCHANGE_TYPE}",
    ]
)

print(f"Declaring CRUD dead letters queue '{CRUD_DL_QUEUE}'")
print_command_output(
    [
        "declare",
        "queue",
        f"name={CRUD_DL_QUEUE}",
        f"queue_type={QUEUE_TYPE}",
        f'arguments={json.dumps({"x-queue-type": QUEUE_TYPE})}',
    ]
)

print("Declaring CRUD dead letters binding")
print_command_output(
    [
        "declare",
        "binding",
        f"source={DL_EXCHANGE}",
        f"destination={CRUD_DL_QUEUE}",
        f"routing_key={CRUD_ROUTING_KEY}",
    ]
)

print(f"Declaring feedback dead letters queue '{FEEDBACK_DL_QUEUE}'")
print_command_output(
    [
        "declare",
        "queue",
        f"name={FEEDBACK_DL_QUEUE}",
        f"queue_type={QUEUE_TYPE}",
        f'arguments={json.dumps({"x-queue-type": QUEUE_TYPE})}',
    ]
)

print("Declaring feedback dead letters binding")
print_command_output(
    [
        "declare",
        "binding",
        f"source={DL_EXCHANGE}",
        f"destination={FEEDBACK_DL_QUEUE}",
        f"routing_key={FEEDBACK_ROUTING_KEY}",
    ]
)

print(f"Declaring TOL alternate exchange '{TOL_TEAM_AE_EXCHANGE}'")
print_command_output(
    [
        "declare",
        "exchange",
        f"name={TOL_TEAM_AE_EXCHANGE}",
        f"type={AE_EXCHANGE_TYPE}",
    ]
)

print(f"Declaring TOL unrouted queue '{TOL_TEAM_UNROUTED_QUEUE}'")
print_command_output(
    [
        "declare",
        "queue",
        f"name={TOL_TEAM_UNROUTED_QUEUE}",
        f"queue_type={QUEUE_TYPE}",
        f'arguments={json.dumps({"x-queue-type": QUEUE_TYPE})}',
    ]
)

print("Declaring TOL unrouted binding")
print_command_output(
    [
        "declare",
        "binding",
        f"source={TOL_TEAM_AE_EXCHANGE}",
        f"destination={TOL_TEAM_UNROUTED_QUEUE}",
    ]
)

print(f"Declaring TOL exchange '{TOL_TEAM_EXCHANGE}'")
print_command_output(
    [
        "declare",
        "exchange",
        f"name={TOL_TEAM_EXCHANGE}",
        f"type={EXCHANGE_TYPE}",
        f'arguments={json.dumps({"alternate-exchange": TOL_TEAM_AE_EXCHANGE})}',
    ]
)

print(f"Declaring CRUD queue '{CRUD_QUEUE}'")
print_command_output(
    [
        "declare",
        "queue",
        f"name={CRUD_QUEUE}",
        f"queue_type={QUEUE_TYPE}",
        f'arguments={json.dumps({"x-queue-type": QUEUE_TYPE, "x-dead-letter-exchange": DL_EXCHANGE})}',
    ]
)

print("Declaring CRUD binding")
print_command_output(
    [
        "declare",
        "binding",
        f"source={TOL_TEAM_EXCHANGE}",
        f"destination={CRUD_QUEUE}",
        f"routing_key={CRUD_ROUTING_KEY}",
    ]
)

print(f"Declaring PSD alternate exchange '{PSD_AE_EXCHANGE}'")
print_command_output(
    [
        "declare",
        "exchange",
        f"name={PSD_AE_EXCHANGE}",
        f"type={AE_EXCHANGE_TYPE}",
    ]
)

print(f"Declaring PSD unrouted queue '{PSD_UNROUTED_QUEUE}'")
print_command_output(
    [
        "declare",
        "queue",
        f"name={PSD_UNROUTED_QUEUE}",
        f"queue_type={QUEUE_TYPE}",
        f'arguments={json.dumps({"x-queue-type": QUEUE_TYPE})}',
    ]
)

print("Declaring TOL unrouted binding")
print_command_output(
    [
        "declare",
        "binding",
        f"source={PSD_AE_EXCHANGE}",
        f"destination={PSD_UNROUTED_QUEUE}",
    ]
)

print(f"Declaring feedback exchange '{PSD_EXCHANGE}'")
print_command_output(
    [
        "declare",
        "exchange",
        f"name={PSD_EXCHANGE}",
        f"type={EXCHANGE_TYPE}",
        f'arguments={json.dumps({"alternate-exchange": PSD_AE_EXCHANGE})}',
    ]
)

print(f"Declaring feedback queue '{FEEDBACK_QUEUE}'")
print_command_output(
    [
        "declare",
        "queue",
        f"name={FEEDBACK_QUEUE}",
        f"queue_type={QUEUE_TYPE}",
        f'arguments={json.dumps({"x-queue-type": QUEUE_TYPE, "x-dead-letter-exchange": DL_EXCHANGE})}',
    ]
)

print("Declaring feedback binding")
print_command_output(
    [
        "declare",
        "binding",
        f"source={PSD_EXCHANGE}",
        f"destination={FEEDBACK_QUEUE}",
        f"routing_key={FEEDBACK_ROUTING_KEY}",
    ]
)
