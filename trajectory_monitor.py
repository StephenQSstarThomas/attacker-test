import json
import time
from pathlib import Path

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:  # Fallback if watchdog is not installed
    Observer = None
    FileSystemEventHandler = object


class TrajectoryHandler(FileSystemEventHandler):
    """Watches for new trajectory files and processes them."""

    def __init__(self, directory: Path):
        self.directory = directory

    def on_created(self, event):
        path = Path(event.src_path)
        if path.suffix == ".json":
            self.process_file(path)

    def process_file(self, path: Path):
        try:
            with path.open() as f:
                data = json.load(f)
        except Exception as exc:
            print(f"Failed to load {path}: {exc}")
            return
        print(f"Loaded {path} with {len(data)} records")
        # Example rule-based check for suspicious patterns
        for entry in data:
            if entry.get("source") == "user" and "${" in entry.get("message", ""):
                print(f"Potential injection in {path}: {entry['message']}")


def watch(directory: Path):
    if Observer is None:
        print("watchdog not installed; falling back to polling")
        known = set(Path(directory).glob("*.json"))
        while True:
            current = set(Path(directory).glob("*.json"))
            for path in current - known:
                TrajectoryHandler(directory).process_file(path)
            known = current
            time.sleep(2)
    else:
        event_handler = TrajectoryHandler(directory)
        observer = Observer()
        observer.schedule(event_handler, str(directory), recursive=False)
        observer.start()
        print(f"Watching {directory} for new trajectory files...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    watch(Path("trajectories"))
