# Python wrapper for Stanford OpenIE

The unofficial cross-platform Python wrapper for the <b>state-of-art</b> information extraction library from Stanford University.

## About Stanford IE

Open information extraction (open IE) refers to the extraction of structured relation triples from plain text, such that the schema for these relations does not need to be specified in advance. For example, Barack Obama was born in Hawaii would create a triple (Barack Obama; was born in; Hawaii), corresponding to the open domain relation "was born in". This software is a Java implementation of an open IE system as described in the paper:

Gabor Angeli, Melvin Johnson Premkumar, and Christopher D. Manning. Leveraging Linguistic Structure For Open Domain Information Extraction. In Proceedings of the Association of Computational Linguistics (ACL), 2015.
The system first splits each sentence into a set of entailed clauses. Each clause is then maximally shortened, producing a set of entailed shorter sentence fragments. These fragments are then segmented into OpenIE triples, and output by the system. 

More information can be found here : http://nlp.stanford.edu/software/openie.html

## Usage 

The code can be invoked either programmatically or through the command line. The program can be invoked with the following command. It will display ```['1.000: (Barack Obama; was; born)\n', '1.000: (Barack Obama; was born in; Hawaii)\n']```
```
git clone https://github.com/philipperemy/Stanford-OpenIE-Python.git
chmod +x init.sh
./init.sh # downloads necessary deps: stanford-openie.jar and stanford-openie-models.jar.
echo "Barack Obama was born in Hawaii." > samples.txt
python main.py -f samples.txt
```

## Support

You can either open an `Issue` or send me a e-mail to premy@reactive.co.jp. Any contributions are welcomed!

