# my_lidar_package/lidar.py

import PyLidar3
import time
import numpy as np
import math
import serial

def collect_lidar_data(port, scan_duration=10):
    try:
        Obj = PyLidar3.YdLidarX4(port)
        if Obj.Connect():
            print(Obj.GetDeviceInfo())
            gen = Obj.StartScanning()
            t_start = time.time()
            angle_distance_dict = {}
            while time.time() - t_start < scan_duration:
                current_time = time.time()
                interval_data = {}
                while time.time() - current_time < 1:  # Collect data for 1 second
                    for data in gen:
                        for angle in data:
                            interval_data[angle] = data[angle]
                        break
                # Process interval data
                if interval_data:
                    trigger_results = process_lidar_data(interval_data)
                    print("Trigger distances array [Front, Right, Back, Left]:", trigger_results["triggers"])
                    print("Distances from inner rectangle boundary [Front, Right, Back, Left]:", trigger_results["distances_to_inner_rect"])

                    # Update the main angle_distance_dict with interval data
                    angle_distance_dict.update(interval_data)

            Obj.StopScanning()
            Obj.Disconnect()
        else:
            print("Error connecting to device")

        return angle_distance_dict
    except serial.SerialException as e:
        print(f"Serial Exception: {e}")
        return {}
    except Exception as e:
        print(f"An error occurred: {e}")
        return {}

def process_lidar_data(interval_data):
    distances, angles = extract_lidar_data(interval_data)
    triggers, trigger_statements, distances_to_inner_rect, t_angles = trigger_directions(distances, angles)
    results = {
        "triggers": triggers,
        "trigger_statements": trigger_statements,
        "distances_to_inner_rect": distances_to_inner_rect,
        "t_angles": t_angles
    }
    return results

def extract_lidar_data(angle_distance_dict):
    distances_in_range = []
    angles_in_range = []

    for angle, distance in angle_distance_dict.items():
        if 120 <= distance <= 300:
            angles_in_range.append(angle)
            distances_in_range.append(distance)

    return distances_in_range, angles_in_range

def trigger_directions(distances, angles):
    sectors = {
        "Front": [],
        "Right": [],
        "Back": [],
        "Left": []
    }

    for distance, angle in zip(distances, angles):
        if 335 <= angle or angle < 25:
            sectors["Front"].append((angle, distance))
        elif 25 <= angle < 155:
            sectors["Right"].append((angle, distance))
        elif 155 <= angle < 205:
            sectors["Back"].append((angle, distance))
        elif 205 <= angle < 335:
            sectors["Left"].append((angle, distance))

    triggers = [0, 0, 0, 0]
    trigger_angles = [0, 0, 0, 0]
    trigger_statements = {}
    distances_to_inner_rect = [0, 0, 0, 0]

    for i, (sector, points) in enumerate(sectors.items()):
        if points:
            min_point = min(points, key=lambda x: x[1])
            triggers[i] = min_point[1]
            angle = min_point[0]
            trigger_statements[sector] = f"Trigger {sector} at angle {angle} with distance {min_point[1]} mm"
            distances_to_inner_rect[i] = max(0, min_point[1] - 120)
            trigger_angles[i] = angle
        else:
            trigger_statements[sector] = f"No trigger for {sector}"

    return triggers, trigger_statements, distances_to_inner_rect, trigger_angles

def run_lidar_scan(port, scan_duration=10):
    lidar_data = collect_lidar_data(port, scan_duration)
    if lidar_data:
        distances, angles = extract_lidar_data(lidar_data)
        triggers, trigger_statements, distances_to_inner_rect, t_angles = trigger_directions(distances, angles)

        print("Trigger distances array [Front, Right, Back, Left]:", triggers)
        print("Distances from inner rectangle boundary [Front, Right, Back, Left]:", distances_to_inner_rect)
    else:
        print("No LIDAR data collected")
