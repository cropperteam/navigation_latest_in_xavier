from lidar_package import LidarScanner
import time

def main():
    com_port = 'COM5'  # Change this to your actual COM port
    scanner = LidarScanner(com_port)
    
    try:
        while True:
            trigger = scanner.scan()
            if trigger:
                print("Trigger array:", trigger)
            else:
                print("Scan failed or no objects detected")
            
            # Optional: add a small delay to prevent overwhelming the system
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\nScanning stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()