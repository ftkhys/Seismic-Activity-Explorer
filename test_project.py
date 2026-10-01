from project import classify_activity, events_overlap, classify_event


def test_classify_activity():
    assert classify_activity(700, 663.50) == "HIGH"
    assert classify_activity(500, 663.50) == "NORMAL"


def test_events_overlap():
    event1 = {
        "start": 10,
        "end": 20
    }

    event2 = {
        "start": 15,
        "end": 25
    }

    event3 = {
        "start": 30,
        "end": 40
    }

    assert events_overlap(event1, event2) is True
    assert events_overlap(event1, event3) is False


def test_classify_event():
    assert classify_event(["BHE"]) == "WEAK"
    assert classify_event(["BHE", "BHN"]) == "MODERATE"
    assert classify_event(["BHE", "BHN", "BHZ"]) == "STRONG"