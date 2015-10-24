# neat-deap
a little variation of neat-GP
</br></br>
Hi everyone! </br>
This is the code to implement neat-GP on python-deap, to install it you have to clone the repository.
The previous software that you'll need are: </br>
-Python 2.7  https://www.python.org/downloads/</br>
-Deap 1.0.2 or 1.1.0 http://deap.gel.ulaval.ca/doc/dev/installation.html</br>
-numpy http://www.numpy.org/ </br>
</br>
</br>
Once that you've download it, you have to modify a little bit the next three files:</br>
<b>-algorithms.py (deap)</b>: you have to modify the function eaSimple, the code that you have to put is in the file alg.py and import the modules.</br>
<b>-init.py (deap)</b>: you have to modify the function initRepeat, the code is in the file init_conf.py </br>
<b>-gp.py (deap)</b>: you have to import the modules and add the attributes on the init function. On the PrimitiveTree Class just add the parameter neat.<br><br>
And that's all. <br>
If you have a problem please contact me: pjuarez@tree-lab.org <br>
Regards!
