import serial
import math
import matplotlib.pyplot as plt
from .utils import _CheckSum, _HexArrToDec, _AngleCorr, _Calculate, _Mean

class LidarScanner:
    def __init__(self, port):
        self.port = port
        self.ser = None  # Serial port object, initially None

    def check_object_in_area(self, x, y):
        trigger = [0, 0, 0, 0]  # Initialize trigger array
        minfront, minright, minback, minleft = [], [], [], []  # Lists to hold minimum distances in each direction
        object_detected = False  # Flag to indicate if object is detected
        for i in range(len(x)):  # Iterate over all x coordinates
            # Check if the point is within the specified areas
            if (420 < abs(x[i]) <= 620 and -1025 <= y[i] <= 1250) or \
               (825 < abs(y[i]) <= 1025 and -620 <= x[i] <= 620):
                object_detected = True  # Set flag to True if object is detected

                # Categorize point based on angle
                if 333 <= i or i < 27:
                    minfront.append(y[i])
                    trigger[0] = min(minfront) if minfront else trigger[0]
                if 27 <= i < 153:
                    minright.append(x[i])
                    trigger[1] = min(minright) if minright else trigger[1]
                if 153 <= i < 207:
                    minback.append(y[i])
                    trigger[2] = max(minback) if minback else trigger[2]
                if 207 <= i < 333:
                    minleft.append(x[i])
                    trigger[3] = max(minleft) if minleft else trigger[3]

        return object_detected, trigger  # Return detection flag and trigger values

    def plot_lidar(self, x, y):
        plt.figure(1)
        plt.cla()  # Clear the current axes
        plt.ylim(-2000, 2000)
        plt.xlim(-2000, 2000)
        plt.scatter(x, y, c='r', s=8)  # Plot the LIDAR points

        # Draw rectangles for the defined areas
        center_box1 = plt.Rectangle((-420, -825), 840, 1650, fill=False, edgecolor='g')
        center_box2 = plt.Rectangle((-620, -1025), 1240, 2050, fill=False, edgecolor='b')
        
        plt.gca().add_patch(center_box1)
        plt.gca().add_patch(center_box2)
        
        plt.title("LIDAR Scan", color='blue')
        plt.pause(0.001)  # Pause to update the plot

    def code(self):
        data1 = self.ser.read(6000)  # Read 6000 bytes from serial port
        if not data1:
            print("No data read from serial port")
            return None

        data2 = data1.split(b"\xaa\x55")[1:-1]  # Split the data packets
        if not data2:
            print("No valid data packets found")
            return None

        distdict = {i: [] for i in range(360)}  # Initialize dictionary for distances
        for e in data2:
            try:
                if e[0] == 0 and _CheckSum(e):  # Check if packet is valid
                    d = _Calculate(e)  # Calculate distances
                    for ele in d:
                        angle = math.floor(ele[1])
                        if 0 <= angle < 360:
                            distdict[angle].append(ele[0])
            except Exception as ex:
                print(f"Error processing data packet: {ex}")

        for i in distdict.keys():
            distdict[i] = _Mean(distdict[i])  # Calculate mean distance for each angle

        return distdict

    def scan(self):
        try:
            self.ser = serial.Serial(port=self.port, baudrate=128000)  # Open serial port
            if not self.ser.isOpen():
                print("Failed to open serial port")
                return None

            # Scan start command
            values = bytearray([int('a5', 16), int('60', 16)])
            self.ser.write(values)

            distdict = self.code()
            if distdict:
                x, y = self.convert_to_xy(distdict)  # Convert distance data to (x, y) coordinates
                object_detected, trigger = self.check_object_in_area(x, y)  # Check for objects in specified area
                self.plot_lidar(x, y)  # Plot the LIDAR data
                return trigger
            else:
                print("No angle data generated")
                return None

        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        finally:
            if self.ser and self.ser.isOpen():
                # Scan end command
                values = bytearray([int('a5', 16), int('65', 16)])
                self.ser.write(values)
                self.ser.close()

    def convert_to_xy(self, distdict):
        x = [0 for i in range(360)]
        y = [0 for i in range(360)]
        for angle in range(0, 360):
            x[angle] = distdict[angle] * math.sin(math.radians(angle))  # Convert to x coordinate
            y[angle] = distdict[angle] * math.cos(math.radians(angle))  # Convert to y coordinate
        return x, y
