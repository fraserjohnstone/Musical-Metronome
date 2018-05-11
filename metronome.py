"""

"""
import os
import numpy as np
import time
import pyaudio
import pprint
import threading


SAMPLE_RATE = 44100
NUM_TICK_SAMPLES = 1400

HIGH_TICK_FREQ = 4000
MID_TICK_FREQ = 3500
LOW_TICK_FREQ = 3200


def get_sin_samples(freq, num_samples, volume):
    """
    Generates the byte array which can be written to our audio stream to produce the metronome tick.
    
    :param freq: Float. The pitch of our sin wave. In Hz.
    :param num_samples: integer. the number of samples of sound we need.
    :param volume: float between 0.0 and 1.0
    
    :return: byte array.
    """
    return (volume*(np.sin(2*np.pi*np.arange(num_samples)*freq/SAMPLE_RATE))).astype(np.float32).tobytes()   
    
    
def get_silence_samples(num_samples):
    """
    Generates the byte array which can be written to our audio stream to produce silence.
    
    :param num_samples: integer. the number of samples of silence we need.
    
    :return: byte array.
    """
    return np.zeros(num_samples).astype(np.float32).tobytes()
    
    
def get_num_silence_samples(bpm, beat_type):
    """
    This function works out how many samples of silence are required in between each tick. As each type of 
    note can be expressed as a fraction of one semibreve, we will work out how many samples are required
    for a semibreve and then work from there.
    
    :param bpm: integer. Beats per minute.
    :param beat_type. float <= 1.0.
    
    :return: integer. the number of silence samples we need inbetween each metronome tick.
    """
    semibreve = 60/bpm*4   
    
    # get number fo samples in each beat and use this to get the number of samples needed for the silence
    beat_samples = int((semibreve*beat_type)*SAMPLE_RATE)
    return beat_samples-NUM_TICK_SAMPLES


def get_user_bpm():
    """
    prompts the user to enter the beats per minute value.
    
    :return bpm: integer that the user has selected as the beats per minute
    """
    os.system('cls')
    print('--- Beats Per Minute ---')
    print()
    
    bpm = 120
    while True:
        bpm = input('Enter the speed of the metronome in beats per minute: ')
        
        if bpm.isdigit() and int(bpm) > 0:
            break
    
    return int(bpm)
    
    
def get_user_beats_per_bar():
    """
    prompts the user to enter the number of beats in a bar.
    
    :return beats_in_bar: integer that the user has selected as the beats_in_bar
    """
    os.system('cls')
    print('--- Beats Per Bar ---')
    print()
    
    beats_in_bar = 4
    while True:
        beats_in_bar = input('Enter the number of beats in each bar: ')
        
        if beats_in_bar.isdigit() and int(beats_in_bar) > 0:
            break
    
    return int(beats_in_bar)
    
    
def get_users_grouping_choice(groupings, beats_in_bar):
    """
    :param grouoings: list of lists. All of the possible of beat groupings available to the user.
    :param beats_in_bar: integer. the number of beats in the bar.
    
    :return list: the list of integers detailing the grouping the user has chosen_grouping
    """
    # get the groupings in a dictionary
    i = 2
    groupings_dict = {1: [beats_in_bar]}
    
    for grouping in groupings:
        groupings_dict[i] = grouping
        i += 1
    
    # clear the screen and print out groupings
    os.system('cls')
    print('--- Groupings ---')
    print()
    
    for key, value in groupings_dict.items():
        if key == 1:
            print('    1)  No Grouping')
        else:
            print('    %s)  %s' % (str(key), ', '.join(str(b) for b in value)))
        
    print()
    
    # get the user input
    while True:
        user_choice = input('Please select a beat grouping from the list above: ')
        
        if user_choice.isdigit() and int(user_choice) in groupings_dict.keys():
            break
    
    return groupings_dict[int(user_choice)]
        
    
def get_possible_groupings(number_list, target_sum):
    """
    Given a number of beats in a bar, this method generates a list of all possible groupings
    of the numbers 2, 3, and 4 that sum to the number of beats in a a bar.
    
    :param number_list: list of integers. The groups of beats that are allowed.
    :param target_sum: integer. number of beats in a bar
    
    :return matching_numbers: list of groupings. eg. [[2, 2, 3], [2, 3, 2], [3, 2, 2] ... ]
    """
    matching_numbers = []

    def recursion(subset):
        for number in number_list:
            if sum(subset+[number]) < target_sum:
                recursion(subset+[number])
            elif sum(subset+[number]) == target_sum:
                matching_numbers.append(subset+[number])

    recursion([])
    return matching_numbers


def calculate_strong_beats(beats_in_bar, grouping):
    """
    Given a particular number of beats in a bar and grouping option, we need to calculate what
    beats are to be considered strong beats. for example in 7/4 time signature, with grouping of
    2,2,3 the strong beats are 1, 3, and 5.
    
    :param beats_in_bar: integer. The number of beats in a bar.
    :param grouping: list of integers. The beat grouping chosen by the user.
    """
    strong_beats = [1]
    for beat in grouping:
        strong_beat = strong_beats[-1] + (beat)
        if strong_beat < beats_in_bar:
            strong_beats.append(strong_beat)
    return strong_beats
    
    
def get_tick_samples():
    """
    For our metronome we need three tick samples, and different frequencies.
    
    :return tick_samples: dictionary of the form:
       
                 {'low_tick': low tick samples,
                  'mid_tick': mid tick samples,
                  'high_tick': high tick samples}
    """
    tick_samples = {
        'low_tick': get_sin_samples(LOW_TICK_FREQ, NUM_TICK_SAMPLES, 0.3),
        'mid_tick': get_sin_samples(MID_TICK_FREQ, NUM_TICK_SAMPLES, 0.4),
        'high_tick': get_sin_samples(HIGH_TICK_FREQ, NUM_TICK_SAMPLES, 1.0)
    }
    
    return tick_samples 
    
    
def run_metronome(stream, pa, tick_samples, silence, strong_beats, beats_in_bar):
    """    
    :param stream: PyAudio audio stream that we can write data to.
    :param pa: PyAudio Object
    :param tick_samples: Dictionary of the form 
    
                             {'low_tick': low tick samples,
                              'mid_tick': mid tick samples,
                              'high_tick': high tick samples}
    
    :param silence: The samples of silence to be written to the audio stream.
    :param strong_beats: list of ints. given the users choice of grouping, a list of strong beats is generated.
    :param beats_in_bar: integer. the number of beats in the bar
    """
    beat_of_bar = 1
    bar_number = 1
    
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        # set the tick frequency
        tick = tick_samples['low_tick']
        
        if beat_of_bar == 1:
            tick = tick_samples['high_tick']
        elif beat_of_bar in strong_beats:
            tick = tick_samples['mid_tick']
        
        #write the samples to the audio stream
        stream.write(tick)
        stream.write(silence)
        
        # update the beat of the bar
        if beat_of_bar < beats_in_bar:
            beat_of_bar += 1
        elif beat_of_bar == beats_in_bar:
            beat_of_bar = 1
            bar_number += 1
    
    # if we get to here then we must stop the metronome
    stream.stop_stream()
    stream.close()
    pa.terminate()

    
def main():
    beats_in_bar = get_user_beats_per_bar()
    beat_type = 1/4
    bpm = get_user_bpm()
    
    # get all possible combinations of groupings for this bar length
    poss_groupings = get_possible_groupings([2,3,4], beats_in_bar)
    
    # get the choice of grouping from the users
    chosen_grouping = get_users_grouping_choice(poss_groupings, beats_in_bar)
    
    # work out the strong beats_in_bar from the groupings
    strong_beats = calculate_strong_beats(beats_in_bar, chosen_grouping)
    
    # calculate the number of silence samples we need
    num_silence_samples = get_num_silence_samples(bpm, beat_type)
    
    pa = pyaudio.PyAudio()
    
    # open a stream to fill with audio
    stream = pa.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=SAMPLE_RATE,
                    output=True)
                    
    # get the samples
    tick_samples = get_tick_samples()
    silence_samples = get_silence_samples(num_silence_samples)
        
    # try to start the metronome thread
    
    try:
        t = threading.Thread(target=run_metronome, args=(stream, pa, tick_samples, silence_samples, strong_beats, beats_in_bar,))
        t.start()
        
        # wait for user input to stop        
        while True:
            os.system('cls')
            user_input = input('Metronome running --- Enter \'q\' to stop: ')
            
            if user_input == 'q':
                break
        
        # stop the thread that the metronome is running in and call main() once more
        t.do_run = False
        t.join()
        main()
    except:
        os.system('cls')
        print('Error: Couldn\'t start metronome thread')


if __name__ == '__main__':
    main()
