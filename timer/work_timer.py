import time
from plyer import notification

def send_alert(title, message, icon_path=None):
    notification.notify(
        title=title,
        message=message,
        app_name="My Python App",
        app_icon=icon_path,      # Path to .ico (Windows) or .png (Linux) file
        timeout=30,              # Duration in seconds the notification stays active
        toast=False              # True for a simple toast, False for a rich notification
    )

def timer(seconds):
     while seconds > 0:
        # Divide seconds into minutes and seconds
        mins, secs = divmod(seconds, 60)
        # Format as 00:00
        timer_format = f"{mins:02d}:{secs:02d}"
        
        # Overwrite the line in the terminal
        print(timer_format, end="\r")
        time.sleep(1)
        seconds -= 1

        if seconds >= 600:
            if seconds == 600:
                send_alert(
                    title="10 minutes left!",
                    message="10 minute remain on your timer."
                )
        elif seconds >= 300:
            if seconds == 300:
                send_alert(
                    title="5 minutes left!",
                    message="5 minute remain on your timer."
                )
        elif seconds >= 60:
            if seconds == 60:
                send_alert(
                    title="1 minute left!",
                    message="Only 1 more minute remaining on your timer."
                )


def main():
    # Title screen
    print("==============+ Timer +==============")
    print("\n Enter the time in minutes and seconds below\n")
    mins = int(input("Minutes:"))
    seconds = int(input("Seconds:"))
    total_time = (mins*60) + seconds
    timer(total_time)

    

if __name__ == "__main__":
    main()
