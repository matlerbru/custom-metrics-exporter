from collections import namedtuple

import paramiko


class SSH:

    Result = namedtuple("Result", ["stdout", "stderr"])

    def __init__(self, host: str, username: str, password: str, port: int = 22) -> None:

        self._client = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(
            hostname=host, username=username, password=password, port=port
        )

    def execute_command(self, command: str) -> Result:

        stdin, stdout, stderr = self._client.exec_command(command)
        return self.Result(stdout=stdout.read().decode(), stderr=stderr.read().decode())

    def close(self) -> None:
        self._client.close()
