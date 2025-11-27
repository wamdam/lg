A simple log which logs to your $HOME.

Usage:

Adding an entry (will be saved to ~/log)::

  # lg "My category: Done something"
  # lg "Breakfast **"

Note: "**" makes this a slacking entry.

Showing what has been logged::

  # lg
  ==============================================================================
  2025-11-27
  ==============================================================================
  
  08:06:50 (+00:00): Moin
  09:17:04 (+01:10): Done something
  10:11:13 (+00:54): Project 1: Projektmeeting
  10:20:25 (+00:09): Project 1: Serverperformance
  10:27:33 (+00:07): Project 2: Review Merges
  10:37:34 (+00:10): Staring at horizon**
            ------
  Project 1: 01:03
  Project 2: 00:07
     _other: 01:10
            ------
       work: 02:20
   slacking: 00:10

Installation:

# python3 -mvenv env
# env/bin/pip install -r requirements.txt
# cd ~/bin
# ln -s …path_to_lg/lg

  
