import multiprocessing
from RabbitMQ.direct_consumer import start_direct_consumer
from RabbitMQ.fanout_consumer import start_fanout_consumer
from RabbitMQ.topic_consumer import start_topic_consumer

class MessageService:
    def __init__(self):
        self.processes = []

    def start_for_user(self, username, account_type, bank_code):
        print(f"[+] Starting consumers for {username} ({account_type}.{bank_code})")

        # Direct confirmation
        p1 = multiprocessing.Process(target=start_direct_consumer, args=(username,))
        p1.start()
        self.processes.append(p1)

        # Topic alerts by type and bank
        routing_key = f"{account_type}.{bank_code}"
        p2 = multiprocessing.Process(target=start_topic_consumer, args=(routing_key,))
        p2.start()
        self.processes.append(p2)

        # Fanout notifications
        p3 = multiprocessing.Process(target=start_fanout_consumer)
        p3.start()
        self.processes.append(p3)

    def stop_all(self):
        print("[x] Stopping all consumers...")
        for p in self.processes:
            p.terminate()
            p.join()
        self.processes.clear()
