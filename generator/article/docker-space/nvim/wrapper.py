import os
import platform
from logging import getLogger
from pathlib import Path
from subprocess import PIPE, Popen, TimeoutExpired, check_output, run

log = getLogger(__name__)

PathLike = str | Path


class DockerWrapper:
    def __init__(self, container: str, workdir: PathLike):
        self.name = container
        self.workdir = Path(workdir)

    def build(self):
        check_output(
            [
                *("docker", "build"),
                *("--tag", self.name),
                str(Path(__file__).parent.absolute()),
            ]
        )

    def exists(self):
        return bool(check_output(["docker", "image", "ls", self.name, "-q"]))

    def run(self, *args: str, timeout: float | None = None) -> None:
        work = "/work"
        docker = [
            *("docker", "run", "--tty", "--rm", "--interactive", "--init"),
            *("--name", self.name),
            *("--workdir", work),
            *("--mount", f"type=bind,src={self.workdir!s},target={work}"),
            *self._linux_workaround(),
            self.name,
        ]
        self._process(*docker, *args, timeout=timeout)

    def _process(self, *cmd: str, timeout: float | None) -> None:
        with Popen(cmd) as process:  # type: ignore  # noqa: S603
            try:
                process.communicate(timeout=timeout)
            except KeyboardInterrupt as e:
                raise SystemExit(1) from e
            except TimeoutExpired as e:
                process.terminate()
                run(["docker", "kill", self.name], stdout=PIPE, check=True)  # noqa: S607, S603
                raise SystemExit(1) from e
            raise SystemExit(process.returncode)

    def _linux_workaround(self) -> tuple[str, ...]:
        if platform.system() != "Windows":
            return ("--user", f"{os.getuid()}:{os.getgid()}", "--group-add", f"{os.getgid()}")  # type: ignore
        else:
            return ()
