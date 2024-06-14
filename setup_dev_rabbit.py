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


class RabbitSetupTool:
    def __init__(self, vhost):
        self.vhost = vhost

    def setup(self):
        self._download_rabbitmq_admin_tool()
        self._declare_vhost()

    def _download_rabbitmq_admin_tool(self):
        print(f"Downloading {RABBITMQ_ADMIN_FILE} tool and setting as executable for your user")
        urllib.request.urlretrieve(f"http://{HOST}:{PORT}/cli/{RABBITMQ_ADMIN_FILE}", RABBITMQ_ADMIN_FILE)
        st = os.stat(RABBITMQ_ADMIN_FILE)
        os.chmod(RABBITMQ_ADMIN_FILE, st.st_mode | stat.S_IXUSR)
        print()

    def _print_command_output(self, specific_command):
        command_parts = [
            f"./{RABBITMQ_ADMIN_FILE}",
            f"--host={HOST}",
            f"--port={PORT}",
            f"--username={USERNAME}",
            f"--password={PASSWORD}",
            f"--vhost={self.vhost}",
            *specific_command,
        ]

        print(subprocess.run(command_parts, encoding="utf-8", stdout=subprocess.PIPE).stdout)

    def _declare_vhost(self):
        print(f"Declaring vhost '{self.vhost}'")
        self._print_command_output(["declare", "vhost", f"name={self.vhost}"])

    def _declare_exchange(self, name, type, arguments=None):
        print(f"Declaring exchange '{name}'")

        command = [
            "declare",
            "exchange",
            f"name={name}",
            f"type={type}",
        ]

        if arguments is not None:
            command.append(f"arguments={json.dumps(arguments)}")

        self._print_command_output(command)

    def _declare_queue(self, name, queue_type, arguments=None):
        print(f"Declaring queue '{name}'")

        command = [
            "declare",
            "queue",
            f"name={name}",
            f"queue_type={queue_type}",
        ]

        if arguments is not None:
            command.append(f"arguments={json.dumps(arguments)}")

        self._print_command_output(command)

    def _declare_binding(self, source, destination, routing_key=None, arguments=None):
        print(f"Declaring binding from '{source}' to '{destination}'")

        command = [
            "declare",
            "binding",
            f"source={source}",
            f"destination={destination}",
        ]

        if routing_key is not None:
            command.append(f"routing_key={routing_key}")

        if arguments is not None:
            command.append(f"arguments={json.dumps(arguments)}")

        self._print_command_output(command)


class CreateUpdateMessagesRabbitSetupTool(RabbitSetupTool):
    def __init__(self):
        self.VHOST = "tol"
        super().__init__(self.VHOST)

        self.EXCHANGE_TYPE = "topic"
        self.AE_EXCHANGE_TYPE = "fanout"
        self.DL_EXCHANGE_TYPE = "topic"
        self.QUEUE_TYPE = "classic"

        self.DL_EXCHANGE = "tol.dead-letters"
        self.CRUD_DL_QUEUE = "tol.crud-operations.dead-letters"
        self.FEEDBACK_DL_QUEUE = "tol.feedback.dead-letters"

        self.TOL_TEAM_AE_EXCHANGE = "tol-team.tol.unrouted"
        self.TOL_TEAM_UNROUTED_QUEUE = "tol-team.tol.unrouted"

        self.TOL_TEAM_EXCHANGE = "tol-team.tol"
        self.CRUD_QUEUE = "tol.crud-operations"
        self.CRUD_ROUTING_KEY = "crud.#"

        self.PSD_AE_EXCHANGE = "psd.tol.unrouted"
        self.PSD_UNROUTED_QUEUE = "psd.tol.unrouted"

        self.PSD_EXCHANGE = "psd.tol"
        self.FEEDBACK_QUEUE = "tol.feedback"
        self.FEEDBACK_ROUTING_KEY = "feedback.#"

    def setup(self):
        super().setup()

        # Dead letter exchange
        self._declare_exchange(self.DL_EXCHANGE, self.DL_EXCHANGE_TYPE)

        # CRUD dead letter queue
        self._declare_queue(self.CRUD_DL_QUEUE, self.QUEUE_TYPE, {"x-queue-type": self.QUEUE_TYPE})
        self._declare_binding(self.DL_EXCHANGE, self.CRUD_DL_QUEUE, routing_key=self.CRUD_ROUTING_KEY)

        # Feedback dead letter queue
        self._declare_queue(self.FEEDBACK_DL_QUEUE, self.QUEUE_TYPE, {"x-queue-type": self.QUEUE_TYPE})
        self._declare_binding(self.DL_EXCHANGE, self.FEEDBACK_DL_QUEUE, routing_key=self.FEEDBACK_ROUTING_KEY)

        # TOL team alternate exchange
        self._declare_exchange(self.TOL_TEAM_AE_EXCHANGE, self.AE_EXCHANGE_TYPE)
        self._declare_queue(self.TOL_TEAM_UNROUTED_QUEUE, self.QUEUE_TYPE, {"x-queue-type": self.QUEUE_TYPE})
        self._declare_binding(self.TOL_TEAM_AE_EXCHANGE, self.TOL_TEAM_UNROUTED_QUEUE)

        # TOL team exchange
        self._declare_exchange(
            self.TOL_TEAM_EXCHANGE,
            self.EXCHANGE_TYPE,
            {"alternate-exchange": self.TOL_TEAM_AE_EXCHANGE},
        )
        self._declare_queue(
            self.CRUD_QUEUE,
            self.QUEUE_TYPE,
            {"x-queue-type": self.QUEUE_TYPE, "x-dead-letter-exchange": self.DL_EXCHANGE},
        )
        self._declare_binding(self.TOL_TEAM_EXCHANGE, self.CRUD_QUEUE, routing_key=self.CRUD_ROUTING_KEY)

        # PSD alternate exchange
        self._declare_exchange(self.PSD_AE_EXCHANGE, self.AE_EXCHANGE_TYPE)
        self._declare_queue(self.PSD_UNROUTED_QUEUE, self.QUEUE_TYPE, {"x-queue-type": self.QUEUE_TYPE})
        self._declare_binding(self.PSD_AE_EXCHANGE, self.PSD_UNROUTED_QUEUE)

        # Feedback exchange
        self._declare_exchange(
            self.PSD_EXCHANGE,
            self.EXCHANGE_TYPE,
            {"alternate-exchange": self.PSD_AE_EXCHANGE},
        )
        self._declare_queue(
            self.FEEDBACK_QUEUE,
            self.QUEUE_TYPE,
            {"x-queue-type": self.QUEUE_TYPE, "x-dead-letter-exchange": self.DL_EXCHANGE},
        )
        self._declare_binding(self.PSD_EXCHANGE, self.FEEDBACK_QUEUE, routing_key=self.FEEDBACK_ROUTING_KEY)


class BioscanPoolXpRabbitSetupTool(RabbitSetupTool):
    def __init__(self):
        super().__init__("tol")

        self.EXCHANGE = "sequencescape"
        self.DL_EXCHANGE = "dead-letters"
        self.HEADERS_EXCHANGE_TYPE = "headers"

        self.QUEUE_TYPE = "classic"
        self.MESSAGE_TTL = 300000  # 5 minutes

        self.CONSUMED_QUEUE_NAME = "tls.poolxp-export-to-traction"
        self.LOGS_QUEUE_NAME = "logs.sequencescape"
        self.DL_QUEUE_NAME = "dead.poolxp-export-to-traction"

        self.SUBJECT = "bioscan-pool-xp-tube-to-traction"

    def setup(self):
        super().setup()

        # Exchanges
        self._declare_exchange(self.EXCHANGE, self.HEADERS_EXCHANGE_TYPE)
        self._declare_exchange(self.DL_EXCHANGE, self.HEADERS_EXCHANGE_TYPE)

        # Queues
        self._declare_queue(
            self.CONSUMED_QUEUE_NAME,
            self.QUEUE_TYPE,
            {"x-queue-type": self.QUEUE_TYPE, "x-dead-letter-exchange": self.DL_EXCHANGE},
        )
        self._declare_queue(
            self.LOGS_QUEUE_NAME, self.QUEUE_TYPE, {"x-queue-type": self.QUEUE_TYPE, "x-message-ttl": self.MESSAGE_TTL}
        )
        self._declare_queue(
            self.DL_QUEUE_NAME, self.QUEUE_TYPE, {"x-queue-type": self.QUEUE_TYPE, "x-message-ttl": self.MESSAGE_TTL}
        )

        # Bindings
        self._declare_binding(self.EXCHANGE, self.CONSUMED_QUEUE_NAME, arguments={"subject": self.SUBJECT})
        self._declare_binding(self.EXCHANGE, self.LOGS_QUEUE_NAME)
        self._declare_binding(self.DL_EXCHANGE, self.DL_QUEUE_NAME, arguments={"subject": self.SUBJECT})


create_update_setup_tool = CreateUpdateMessagesRabbitSetupTool()
create_update_setup_tool.setup()

bioscan_pool_xp_setup_tool = BioscanPoolXpRabbitSetupTool()
bioscan_pool_xp_setup_tool.setup()
