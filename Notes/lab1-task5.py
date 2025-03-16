import random
import time

class Env:
    def __init__(self):
        self.corridors = ["corridor 1", "corridor 2"]
        self.rooms = ["room 101", "room 102", "room 103"]
        self.nurse_stations = ["nurse station A", "nurse station B"]
        self.medicine_storage = "medicine storage"
        
        self.tasks = [
            {"room": "room 101", "medicine": "Aspirin", "patient_id": "P1001", "delivered": False},
            {"room": "room 102", "medicine": "Antibiotic", "patient_id": "P1002", "delivered": False},
            {"room": "room 103", "medicine": "Insulin", "patient_id": "P1003", "delivered": False},
        ]
        
    def get_tasks(self):
        return self.tasks
    
    def update_task(self, task_index, delivered_status):
        self.tasks[task_index]["delivered"] = delivered_status
        
    def display_system_state(self):
        print("Current Delivery Tasks:")
        for task in self.tasks:
            status = "DELIVERED" if task["delivered"] else "PENDING"
            print(f"  Room: {task['room']} | Medicine: {task['medicine']} | Patient ID: {task['patient_id']} | Status: {status}")
        print()    
        
class HospitalDeliveryRobot:
    def __init__(self):
        self.current_location = "docking station"
    
    def move_to(self, destination):
        print(f"moving from {self.current_location} ot {destination}...")
        time.sleep(1)
        self.current_location = destination
        print(f"arrived at {self.current_location}.\n")
        
    def pick_up_medicine(self, medicine):
        print(f"picking up {medicine} from the medicine storage...")
        time.sleep(1)
        print(f"{medicine} has been picked up.\n")
    
    def scan_patient_id(self, expected_id):
        print("Scanning patient ID...")
        time.sleep(1)
        success = random.random() < 0.9
        scanned_id = expected_id if success else "UNKNOWN"
        print(f"Scanned patient ID: {scanned_id} (expected: {expected_id})")
        return scanned_id == expected_id

    def deliver_medicine(self, task):
        print(f"Delivering {task['medicine']} to {task['room']}...")
        time.sleep(1)
        print("Medicine delivered successfully.\n")

    def alert_staff(self, room):
        print(f"Alerting staff at nurse station regarding an issue at {room}...")
        time.sleep(1)
        print("Staff has been alerted.\n")

    def execute_delivery(self, environment):
        tasks = environment.get_tasks()
        print("Starting delivery tasks...\n")

        for index, task in enumerate(tasks):
            print(f"Processing task for {task['room']}: Deliver {task['medicine']} to patient {task['patient_id']}")
            self.move_to(environment.medicine_storage)
            self.pick_up_medicine(task["medicine"])
            self.move_to(task["room"])
            if self.scan_patient_id(task["patient_id"]):
                self.deliver_medicine(task)
                environment.update_task(index, True)
            else:
                print("Patient ID mismatch detected!")
                self.alert_staff(task["room"])
                environment.update_task(index, False)
            self.move_to(random.choice(environment.corridors))

        print("All tasks processed.\n")


def run_simulation():
    environment = Env()
    print("Initial System State:")
    environment.display_system_state()

    robot = HospitalDeliveryRobot()

    robot.execute_delivery(environment)

    print("Final System State:")
    environment.display_system_state()
