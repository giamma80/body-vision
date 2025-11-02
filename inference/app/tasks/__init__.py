"""Background tasks for inference processing."""

from inference.app.tasks.body_analysis import process_body_analysis

__all__ = ["process_body_analysis"]
