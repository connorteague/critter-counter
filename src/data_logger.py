"""
Data Logger

Logs events to CSV with motion context and tag information.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, List
import csv


@dataclass
class CattleEvent:
    """
    Single event in the cattle tracking system.

    You will implement fields based on CSV schema:
    - timestamp: When event occurred
    - motion_start: When motion began (for tag events)
    - motion_end: When motion ended (for tag events)
    - tag_id: Tag identifier (None for motion events)
    - direction: ENTRY/EXIT/UNKNOWN (None for motion events)
    - rssi: Signal strength (None for motion events)
    - occurrence_count: How many times tag has been seen
    - event_type: motion_start, motion_end, motion_timeout, tag_detection
    """

    timestamp: datetime
    event_type: str
    motion_start: Optional[datetime] = None
    motion_end: Optional[datetime] = None
    tag_id: Optional[str] = None
    direction: Optional[str] = None
    rssi: Optional[float] = None
    occurrence_count: Optional[int] = None


class DataLogger:
    """
    Log events to CSV file.

    Data structure:
    - log_motion_start(timestamp): Log motion detection
    - log_motion_end(timestamp): Log motion ended
    - log_motion_timeout(timestamp): Log 5s timeout reached
    - log_tag_detection(...): Log tag with direction, RSSI, occurrence
    - get_recent_events(n): Return last N events from CSV
    - _write_event(event): Append event to CSV file

    CSV Schema:
    timestamp,motion_start,motion_end,tag_id,direction,rssi,occurrence_count,event_type
    """

    def __init__(self, log_file: Path = Path("data/events.csv")):
        """
        Initialize data logger.

        Args:
            log_file: Path to CSV file for event logging
        """
        # Create folder if it's missing
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        #File Headers
        self.fieldnames = [
            "timestamp", "motion_start", "motion_end", "tag_id",
            "direction", "rssi", "occurrence_count", "event_type"
        ]
        if not self.log_file.exists():
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()


    def log_motion_start(self, timestamp: Optional[datetime] = None) -> None:
        """
        Log motion detection event.

        Args:
            timestamp: When motion started (defaults to now)
        """
        event = CattleEvent(
            timestamp=timestamp or datetime.now(), event_type="motion_start")
        self._write_event(event)
        # TODO: Log the motion event
        pass

    def log_motion_end(self, timestamp: Optional[datetime] = None) -> None:
        """
        Log motion ended event.

        Args:
            timestamp: When motion ended (defaults to now)
        """
        event = CattleEvent(
            timestamp=timestamp or datetime.now(), event_type="motion_end")
        self._write_event(event)
        # TODO: Log when motion has ended
        pass

    def log_motion_timeout(self, timestamp: Optional[datetime] = None) -> None:
        """
        Log motion timeout event (5s after last motion).

        Args:
            timestamp: When timeout occurred (defaults to now)
        """
        event = CattleEvent(
            timestamp=timestamp or datetime.now(),
            event_type="motion_timeout"
        )
        self._write_event(event)
        # TODO: Log when motion has timed out
        pass

    def log_tag_detection(
        self,
        tag_id: str,
        direction: str,
        rssi: float,
        occurrence_count: int,
        motion_start: datetime,
        motion_end: datetime,
        timestamp: Optional[datetime] = None,
    ) -> None:
        """
        Log tag detection with full context.

        Args:
            tag_id: Tag identifier
            direction: ENTRY/EXIT/UNKNOWN
            rssi: Signal strength in dBm
            occurrence_count: How many times tag has been seen
            motion_start: When motion event started
            motion_end: When motion event ended
            timestamp: When tag was detected (defaults to now)
        """
        # Create event with all data
        event = CattleEvent(
            timestamp=timestamp or datetime.now(),
            event_type="tag_detection",
            motion_start=motion_start,
            motion_end=motion_end,
            tag_id=tag_id,
            direction=direction,
            rssi=rssi,
            occurrence_count=occurrence_count
        )
        self._write_event(event)
        # TODO: Log the tag that has been detected and all relevant data
        pass

    def get_recent_events(self, n: int = 10) -> List[CattleEvent]:
        """
        Get the most recent N events from the log.

        Args:
            n: Number of events to retrieve

        Returns:
            List of CattleEvent objects (newest first)
        """
        if not self.log_file.exists():
            return []

        all_rows = []
        with open(self.log_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse each row into a CattleEvent
                event = CattleEvent(
                    timestamp=datetime.fromisoformat(row["timestamp"]) if row["timestamp"] else None,
                    event_type=row["event_type"],
                    motion_start=datetime.fromisoformat(row["motion_start"]) if row["motion_start"] else None,
                    motion_end=datetime.fromisoformat(row["motion_end"]) if row["motion_end"] else None,
                    tag_id=row["tag_id"] if row["tag_id"] else None,
                    direction=row["direction"] if row["direction"] else None,
                    rssi=float(row["rssi"]) if row["rssi"] else None,
                    occurrence_count=int(row["occurrence_count"]) if row["occurrence_count"] else None
                )
                all_rows.append(event)

        # Grab the last 'n' events, newest first
        return all_rows[-n:][::-1]
    
    def get_stats(self) -> dict:
        """
        Calculates statistics based on the log file.
        """
        # 1. Get the events
        events = self.get_recent_events(n=10000)

        # 2. Build the dictionary that the test expects
        stats = {
            'total_events': len(events),
        }

        return stats

    def _write_event(self, event: CattleEvent) -> None:
        # 2. Open file in append mode
        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)

        # 3. Create a dictionary from the dataclass
            row = {
                "timestamp": event.timestamp.isoformat(),
                "motion_start": event.motion_start.isoformat() if event.motion_start else "",
                "motion_end": event.motion_end.isoformat() if event.motion_end else "",
                "tag_id": event.tag_id or "",
                "direction": event.direction or "",
                "rssi": event.rssi if event.rssi is not None else "",
                "occurrence_count": event.occurrence_count if event.occurrence_count is not None else "",
                "event_type": event.event_type
        }

            writer.writerow(row)
        # TODO: Write new event to CSV file
        # Hint: Use csv.DictWriter to append row
        pass
