import numpy as np
from scipy.signal import find_peaks

def calculate_distance_and_steps_from_sensor_data(sensor_data):
    """
    Process 3D sensor data to calculate the distance in meters, count the steps, and calculate the total time in seconds.
    Sensor data is expected to be a dictionary with 'time' and 'acceleration' keys.
    'acceleration' should be another dictionary with 'x', 'y', and 'z' keys.
    Example: {'time': [0, 1, 2, 3, 4], 'acceleration': {'x': [0.4, 0.5, 0.6, 0.7, 0.8], 'y': [...], 'z': [...]} }
    """
    if not isinstance(sensor_data, dict):
        raise TypeError("sensor_data should be a dictionary with 'time' and 'acceleration' keys.")

    if 'time' not in sensor_data or 'acceleration' not in sensor_data:
        raise ValueError("sensor_data should contain 'time' and 'acceleration' keys.")
    
    times = np.array(sensor_data['time'])
    acceleration = sensor_data['acceleration']
    
    if not all(k in acceleration for k in ('x', 'y', 'z')):
        raise ValueError("acceleration should contain 'x', 'y', and 'z' keys.")
    
    accel_x = np.array(acceleration['x'])
    accel_y = np.array(acceleration['y'])
    accel_z = np.array(acceleration['z'])
    
    if len(times) == 0 or len(accel_x) == 0 or len(accel_y) == 0 or len(accel_z) == 0:
        return 0.0, 0, [], []
    
    # Calculate the resultant acceleration
    resultant_acceleration = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
    
    # Detect peaks in the resultant acceleration to count steps
    peaks, _ = find_peaks(resultant_acceleration, height=0.5)  # Adjust height threshold as needed
    step_count = len(peaks)
    
    # Get the times at which peaks occur
    peak_times = times[peaks]
    
    # Integrate acceleration to get velocity (simple numerical integration)
    velocities = np.cumsum(resultant_acceleration * np.diff(times, prepend=0))
    
    # Integrate velocity to get distance (simple numerical integration)
    distances = np.cumsum(velocities * np.diff(times, prepend=0))
    
    # Calculate distances at each step
    step_distances = []
    if step_count > 0:
        # Include the first step distance
        step_distances.append(distances[peaks[0]])
        for i in range(1, step_count):
            step_distance = distances[peaks[i]] - distances[peaks[i-1]]
            step_distances.append(step_distance)
    
    # The total distance is the last value in the distances array
    total_distance = distances[-1] if len(distances) > 0 else 0.0
    
    return total_distance, step_count, step_distances, peak_times.tolist()
