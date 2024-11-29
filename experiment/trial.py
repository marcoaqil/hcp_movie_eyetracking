import numpy as np
from exptools2.core import Trial
from psychopy.visual import TextStim
from psychopy import event

class HCPMovieELTrial(Trial):
    
    def __init__(self, session, trial_nr, phase_durations, phase_names,
                 parameters, timing='seconds', 
                 verbose=True):
        """ Initializes a StroopTrial object. 
        
        Parameters
        ----------
        session : exptools Session object
            A Session object (needed for metadata)
        trial_nr: int
            Trial nr of trial
        phase_durations : array-like
            List/tuple/array with phase durations
        phase_names : array-like
            List/tuple/array with names for phases (only for logging),
            optional (if None, all are named 'stim')
        parameters : dict
            Dict of parameters that needs to be added to the log of this trial
        timing : str
            The "units" of the phase durations. Default is 'seconds', where we
            assume the phase-durations are in seconds. The other option is
            'frames', where the phase-"duration" refers to the number of frames.
        verbose : bool
            Whether to print extra output (mostly timing info)
        """
        super().__init__(session, trial_nr, phase_durations, phase_names,
                         parameters, timing, load_next_during_phase=None, verbose=verbose)
    
    def create_trial(self):
        pass

    # def run(self):
    #     if self.parameters['condition'] == 'left':
    #         self.session.hemistim.stimulus_1.ori = 0
    #         self.session.hemistim.stimulus_2.ori = 0
    #     else:
    #         self.session.hemistim.stimulus_1.ori = 180
    #         self.session.hemistim.stimulus_2.ori = 180
    #     super().run()

    def draw(self):
        
        self.session.movie_stim.draw()

        #self.session.line_1.draw()
        #self.session.line_2.draw()
        #self.session.fixation_disk.draw() 

    def get_events(self):
        events = event.getKeys(timeStamped=self.session.clock)
        if events:
            if 'q' in [ev[0] for ev in events]:  # specific key in settings?

                self.session.quit() 




class DummyWaiterTrial(Trial):
    """ Simple trial with text (trial x) and fixation. """

    def __init__(self, session, trial_nr, phase_durations,
                 txt='', **kwargs):

        super().__init__(session, trial_nr, phase_durations, **kwargs)

        txt_height = self.session.settings['various']['text_height']
        txt_width = self.session.settings['various']['text_width']
        txt_y_pos = self.session.settings['various']['txt_y_pos']

        self.text = TextStim(self.session.win, txt,
                             pos=[0,txt_y_pos],
                             height=txt_height, wrapWidth=txt_width, **kwargs)
    
    def draw(self):
        self.text.draw()
        self.session.fixation_disk.draw()

    def get_events(self):
        events = event.getKeys(timeStamped=self.session.clock)
        if events:
            if 'q' in [ev[0] for ev in events]:  # specific key in settings?

                self.session.quit() 

            for key, t in events:
                if key == self.session.mri_trigger:
                    self.stop_phase()


class OutroTrial(Trial):
    """ Simple trial with only fixation cross.  """

    def __init__(self, session, trial_nr, phase_durations, txt='', **kwargs):

        super().__init__(session, trial_nr, phase_durations, **kwargs)

        txt_height = self.session.settings['various']['text_height']
        txt_width = self.session.settings['various']['text_width']
        txt_y_pos = self.session.settings['various']['txt_y_pos']

        self.text = TextStim(self.session.win, txt,
                             pos=[0,txt_y_pos],
                             height=txt_height, wrapWidth=txt_width, **kwargs)

    def draw(self):
        #self.text.draw()
        self.session.fixation_disk.draw()

    def get_events(self):
        events = event.getKeys(timeStamped=self.session.clock)
        if events:
            if 'q' in [ev[0] for ev in events]:  # specific key in settings?

                self.session.quit() 