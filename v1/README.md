## V1 (deprecated)

The unofficial cross-platform Python wrapper for the <b>state-of-art</b> information extraction library from Stanford University.

```
NOTE: Windows is not currently supported! Works on UNIX systems like Linux and Mac OS.
```

### Usage

First of all, make sure Java 1.8 is installed. Open a terminal and run this command to check:

```bash
java -version
```

If this is not the case and if your OS is Ubuntu, you can install it this way:

```bash
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```

The code can be invoked either programmatically or through the command line. The program can be invoked with the following command. It will display ```[['Barack Obama', ' was', ' born'], ['Barack Obama', ' was born in', ' Hawaii']]```
```bash
git clone https://github.com/philipperemy/Stanford-OpenIE-Python.git
cd Stanford-OpenIE-Python
echo "Barack Obama was born in Hawaii." > samples.txt
python main.py -f samples.txt
```

The output should be something like:

```
Barack Obama | was | born
Barack Obama | was born in | Hawaii
```

#### Troubleshooting

It's possible that you get an error like that one when using the lib for the first time:

```
AssertionError: ERROR: Call to stanford_ie exited with a non-zero code status
```

The error is related to the interaction with Java. To troubleshoot it, I would advise to run the python script with the `--verbose` argument. Search for line `executing command = <whatever command>` in the logs and copy paste this `<whatever command>` in your terminal to see the error.

#### Large Corpus

Sometimes you just want to run the information extraction tool on something larger than just a couple of sentences. I provide a bash script for that. This example runs the tool on the book: [The Iliad by Homer](http://www.gutenberg.org/ebooks/6130?msg=welcome_stranger), composed of 1.2M characters and 26K lines.

```bash
./process_large_corpus.sh corpus/pg6130.txt corpus/pg6130.txt.out
```

```
wc -l corpus/pg6130.txt.out
> 23888
```

### Generate Graph

```bash
echo "Barack Obama was born in Hawaii." > samples.txt
python main.py -f samples.txt -g
```
Will generate a [GraphViz DOT](http://www.graphviz.org/) graph and its related PNG file in `/tmp/openie/`

<div align="center">
  <img src="../img/out.png"><br><br>
</div>

Note: Make sure GraphViz is installed beforehand. Try to run the `dot` command to see if this is the case. If not, run `sudo apt-get install graphviz` if you're running on Ubuntu.
