import pyautogui
import time

def close_current_tab():
    """Simulates Ctrl+w to close the current tab."""
    try:
        pyautogui.hotkey('ctrl', 'w')
        return True
    except Exception as e:
        print(f"Error closing tab: {e}")
        return False

def switch_next_tab():
    """Simulates Ctrl+Tab to switch to the next tab."""
    try:
        pyautogui.hotkey('ctrl', 'tab')
        return True
    except Exception as e:
        print(f"Error switching tab: {e}")
        return False

def switch_prev_tab():
    """Simulates Ctrl+Shift+Tab to switch to the previous tab."""
    try:
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        return True
    except Exception as e:
        print(f"Error switching tab: {e}")
        return False

def open_new_tab():
    """Simulates Ctrl+t to open a new tab."""
    try:
        pyautogui.hotkey('ctrl', 't')
        return True
    except Exception as e:
        print(f"Error opening new tab: {e}")
        return False

def search_in_new_tab(query):
    """Simulates Ctrl+t to open a new tab and searches for the query."""
    try:
        pyautogui.hotkey('ctrl', 't')
        time.sleep(0.5) # Wait for tab to open
        pyautogui.write(query)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Error searching in new tab: {e}")
        return False

def search_in_current_tab(query):
    """Simulates Ctrl+l to focus address bar and searches for the query."""
    try:
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5) # Wait for address bar focus
        pyautogui.write(query)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Error searching in current tab: {e}")
        return False
