# britbot.py
# a Discord bot written to aid Thoth in CSC 442-001 Challenge 02: Reverse Engineering
#
# Usage: First, obtain a Discord login token. Alter the TOKEN constant and then execute.
#
# This bot will wait until it sees a message containing a file with the PDF extension.
# It will download the file, run John the Ripper's pdf2john.pl on it to create a hash file,
# then run john on the hash file to (hopefully) arrive at the PDF's encryption password.
# It will then reply with the output of john in the same Discord channel as the original file.

import discord
import requests
from subprocess import call, check_output
import typing
import functools

PERL_PATH = "C:\\Users\\brendan\\AppData\\Local\\Strawberry\\perl\\bin\\perl.exe"
PDF2JOHN_PATH = "C:\\Users\\brendan\\Downloads\\john-1.9.0-jumbo-1-win64\\run\\pdf2john.pl"
JOHN_PATH = "C:\\Users\\brendan\\Downloads\\john-1.9.0-jumbo-1-win64\\run\\john.exe"

TOKEN = "token_here"

def download_file(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

def scan_pdf_john(filepath):
    hash_path = filepath + ".hash"
    temp_john_out = hash_path + ".john"

    call([PERL_PATH, PDF2JOHN_PATH, filepath, ">", hash_path], shell=True)
    print(f"Hash {filepath} > {hash_path}")

    call([JOHN_PATH, hash_path, ">", temp_john_out], shell=True)

    with open(temp_john_out) as f:
        john_out = f.read()

    return john_out


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs) # `run_in_executor` doesn't support kwargs, `functools.partial` does
    return await client.loop.run_in_executor(None, func)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        for attachment in message.attachments:
            if attachment.filename.lower().endswith(".pdf"):
                print("Found pdf: " + attachment.filename)
                download_file(attachment.url, attachment.filename)

                await message.channel.send("Downloaded PDF. Starting cracker...")

                try:
                    scan_result = await run_blocking(scan_pdf_john, attachment.filename)
                    await message.channel.send(f"{message.author.mention} found result:\n" + scan_result)
                except:
                    await message.channel.send("Failed to crack.")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)