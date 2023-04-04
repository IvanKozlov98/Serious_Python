import time
import logging
import multiprocessing
from codecs import getencoder


def setup_logger():
    logging.basicConfig(filename='../artifacts/hard_logging.txt', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')


def process_a(queue_in, queue_out):
    setup_logger()
    while True:
        msg = queue_in.get()
        if msg == "exit":
            break
        msg_lower = msg.lower()
        logging.info(f"Process A received: {msg}, Process A sent: {msg_lower}")
        queue_out.put(msg_lower)
        time.sleep(5)


def process_b(queue_in, conn):
    setup_logger()
    encoder = getencoder('rot_13')
    while True:
        msg = queue_in.get()
        if msg == "exit":
            break
        msg_rot13 = encoder(msg)[0]
        logging.info(f"Process B received: {msg}, Process B sent: {msg_rot13}")
        conn.send(msg_rot13)


def main_hard():
    setup_logger()
    logging.info(f"Start logging")
    queue_a = multiprocessing.Queue()
    queue_b = multiprocessing.Queue()
    parent_conn, child_conn = multiprocessing.Pipe()

    a = multiprocessing.Process(target=process_a, args=(queue_a, queue_b))
    b = multiprocessing.Process(target=process_b, args=(queue_b, child_conn))

    a.start()
    b.start()

    setup_logger()
    print("Enter messages (type 'exit' to quit):")

    while True:
        user_input = input()
        logging.info(f"User input: {user_input}")

        if user_input.lower() == "exit":
            queue_a.put("exit")
            queue_b.put("exit")
            break

        queue_a.put(user_input)

        if parent_conn.poll():
            rot13_msg = parent_conn.recv()
            print(f"Rot13 encoded message: {rot13_msg}")
            logging.info(f"Rot13 encoded message: {rot13_msg}")

    a.join()
    b.join()
