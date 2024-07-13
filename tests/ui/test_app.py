import unittest
import time
import os
from multiprocessing import Process
from dotenv import load_dotenv
from src.testdriver import run_server, TKTestDriver
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestMailSocialApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info("Setting up test class")
        os.environ["TESTDRIVER"] = "true"
        cls.host = "127.0.0.1"
        cls.port = 8000
        cls.api_key = "test_api_key"
        cls.server_process = Process(target=run_server, args=(cls.host, cls.port, cls.api_key))
        cls.server_process.daemon = False
        cls.server_process.start()
        logger.info("Started server process")
        time.sleep(5)  # Allow time for the server to start
        cls.driver = TKTestDriver(cls.host, cls.port, cls.api_key)

    @classmethod
    def tearDownClass(cls):
        logger.info("Tearing down test class")
        try:
            cls.driver.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown request: {e}")
        cls.server_process.terminate()
        cls.server_process.join(timeout=30)
        if cls.server_process.is_alive():
            logger.warning("Server process did not terminate, forcing...")
            cls.server_process.kill()
            cls.server_process.join()
        logger.info("Terminated server process")

    def setUp(self):
        logger.info("Setting up test")
        self.ensure_app_is_running()
        logger.info("Application is running and ready for test")

    def tearDown(self):
        logger.info("Tearing down test")
        # No need to shut down the application after each test
        pass

    def ensure_app_is_running(self):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                status = self.driver.status()
                if status["application_running"] and status["application_fully_initialized"]:
                    return  # App is already running and initialized
                
                # If not running, start the app
                response = self.driver.startup()
                if response["status"] == "Application started":
                    # Wait for initialization
                    self.driver.wait_for_initialization()
                    return
                
            except Exception as e:
                logger.error(f"Error during setup (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(5)  # Wait before retrying

    def test_startup_shutdown(self):
        logger.info("Running test_startup_shutdown")
        # Test starting up when the app is already running
        response = self.driver.startup()
        self.assertEqual(response["status"], "Application already running")

        # Test shutting down
        response = self.driver.shutdown()
        self.assertEqual(response["status"], "Application shut down")

        # Test starting up when the app is not running
        response = self.driver.startup()
        self.assertEqual(response["status"], "Application started")

    def test_status(self):
        logger.info("Running test_status")
        # Check status when the app is running
        status = self.driver.status()
        self.assertTrue(status["application_running"])
        self.assertTrue(status["application_fully_initialized"])

        # Shut down the app
        self.driver.shutdown()
        time.sleep(2)

        # Check status when the app is not running
        status = self.driver.status()
        self.assertFalse(status["application_running"])
        self.assertFalse(status["application_fully_initialized"])

        # Start the app again for the next tests
        self.driver.startup()
        self.driver.wait_for_initialization()

    def test_update_accent_color(self):
        logger.info("Running test_update_accent_color")
        response = self.driver.interact("update_accent_color", ["#FF0000"])
        self.assertEqual(response["status"], "Success")

    def test_update_font_size(self):
        logger.info("Running test_update_font_size")
        response = self.driver.interact("update_font_size", [16])
        self.assertEqual(response["status"], "Success")

    def test_send_message(self):
        logger.info("Running test_send_message")
        response = self.driver.interact("send_message")
        self.assertEqual(response["status"], "Success")

if __name__ == '__main__':
    unittest.main()