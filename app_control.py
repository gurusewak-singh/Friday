from AppOpener import open as open_app, give_appnames
import difflib
import psutil
import re
import pygetwindow as gw

def get_installed_apps():
    try:
        # give_appnames returns dict_keys, convert to list
        return list(give_appnames())
    except:
        return []

def find_best_match(query, apps):
    # exact match
    if query in apps:
        return query
    
    # close match
    matches = difflib.get_close_matches(query, apps, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return None

def open_system_app(query):
    apps = get_installed_apps()
    match = find_best_match(query, apps)
    
    if match:
        print(f"Found app match: {match}")
        try:
            open_app(match, match_closest=True, output=True)
            return True, match
        except Exception as e:
            print(f"Error opening app: {e}")
            return False, None
    else:
        return False, None

def force_close_process(app_name):
    """
    Fallback method to close an app by killing its process.
    Matches words in app_name against running process names.
    """
    print(f"Attempting to force close processes matching: {app_name}")
    app_words = set(app_name.lower().split())
    killed_any = False
    
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc_name = proc.info['name'].lower()
            # Check if any significant word from app_name is in proc_name
            # We filter out very short words to avoid false positives unless the app_name itself is short
            for word in app_words:
                if len(word) > 2 and word in proc_name:
                    print(f"Killing process {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.kill()
                    killed_any = True
                elif len(word) <= 2 and word == proc_name.split('.')[0]: # Exact match for short names
                     print(f"Killing process {proc.info['name']} (PID: {proc.info['pid']})")
                     proc.kill()
                     killed_any = True
                     
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    return killed_any

def normalize_string(s):
    """Removes spaces and non-alphanumeric characters, converts to lower case."""
    return re.sub(r'[^a-z0-9]', '', s.lower())

def find_window_by_query(query):
    """
    Finds a window matching the query using robust matching logic.
    Returns (window_obj, title) or (None, None).
    """
    query = query.lower()
    try:
        windows = gw.getAllTitles()
        windows = [w for w in windows if w.strip()]
        
        target_title = None
        
        # 1. Exact case-insensitive substring match
        matches = [w for w in windows if query in w.lower()]
        
        if matches:
            matches.sort(key=lambda x: 0 if x.lower().startswith(query) else 1)
            target_title = matches[0]
        
        # 2. Normalized match
        if not target_title:
            norm_query = normalize_string(query)
            for w in windows:
                if norm_query in normalize_string(w):
                    target_title = w
                    break
        
        # 3. Word subset match
        if not target_title:
            query_words = set(query.split())
            for w in windows:
                w_lower = w.lower()
                if all(word in w_lower for word in query_words):
                    target_title = w
                    break

        # 4. Fuzzy match
        if not target_title:
            close_matches = difflib.get_close_matches(query, windows, n=1, cutoff=0.6)
            if close_matches:
                target_title = close_matches[0]
        
        if target_title:
            print(f"Found window: {target_title}")
            target_windows = gw.getWindowsWithTitle(target_title)
            if target_windows:
                return target_windows[0], target_title
                
        return None, None
    except Exception as e:
        print(f"Error finding window: {e}")
        return None, None

def switch_to_window(query):
    """
    Switches focus to a window with a title matching the query.
    """
    print(f"Attempting to switch to window matching: {query}")
    win, title = find_window_by_query(query)
    
    if win:
        # Focus stealing workaround
        try:
            if win.isMinimized:
                win.restore()
            else:
                win.minimize()
                win.restore()
        except Exception as e:
            print(f"Warning: Failed to minimize/restore: {e}")

        try:
            win.activate()
        except Exception as e:
            if "Error code from Windows: 0" in str(e):
                pass
            else:
                print(f"Warning: Error during window activation: {e}")
            pass
        return True, title
    
    return False, None

def minimize_window(query):
    print(f"Attempting to minimize window matching: {query}")
    win, title = find_window_by_query(query)
    if win:
        try:
            win.minimize()
            return True, title
        except Exception as e:
            print(f"Error minimizing window: {e}")
    return False, None

def maximize_window(query):
    print(f"Attempting to maximize window matching: {query}")
    win, title = find_window_by_query(query)
    if win:
        try:
            win.maximize()
            return True, title
        except Exception as e:
            print(f"Error maximizing window: {e}")
    return False, None

def close_system_app(query):
    apps = get_installed_apps()
    match = find_best_match(query, apps)
    
    if match:
        print(f"Found app match to close: {match}")
        
        # 1. Try AppOpener first
        try:
            from AppOpener import close as close_app
            close_app(match, match_closest=True, output=True)
            
            force_close_process(match)
            return True, match
            
        except Exception as e:
            print(f"Error using AppOpener to close: {e}")
            # Fallback
            if force_close_process(match):
                return True, match
            return False, None
    else:
        return False, None

def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        if win:
            return win.title
        return None
    except Exception as e:
        print(f"Error getting active window: {e}")
        return None

def type_text(text):
    try:
        import pyautogui
        # Type the text
        pyautogui.write(text)
        return True
    except Exception as e:
        print(f"Error typing text: {e}")
        return False
