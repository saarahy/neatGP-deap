# neat-deap
Implementation of neat-GP on DEAP framework. </br>
</br></br>
Hi everyone! </br>
This is the code to implement neat-GP on python-deap, to install it you have to clone the repository. 
The example to run it is the EnergyCooling file.</br>
The previous software that you'll need are: </br>
-Python 2.7  https://www.python.org/downloads/</br>
-Deap 1.0.2 or 1.1.0 http://deap.gel.ulaval.ca/doc/dev/installation.html</br>
-numpy http://www.numpy.org/ </br>

</br>
</br>
[Apr/2016]<b>New Status:</b><br>
There's a modification on crossover and mutation, previously we could make a crossover AND mutation to the same individual, however we modified the algorithm to do it like a standard GP, where the individual pass to the crossover OR mutation given a probability.
</br>
</br>
[Jun/2017]<b>New Update [Thanks to Aditya Rawal]:</b><br>
There's a modification on measure_tree.py file on the compare tree method. The method was not calculating the correct 'structure share' between two trees.
</br>
</br>
By the way, we made a new version of the algorithm where we integrate a local search method into neat-GP, you can found it in https://github.com/saarahy/NGP-LS (Article: http://dl.acm.org/citation.cfm?id=2931659).
</br>
</br>
<h1>Instructions</h1>
After the installation you only have to configure the parameters in the conf file (conf.yaml) and the run the MAIN_FILE.py.
If you want to add or remove the primitives set you have to modify the conf_primitives.py file, also in this file you can check if the number of arguments that you are going to need is in dictionary of the rename_arguments method.
</br>
</br>
And that's all. <br>
If you have a problem please contact me: juarez.s.perla[at]gmail.com <br>
Regards!
