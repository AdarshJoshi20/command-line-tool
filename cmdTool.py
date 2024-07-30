import requests
import json
import click

@click.command()
@click.option('--text', prompt='Enter the text to summarize (leave blank if providing a file path)', default='', help='Text to summarize')
@click.option('--file_path', prompt='Enter the file path (leave blank if providing text)', default='', help='Path to the file to summarize')
def summarize(text, file_path):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Content-Type": "application/json"
    }

    if text:
        # Split text into paragraphs if it contains multiple paragraphs
        paragraphs = text.split('\n\n')  # Assuming paragraphs are separated by two newlines

        # Join paragraphs with ' ' and create prompt
        prompt = ' '.join(paragraphs)

    elif file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                contents = file.read()
                # Split file contents into paragraphs if it contains multiple paragraphs
                paragraphs = contents.split('\n\n')  # Assuming paragraphs are separated by two newlines
                # Join paragraphs with ' ' and create prompt
                prompt = ' '.join(paragraphs)
        except FileNotFoundError:
            click.echo(f"File '{file_path}' not found. Please provide a valid file path.")
            return
        except OSError as e:
            click.echo(f"Error opening file '{file_path}': {e}")
            return
    else:
        click.echo("You must provide either text or a file path.")
        return

    data = {
        "model": "qwen2",
        "prompt": f"summarize the key points in 3-4 sentences {prompt}",  # Combine 'summarize' with the joined paragraphs
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        summary_json = response.json()
        summary_text = summary_json.get('response', 'No summary available')
        click.echo("Summary:")
        click.echo(summary_text)
    else:
        click.echo(f"Failed to summarize. Status code: {response.status_code}")

if __name__ == '__main__':
    summarize()
