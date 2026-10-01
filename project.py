import numpy as np
from obspy import read

def classify_activity(rms, threshold):
    if rms > threshold:
        return "HIGH"
    return "NORMAL"

def analyze_channel(trace):
    window_size = int(trace.stats.sampling_rate * 60)
    results = []
    rms_values = []

    for start in range(0, len(trace.data), window_size):
        chunk = trace.data[start:start + window_size]

        rms = np.sqrt(np.mean(chunk.astype(float) ** 2))
        rms_values.append(rms)

    rms_values = np.array(rms_values)

    median = np.median(rms_values)
    mad = np.median(np.abs(rms_values - median))
    threshold = median + 3 * mad

    for i, rms in enumerate(rms_values):
        start_time = trace.stats.starttime + i * 60
        end_time = start_time + 60
    
        status = classify_activity(rms, threshold)

        results.append({
            "start": start_time,
            "end": end_time,
            "rms": rms,
            "status": status
        })

    return results

def group_events(results):
    events = []
    current_event = None

    for result in results:
        if result["status"] == "HIGH":
            if current_event is None:
                current_event = {
                    "start": result["start"],
                    "end": result["end"]
                }
            else:
                current_event["end"] = result["end"]

        else:
            if current_event is not None:
                events.append(current_event)
                current_event = None

    if current_event is not None:
        events.append(current_event)

    return events

def events_overlap(event1, event2):
    return (
        event1["start"] < event2["end"]
        and event2["start"] < event1["end"]
    )

def compare_events(all_events):
    combined = []

    for channel, events in all_events.items():
        for event in events:
            found = False

            for combined_event in combined:
                if events_overlap(event, combined_event):
                    combined_event["start"] = min(
                        combined_event["start"], event["start"]
                    )
                    combined_event["end"] = max(
                        combined_event["end"], event["end"]
                    )

                    if channel not in combined_event["channels"]:
                        combined_event["channels"].append(channel)

                    found = True
                    break

            if not found:
                combined.append({
                    "start": event["start"],
                    "end": event["end"],
                    "channels": [channel]
                })

    combined.sort(key=lambda event: event["start"])
    
    return combined

def classify_event(channels):
    count = len(channels)

    if count == 3:
        return "STRONG"
    elif count == 2:
        return "MODERATE"
    return "WEAK"

def format_event(event, number):
    start = event["start"].strftime("%H:%M:%S")
    end = event["end"].strftime("%H:%M:%S")
    channels = ", ".join(event["channels"])

    return (
        f"[{number}] {start} - {end} UTC\n"
        f"Channels: {channels}\n"
        f"Strength: {event['strength']}"
    )

def summarize_analisys(combined, station):
    strong = 0
    moderate = 0
    weak = 0

    for event in combined:
        if event["strength"] == "STRONG":
            strong += 1
        elif event["strength"] == "MODERATE":
            moderate += 1
        else:
            weak += 1

    if strong > 0:
        observation = (
            "High seismic activity was detected during "
            "several periods of the analysis."
        )
    elif moderate > 0:
        observation = (
            "Moderate seismic activity was detected, "
            "but no strong multi-channel activity was observed."
        )
    else:
        observation = (
            "Only isolated periods of elevated activity "
            "were detected."
        )

    print(f"Analysis for station {station}:")
    print()
    print(observation)
    print()

    strong_events = [
        event for event in combined if event["strength"] == "STRONG"
    ]

    if strong_events:
        first_strong = strong_events[0]
        last_strong = strong_events[-1]

        activity_start = first_strong["start"].strftime("%H:%M:%S")
        activity_end = last_strong["end"].strftime("%H:%M:%S")

        print(
            f"Several periods of high seismic activity were detected "
            f"between {activity_start} and {activity_end} UTC."
        )


def main():
    st = read("krakatau10.seed")

    stations = sorted(set(trace.stats.station for trace in st))

    print("=" * 50)
    print("\t\tSEISMIC ACTIVITY EXPLORER")
    print("\tAnak Krakatau Volcano - 22 December 2018")
    print("=" * 50)
    print()
    print("Available Stations:")
    print()

    for number, station in enumerate(stations, start=1):
        station_traces = st.select(station=station)
        channels = sorted(set(trace.stats.channel for trace in station_traces))

        print(
            f"{number:2}.{station:<6} "
            f"{len(channels)} channels: {', '.join(channels)}"
        )

    print()

    while True:
        choice = input("Choose a station: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(stations):
            station = stations[int(choice) - 1]
            break

        print("Invalid choice.Please enter a valid station number.")

    st = st.select(station=station)

    print()
    print("=" * 50)
    print()
    print(f"Selected Station: {station}")
    print()

    all_events = {}

    for trace in st:
        results = analyze_channel(trace)
        events = group_events(results)

        channel = trace.stats.channel
        all_events[channel] = events

    combined = compare_events(all_events)

    for event in combined:
        event["strength"] = classify_event(event["channels"])

    print("Detected seismic activity:")
    print()

    for number, event in enumerate(combined, start=1):
        print(format_event(event, number))
        print()

    print("=" * 50)
    print(f"Total events detected: {len(combined)}")
    print("=" * 50)

    print()
    summarize_analisys(combined, station)
    print()


if __name__ == "__main__":
    main()