PiFM radio
==========

Turn your `Raspberry pi`_ into a small FM radio with `pifm`_! This daemon
listens on port 8000 for a audio stream and broadcast it through FM.

The audio stream must be a 16 bit mono 22050 Hz PCM.

It can be controlled on port 8080 to change emitting frequency, start or
stop the emission or gather information.


Install
-------

No install required, simply run the pifmradio.py script. Ensure pifm binary
is in the same folder as pifmradio.py (bundled with this code).

Currently the listening ports and address must be changed in the code, wait
for the next version :-)


Usage
-----

Start PiFMRadio on the server::

    python pifmradio.py

Control the radio with a client, the control.py script included with
PiFMRadio or the `pifm_client_controller`_ for android.



Control protocol
----------------

The control daemon uses json for communication. 

All commands return a *retval* string indicating if the operation succeeded
(*"OK"* or *"ERROR"*).

Currently implemented commands:

info
~~~~

Get current frequency and running status of the server.

This commands takes no argument. The response includes *status* boolean
indicating if server is emitting or not, and *freq* with the current
frequency as a string.

json message::

    {'command':'info'}

Sample response::

    {'retval':'OK', 'status':true, 'freq':'107.4'}

start
~~~~~

Start the emission.

This command takes no argument. *retval* *OK* when the emission starts, or
*ERROR* if the emission was already started.

json message::

    {'command':'start'}

Sample response::

    {'retval':'OK'}

stop
~~~~

Stops the emission.

This command takes no argument. *retval* *OK* when the emission stops, or
*ERROR* if the emission was already stopped.

json message::

    {'command':'stop'}

Sample response::

    {'retval':'OK'}


sintonize
~~~~~~~~~

Change the emitting frequency.

This command takes one argument, *freq* with the target frequency. *retval*
*OK* when the frequency is effectively changed or *ERROR* if there was any
trouble.

json message::

    {'command':'sintonize', 'freq':'90.5'}

Sample response::

    {'retval':'OK'}


exit
~~~~

Terminates current control session.

This command takes no argument. *retval* 'OK' always.

json message::

    {'command':'exit'}

Sample response::

    {'retval':'OK'}


quit
~~~~

Kill the emission and the control server.

This command takes no argument. *retval* 'OK' always.

json message::

    {'command':'exit'}

Sample response::

    {'retval':'OK'}


.. _pifm: http://www.icrobotics.co.uk/wiki/index.php/Turning_the_Raspberry_Pi_Into_an_FM_Transmitter
.. _Raspberry pi: http://www.raspberrypi.org/
.. _pifm_client_controller: https://github.com/interferencies/pifm_client_controller
