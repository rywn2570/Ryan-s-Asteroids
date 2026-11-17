from unittest.mock import Mock, patch

import main

def test_handle_events_true_no_events(): # This test checks that handle_events returns True when there are no events in the event queue. 
    get_events = Mock(return_value=[])
    with patch.object(main.pygame.event, "get", get_events):
        assert main.handle_events() is True
    get_events.assert_called_once_with()

def test_update_game(): 
    dt = 0.1
    updatable = Mock()
    asteroids = []
    shots = []
    player = Mock()
    score = 0
    lives = 3
    hit_sound = Mock()

    assert lives == 3
    assert score == 0
    
    result = main.update_game(
        dt, updatable, asteroids, shots, player, score, lives, hit_sound
    )

    updatable.update.assert_called_once_with(dt) # Method provided by Mock imported from unittest.mock to check that the update method was called with the correct dt value
    assert result == (score, lives)

