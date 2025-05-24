import unittest
import pygame # Required for Rect and potentially other types
from settings import Settings
from alien import NormalAlien, FastAlien, TankAlien, ShooterAlien

# --- Mocks ---
class MockSurface:
    def get_rect(self):
        return pygame.Rect(0, 0, 50, 50) # Example dimensions

class MockScreen:
    def get_rect(self):
        # Return a Pygame Rect object, as this is often expected
        return pygame.Rect(0, 0, 1200, 800)

class MockSound:
    def __init__(self, file_path):
        self.file_path = file_path
    def play(self):
        pass # Does nothing

class TestAlienBehavior(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up for all tests in the class."""
        # Initialize pygame.mixer if not already initialized, to prevent "mixer system not initialized"
        # This is a common requirement for Sound objects, even if they are mocked.
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # Mock Pygame's image loading and sound system
        cls.original_pygame_image_load = pygame.image.load
        pygame.image.load = lambda path: MockSurface()

        cls.original_pygame_mixer_Sound = pygame.mixer.Sound
        pygame.mixer.Sound = MockSound

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests in the class."""
        # Restore original Pygame functions
        pygame.image.load = cls.original_pygame_image_load
        pygame.mixer.Sound = cls.original_pygame_mixer_Sound

    def setUp(self):
        """Set up for each test method."""
        self.ai_settings = Settings()
        self.mock_screen = MockScreen()

    def test_normal_alien_properties(self):
        """Test properties of NormalAlien."""
        normal = NormalAlien(self.ai_settings, self.mock_screen)
        self.assertEqual(normal.health, 1)
        self.assertEqual(normal.points, self.ai_settings.normal_alien_points)
        self.assertEqual(normal.speed_factor, self.ai_settings.alien_speed_factor)

    def test_tank_alien_properties(self):
        """Test properties of TankAlien."""
        tank = TankAlien(self.ai_settings, self.mock_screen)
        self.assertEqual(tank.health, self.ai_settings.tank_alien_health)
        self.assertEqual(tank.points, self.ai_settings.tank_alien_points)
        expected_speed = self.ai_settings.alien_speed_factor * self.ai_settings.tank_alien_speed_multiplier
        self.assertAlmostEqual(tank.speed_factor, expected_speed)

    def test_tank_alien_take_damage(self):
        """Test TankAlien taking damage."""
        tank = TankAlien(self.ai_settings, self.mock_screen)
        hits_to_destroy = self.ai_settings.tank_alien_health
        
        # Initial health should match
        self.assertEqual(tank.health, hits_to_destroy)

        for i in range(hits_to_destroy - 1):
            self.assertFalse(tank.take_damage(1), f"Tank should not be destroyed after {i+1} hit(s)")
            self.assertEqual(tank.health, hits_to_destroy - (i + 1), "Tank health not reduced correctly.")
        
        self.assertTrue(tank.take_damage(1), "Tank should be destroyed on the final hit.")
        self.assertEqual(tank.health, 0, "Tank health should be 0 after being destroyed.")

    def test_fast_alien_properties(self):
        """Test properties of FastAlien."""
        fast = FastAlien(self.ai_settings, self.mock_screen)
        expected_speed = self.ai_settings.alien_speed_factor * self.ai_settings.fast_alien_speed_multiplier
        self.assertAlmostEqual(fast.speed_factor, expected_speed)
        self.assertEqual(fast.points, self.ai_settings.fast_alien_points)
        self.assertEqual(fast.health, 1) # Assuming FastAlien has 1 health

    def test_shooter_alien_properties(self):
        """Test properties of ShooterAlien."""
        shooter = ShooterAlien(self.ai_settings, self.mock_screen)
        self.assertEqual(shooter.points, self.ai_settings.shooter_alien_points)
        self.assertEqual(shooter.fire_interval_frames, self.ai_settings.shooter_alien_fire_cooldown)
        self.assertEqual(shooter.health, 1) # Assuming ShooterAlien has 1 health

if __name__ == '__main__':
    # Pygame might need to be initialized for Rect and other types if not done by mocks
    pygame.init() 
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
