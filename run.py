"""Startup script with auto-restart on crash"""
import subprocess
import sys
import time
from datetime import datetime

MAX_RESTARTS = 10
RESTART_WINDOW_SECONDS = 3600  # 1 hour
restart_times = []

def should_restart() -> bool:
    """Check if we should restart based on restart frequency"""
    current_time = time.time()
    
    # Remove old restart times outside the window
    restart_times[:] = [t for t in restart_times if current_time - t < RESTART_WINDOW_SECONDS]
    
    # Check if we've restarted too many times
    if len(restart_times) >= MAX_RESTARTS:
        print(f"\n{'='*80}")
        print(f"ERROR: Bot has crashed {MAX_RESTARTS} times in the last hour.")
        print("This likely indicates a configuration or system issue.")
        print("Please check logs and fix the issue before restarting.")
        print(f"{'='*80}\n")
        return False
        
    return True

def run_bot():
    """Run the bot with auto-restart"""
    print("="*80)
    print("POLYMARKET SNIPER BOT - AUTO-RESTART WRAPPER")
    print("="*80)
    print("Press Ctrl+C to stop the bot permanently")
    print("="*80 + "\n")
    
    while True:
        try:
            if not should_restart():
                return
                
            # Record restart time
            restart_times.append(time.time())
            
            print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting bot...")
            
            # Run the bot
            process = subprocess.Popen(
                [sys.executable, 'bot.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # Stream output
            for line in process.stdout:
                print(line, end='')
                
            # Wait for process to complete
            return_code = process.wait()
            
            if return_code == 0:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bot stopped normally")
                break
            else:
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bot crashed with code {return_code}")
                print("Restarting in 5 seconds...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\nReceived Ctrl+C - Stopping bot...")
            if process:
                process.terminate()
                process.wait()
            break
        except Exception as e:
            print(f"\nUnexpected error in wrapper: {e}")
            print("Restarting in 10 seconds...")
            time.sleep(10)

if __name__ == "__main__":
    run_bot()
