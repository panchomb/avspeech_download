import csv
import subprocess

# Path to the CSV file
csv_file = 'test.csv'

# Directory to save the downloaded segments
output_directory = 'videos/'
temp_directory = 'temp/'

# Read the CSV file and iterate through its rows
with open(csv_file, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    for row in csv_reader:
        if len(row) != 5:
            print("Invalid row format. Skipping:", row)
            continue

        youtube_id, start_time, end_time, x_coord, y_coord = row

        # Format the URL for the video
        video_url = f"https://www.youtube.com/watch?v={youtube_id}"

        # Define the start and end timestamps, as well as the time range
        start_time_seconds = round(float(start_time))
        end_time_seconds = round(float(end_time))
        time_range = end_time_seconds - start_time_seconds

        # Use yt-dlp to download the video segment using ffmpeg
        output_filename = f"{youtube_id}_{start_time}_{end_time}.mp4"
        output_path = f"{output_directory}{output_filename}"

        temp_filename = f"temp_{output_filename}"
        temp_output_path = f"{temp_directory}{temp_filename}"

        yt_dlp_command = [
            'yt-dlp',
            '-f', 'best',
            '-o', f'{temp_output_path}',
            video_url
        ]

        ffmpeg_command = [
            'ffmpeg',
            '-ss', f'{start_time_seconds}',
            '-i', f'{temp_output_path}',
            '-t', f'{time_range}',
            '-c', 'copy', f'{output_path}'
        ]

        delete_temp_file_command = [
            'rm',
            temp_output_path
        ]


        try:
            # Download the video segment
            subprocess.run(yt_dlp_command, check=True)

            # Trim the video segment
            subprocess.run(ffmpeg_command, check=True)

            # Delete the temporary file
            subprocess.run(delete_temp_file_command, check=True)

            print(f"Downloaded {output_filename}")

        except Exception as e:
            print(f"Error downloading {output_filename}: {e}")
