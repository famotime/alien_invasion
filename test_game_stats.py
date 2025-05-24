import unittest
import os
import json
from game_stats import GameStats, HIGH_SCORE_FILE # Import the global constant as well
from settings import Settings

class TestGameStats(unittest.TestCase):
    def setUp(self):
        """Set up for test methods."""
        self.ai_settings = Settings()
        self.test_highscore_file = 'test_highscore.json'
        
        # Override the global HIGH_SCORE_FILE for the duration of the tests
        # This is a bit tricky as the GameStats instance uses the global directly
        # A better approach would be to pass the filename to GameStats constructor or a method
        # For now, we'll patch the global variable in the game_stats module
        self.original_highscore_file_path = HIGH_SCORE_FILE
        import game_stats
        game_stats.HIGH_SCORE_FILE = self.test_highscore_file
        
        self.stats = GameStats(self.ai_settings)
        # Ensure stats instance uses the overridden path, it should if it re-evaluates the global
        # or if we re-initialize after patching. Re-initializing for safety here.
        self.stats = GameStats(self.ai_settings)


    def tearDown(self):
        """Clean up after test methods."""
        if os.path.exists(self.test_highscore_file):
            os.remove(self.test_highscore_file)
        
        # Restore the original high score file path
        import game_stats
        game_stats.HIGH_SCORE_FILE = self.original_highscore_file_path

    def test_initial_high_score_no_file(self):
        """Test that high_score is 0 if the highscore file doesn't exist."""
        # This test relies on setUp ensuring no file exists initially for this specific instance
        # and that GameStats correctly handles FileNotFoundError.
        # Since self.stats is created in setUp after potential file removal, this should be fine.
        self.assertEqual(self.stats.high_score, 0, "Initial high score should be 0 with no file.")

    def test_save_high_score(self):
        """Test saving the high score to a file."""
        self.stats.high_score = 50000
        self.stats.save_high_score()
        self.assertTrue(os.path.exists(self.test_highscore_file), "High score file was not created.")
        with open(self.test_highscore_file, 'r') as f:
            saved_score = json.load(f)
        self.assertEqual(saved_score, 50000, "Saved high score in file does not match.")

    def test_load_high_score(self):
        """Test loading the high score from an existing file."""
        expected_high_score = 12345
        # Directly write to the test highscore file
        with open(self.test_highscore_file, 'w') as f:
            json.dump(expected_high_score, f)
        
        # Create a new GameStats instance to trigger loading
        stats_loader = GameStats(self.ai_settings)
        self.assertEqual(stats_loader.high_score, expected_high_score, "Loaded high score does not match expected.")

    def test_load_high_score_invalid_json(self):
        """Test loading high score from a file with invalid JSON."""
        # Write invalid JSON to the test highscore file
        with open(self.test_highscore_file, 'w') as f:
            f.write("This is not valid JSON")
            
        # Create a new GameStats instance
        stats_loader = GameStats(self.ai_settings)
        self.assertEqual(stats_loader.high_score, 0, "High score should be 0 when file contains invalid JSON.")

    def test_load_high_score_empty_file(self):
        """Test loading high score from an empty file (which is invalid JSON)."""
        with open(self.test_highscore_file, 'w') as f:
            pass # Create an empty file
        
        stats_loader = GameStats(self.ai_settings)
        self.assertEqual(stats_loader.high_score, 0, "High score should be 0 for an empty file.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
