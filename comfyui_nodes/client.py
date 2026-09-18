from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

SERVICE_CONFIGURED = bool(os.environ.get("YUE2_SERVICE"))
SERVICE = os.environ.get("YUE2_SERVICE", "http://127.0.0.1:8189").rstrip("/")
__version__ = "1.5.13"


def find_root() -> Path:
    if os.environ.get("YUE2_HOME"):
        return Path(os.environ["YUE2_HOME"]).expanduser().resolve()
    marker = Path(__file__).with_name("yue2_home.txt")
    if marker.is_file():
        return Path(marker.read_text(encoding="utf-8-sig").strip()).expanduser().resolve()
    node_root = Path(__file__).resolve().parent
    for local in (node_root, node_root.parent):
        if (local / "app" / "yue2_app").is_dir():
            return local
    raise FileNotFoundError("Cannot find the YuE2 node directory; set YUE2_HOME")


def request(path: str, method="GET", data=None, timeout=30):
    body = None if data is None else json.dumps(data, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"} if body is not None else {}
    message = urllib.request.Request(SERVICE + path, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(message, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            detail = json.loads(exc.read().decode("utf-8")).get("error")
        except Exception:
            detail = str(exc)
        raise RuntimeError(detail) from exc


def validate_health(health: dict) -> dict:
    if not isinstance(health, dict) or health.get("ok") is not True:
        raise RuntimeError(f"{SERVICE} is not a valid YuE2 service")
    if health.get("version") != __version__:
        raise RuntimeError(
            f"YuE2 service version at {SERVICE} is {health.get('version')!r}, but the node version is {__version__}; "
            "run stop_service.bat first, then retry"
        )
    if not SERVICE_CONFIGURED:
        expected = find_root().resolve()
        try:
            actual = Path(str(health["root"])).resolve()
        except (KeyError, OSError, ValueError) as exc:
            raise RuntimeError(f"{SERVICE} returned an invalid installation directory") from exc
        if actual != expected:
            raise RuntimeError(
                f"Port 8189 is already used by another YuE2 installation: {actual}; current node directory is {expected}. "
                "Stop the other service or set YUE2_SERVICE explicitly"
            )
    return health


def ensure_service(timeout=30):
    try:
        health = request("/api/health", timeout=2)
    except Exception as exc:
        if SERVICE_CONFIGURED:
            raise RuntimeError(f"Cannot connect to the explicitly configured YuE2 service {SERVICE}") from exc
    else:
        return validate_health(health)

    root = find_root()
    python = root / "runtime" / "python.exe"
    if not python.is_file():
        raise RuntimeError(f"YuE2 runtime is not installed; run the runtime installer (安装运行环境.bat) in {root}")
    environment = os.environ.copy()
    environment.update({"YUE2_HOME": str(root), "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8",
                        "PLAYWRIGHT_BROWSERS_PATH": str(root / "runtime" / "playwright")})
    environment["PATH"] = str(root / "runtime" / "ffmpeg") + os.pathsep + environment.get("PATH", "")
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    logs = root / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    with (logs / "service.stdout.log").open("ab") as stdout, (logs / "service.stderr.log").open("ab") as stderr:
        subprocess.Popen([str(python), "-X", "utf8", "-m", "app.yue2_app.service"], cwd=root,
                         env=environment, creationflags=flags, stdout=stdout, stderr=stderr)
    started = time.monotonic()
    while time.monotonic() - started < timeout:
        try:
            health = request("/api/health", timeout=2)
        except Exception:
            time.sleep(0.4)
            continue
        return validate_health(health)
    raise RuntimeError("YuE2 service startup timed out; check logs/service.stderr.log")


def submit(kind: str, payload: dict) -> dict:
    ensure_service()
    return request("/api/jobs", method="POST", data={"kind": kind, "request": payload, "source": "comfyui"})


def cancel(job_id: str, force=False):
    return request(f"/api/jobs/{job_id}/cancel", method="POST", data={"force": force})


def wait(job_id: str, interval=0.8) -> dict:
    while True:
        status = request(f"/api/jobs/{job_id}")
        if status.get("status") == "complete":
            return status
        if status.get("status") in {"failed", "cancelled"}:
            raise RuntimeError(status.get("error") or status["status"])
        try:
            import comfy.model_management
            comfy.model_management.throw_exception_if_processing_interrupted()
        except ImportError:
            pass
        except BaseException:
            try:
                cancel(job_id)
            finally:
                raise
        time.sleep(interval)


def run(kind: str, payload: dict) -> dict:
    return wait(submit(kind, payload)["id"])
