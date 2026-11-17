
from models.event import get_event, get_system_event
from unittest.mock import patch
from main import main


def test_system_event_is_not_saved_to_database():
    system_event = get_system_event(
        title="Parser Failure Warning",
        location="Parser"
    )

    with (
        patch("main.fetch_events", return_value=[system_event]),
        patch("main.save_events"),
        patch("main.find_new_events", return_value=[system_event]),
        patch("main.send_notification", return_value=True),
        patch("main.update_events") as mock_update_events,
        patch("main.logger")
    ):
        main()

        mock_update_events.assert_called_once_with([])


def test_regular_event_is_saved_to_database():
    event = get_event(
        artist="Test Artist",
        date="2026-11-17",
        title="Test Concert",
        location="Test Location",
        url="https://example.com"
    )

    with (
        patch("main.fetch_events", return_value=[event]),
        patch("main.save_events"),
        patch("main.find_new_events", return_value=[event]),
        patch("main.send_notification", return_value=True),
        patch("main.update_events") as mock_update_events,
        patch("main.logger")
    ):
        main()

        mock_update_events.assert_called_once_with([event])
