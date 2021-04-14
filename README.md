# Hangman-game-with-Threading
## Uses TCP connection to establish a connection and RSA Encryption to keep list of words hidden.
---
## In order to run this program you'll need the following:
- Python version 3.+ installed 
- Install PyCrpyto Library from https://pycryptodome.readthedocs.io/en/latest/src/installation.html
### (I personally, installed using ' pip install pycryptodomex ', which means I'm using 'Cryptodome' to import modules

To play the game run **runGame.py** file

ServerTCPONLY.py<br/>
      1. Server receives a command ‘-r’ to pick a word randomly or a custom string to be used<br/>
      throughout the program<br/>
      2. It creates a TCP socket and listens connections from clients<br/>
      3. Reads from a encryptedWords.txt and creates a list of words called ‘words’(One can modify it by<br/> 
      not doing this step if the custom string is provided)<br/>
      4. Server receives <char> and checks it against characters in the word. If the character in the list, it replaces all instances of that char in<br/>
      the dasher version and sends it back including (len(word)+1) - count[count is incremented previously].<br/>
      5. Client can exit guessing loop by entering clicking the 'quit' button. If a client runs out of guesses he/she<br/>
      loses.<br/>
      6. Client can also guess an entire word by entering guess <string> and the game for<br/>
      guessing this word will finish if the guessed word is right or wrong<br/>
      <br/>
ClientTCPONLY.py<br/>
      1. Creates a TCP socket and connects<br/>
      2. It has two loops to interact with the server first loop to start or exit(in which it receives<br/>
      instructions) and the second loop for playing the game by guessing letters of a word that<br/>
      is provided.<br/>
      3. In the game you can enter <char> -> to guess a letter, <string> ->  <br/>
      to guess an entire word, or click the 'quit' button -> to end this game<br/>
