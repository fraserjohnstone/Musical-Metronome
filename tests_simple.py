"""
The majority of the features in this project have been manually tested. These unit tests are very limited.
"""

import unittest
import metronome


class TestMetronome(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_possible_groupings(self):
        """
        Given a number of beats in a bar, the function get_possible_groupings should produce a list of 
        possible combinations of the numbers 2, 3, and 4 that add up to the beats in a bar
        """
        # fixtures are simply bar numbers
        fixtures = [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] # 20 beats in a bar is ridiculous...
        beat_groupings = [2, 3, 4]

        for fixture in fixtures:
            # get the possible permutations
            perms = metronome.get_possible_groupings(beat_groupings, fixture)
            print('number permutations: %s' % len(perms))
            for perm in perms:
                self.assertEqual(sum(perm), fixture)
                for num in perm:
                    self.assertTrue(num in beat_groupings)
            
    def test_calculate_strong_beats(self):
        """
        Given a particular number of beats in a bar and grouping option, we need to be able to calculate what
        beats are to be considered strong beats.
        """
        # fixtures are simply bar numbers
        fixtures = [
            ([2,2,3], [1,3,5]),
            ([2,3,2], [1,3,6]),
            ([3,2,4], [1,4,6]),
            ([2,2,3,3], [1,3,5,8]),
            ([4,2,3,2], [1,5,7,10])
        ]

        for fixture in fixtures:
            self.assertEqual(metronome.calculate_strong_beats(sum(fixture[0]), fixture[0]), fixture[1])


if __name__ == '__main__':
    unittest.main()

