import numpy as np
import scipy.stats as ss
import subprocess, os

from exptools2.core import Session, PylinkEyetrackerSession
from stimuli import FixationLines
from trial import HCPMovieELTrial, DummyWaiterTrial, OutroTrial
from psychopy.visual import ImageStim, MovieStim3, Circle, Line
from psychopy import tools
import yaml
opj = os.path.join

def get_movie_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", str(filename)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


class HCPMovieELSession(PylinkEyetrackerSession):
    def __init__(self, output_str, output_dir, settings_file, eyetracker_on=True):
        """ Initializes StroopSession object. 
      
        Parameters
        ----------
        output_str : str
            Basename for all output-files (like logs), e.g., "sub-01_task-stroop_run-1"
        output_dir : str
            Path to desired output-directory (default: None, which results in $pwd/logs)
        settings_file : str
            Path to yaml-file with settings (default: None, which results in the package's
            default settings file (in data/default_settings.yml)
        """
        super().__init__(output_str, output_dir=output_dir, settings_file=settings_file, eyetracker_on=eyetracker_on)  # initialize parent class!
        

        self.mri_trigger = self.settings['scanner']['mri_trigger']


        self.movie = os.path.join(os.path.abspath(os.getcwd()), 'movs', self.settings['stimuli']['movie_file'])
        self.movie_duration = get_movie_length(self.movie)

        print(f'movie duration for this run: {self.movie_duration}')

        self.movie_stim = MovieStim3(self.win, filename=self.movie, size=self.settings['stimuli']['movie_size_pix'], pos=[0,-100])

        self.fixation_disk = Circle(
            self.win, 
            units='deg', 
            radius=0.05,
            lineWidth = 3, 
            fillColor=[1,1,1], 
            lineColor=[-1,-1,-1],
            pos=[0,-tools.monitorunittools.pix2deg(100, self.monitor)])
        
        # movie_ext_pix_x = (-self.settings['stimuli']['movie_size_pix'][0]/2,self.settings['stimuli']['movie_size_pix'][0]/2)
        # movie_ext_pix_y = (-self.settings['stimuli']['movie_size_pix'][1]/2-100,self.settings['stimuli']['movie_size_pix'][1]/2-100)
       

        # self.line_1 = Line(self.win, start=(movie_ext_pix_x[0], movie_ext_pix_y[0]), units='pix',
        #                   end=(movie_ext_pix_x[1], movie_ext_pix_y[1]), lineColor=[-1,-1,-1], lineWidth=1)
        # self.line_2 = Line(self.win, start=(movie_ext_pix_x[0], movie_ext_pix_y[1]), units='pix',
        #                   end=(movie_ext_pix_x[1], movie_ext_pix_y[0]), lineColor=[-1,-1,-1], lineWidth=1)

        self.create_trials()

    def create_trials(self):
        """ Creates trials (ideally before running your session!) """

        dummy_trial = DummyWaiterTrial(session=self, 
                                            trial_nr=0, 
                                            phase_durations=[np.inf],
                                            txt="Waiting for scanner; please remain still and maintain fixation.")

        outro_trial = OutroTrial(session=self, 
                                            trial_nr=3, 
                                            phase_durations=[self.settings['design']['end_duration']]
                                            )#txt='Scan still in progress; please remain still and maintain fixation.'
        
        intro_trial = OutroTrial(session=self, 
                                            trial_nr=1, 
                                            phase_durations=[self.settings['design']['start_duration']])

        movie_trial = HCPMovieELTrial(self, 
                                        trial_nr=2, 
                                        phase_durations=[self.movie_duration], 
                                        phase_names=['movie'],
                                        parameters={'movie_duration':self.movie_duration, 'movie_file': self.movie})

        self.trials = [dummy_trial, intro_trial, movie_trial, outro_trial]



    def run(self):

        if self.eyetracker_on:
            self.calibrate_eyetracker()

            self.start_recording_eyetracker()

        self.start_experiment()
        
        self.win.color = [-1,-1,-1]

        for trial in self.trials:
            trial.run()

        self.quit()


    def quit(self):

        # write to disk
        settings_out = opj(self.output_dir, self.output_str + '_expsettings.yml')
        with open(settings_out, 'w') as f_out:
            yaml.dump(self.settings, f_out, indent=4, default_flow_style=False)
            
        super().quit()