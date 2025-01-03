import subprocess
import signal
import time



def run():
    while True:
        # open a thread to get the feed every 24 hours
        # and update the json and csv files
        process = subprocess.Popen(['python', 'get_feed.py'])

        # have a wait here that waits till it gets a signal
        # from the subprocess that the feed has been updated
        # Define a signal handler
        def signal_handler(signum, frame):
            print("Signal received, continuing execution")

        # Register the signal handler for SIGUSR1
        signal.signal(signal.SIGUSR1, signal_handler)

        # Wait for the signal
        print("Waiting for signal...")
        signal.pause()

        print("Feed has been updated, continuing execution")

        # Ensure the subprocess has finished
        process.wait()

        # now we can do some processing on the feed
        # like getting the latest papers and downloading the pdfs
        process = subprocess.Popen(['python', 'parse.py'])
        
    

if __name__ == "__main__":
    run()

