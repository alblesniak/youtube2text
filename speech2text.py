import os
import whisper
from tqdm import tqdm

# Load the large Whisper model
model = whisper.load_model("large")

# Specify the input directory containing the MP3 files
input_directory = "Gdy zstępuje Duch Święty - seria 2"
audio_directory = os.path.join(*[os.getcwd(), "audio", input_directory])

# Specify the output directory for the transcripts
transcripts_directory = os.path.join(os.getcwd(), "transcripts")
os.makedirs(transcripts_directory, exist_ok=True)

# Create a folder with the same name as the input directory inside the ./transcripts directory
output_directory = os.path.join(transcripts_directory, input_directory)
os.makedirs(output_directory, exist_ok=True)

# Function to transcribe a single MP3 file
def transcribe_file(file_path):
    result = model.transcribe(file_path, language="Polish")
    return result["text"]

# Function to save the transcript to a text file
def save_transcript(filename, transcript):
    output_file = os.path.join(output_directory, os.path.splitext(filename)[0] + ".txt")
    with open(output_file, "w") as f:
        f.write(transcript)

# Iterate through all MP3 files in the directory, transcribe them, and save the transcripts to text files
for filename in tqdm(os.listdir(audio_directory)):
    if filename.endswith(".mp3"):
        output_filename = os.path.splitext(filename)[0] + ".txt"
        output_filepath = os.path.join(output_directory, output_filename)

        if not os.path.exists(output_filepath):
            file_path = os.path.join(audio_directory, filename)
            transcript = transcribe_file(file_path)
            save_transcript(output_filename, transcript)
            print(f"Transcript for {filename} saved to {output_filename}")
        else:
            print(f"Transcript for {filename} already exists, skipping.")

