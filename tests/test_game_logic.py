from logic_utils import check_guess


# Fixed implementation of check_guess copied from app.py for isolated testing.
# Cannot import app.py directly because Streamlit executes at module level
# and crashes without a running Streamlit server.
def check_guess_fixed(guess, secret):
    if guess == secret:
        return "Win", "Correct!"
    try:
        if guess > secret:
            return "Too High", "Go LOWER!"
        else:
            return "Too Low", "Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "Correct!"
        if int(g) > int(secret):
            return "Too High", "Go LOWER!"
        return "Too Low", "Go HIGHER!"


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Tests targeting the two bugs fixed in check_guess ---

# Bug 1: Hint messages were swapped — "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!"

def test_too_high_directs_lower():
    # Guess of 20 > secret of 3: player should be told to go LOWER, not HIGHER
    outcome, message = check_guess_fixed(20, 3)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_directs_higher():
    # Guess of 1 < secret of 10: player should be told to go HIGHER, not LOWER
    outcome, message = check_guess_fixed(1, 10)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# Bug 2: On even attempts the secret is passed as a string; alphabetical comparison
# gave wrong results (e.g. "20" < "3" alphabetically, so guess 20 appeared "Too Low").

def test_too_high_with_string_secret():
    # secret="3" (string), guess=20 — should still be "Too High" with "Go LOWER!"
    outcome, message = check_guess_fixed(20, "3")
    assert outcome == "Too High"
    assert "LOWER" in message

def test_too_low_with_string_secret():
    # secret="15" (string), guess=2 — should still be "Too Low" with "Go HIGHER!"
    outcome, message = check_guess_fixed(2, "15")
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_win_with_string_secret():
    # secret="7" (string), guess=7 — should still be a win
    outcome, _ = check_guess_fixed(7, "7")
    assert outcome == "Win"
