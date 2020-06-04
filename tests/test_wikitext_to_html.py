import unittest
from lib import wikitext_to_html

class TestPreprocess(unittest.TestCase):

  def setUp(self):
    self.raw_text = """ = toronto raptors = 
 
 
 = = = Hurricane Isabel = = = 
 
 In the tropical Pacific Ocean, the hurricane entered the Gulf of Mexico. It made landfall at about 0830 UTC on October 8. It was the strongest hurricane to strike the Atlantic Coast since 1878. The storm moved west @-@ northwestward at 10 knots ( 30 km / h ; 21 mph ) at an altitude of 4 @,@ 000 ft ( 2 @,@ 000 m ; 5 @,@ 500 m ). As a result of the hurricane's path, the United States Geological Survey classified the storm as having tropical storm strength and hurricane radius, respectively. 
 
 = = = Tropical Depression = = = 
 
 In the Gulf of Mexico, the depression formed on October 10. The storm moved south @-@ southwest and entered its third hour of movement. It was named by U.S. President Franklin Delano Roosevelt as the Tropical Depression of the United States. 
 
 = = = Tropical Storm Brenda and Hurricane Ike = = = 
 
 On October 11, the storm moved west @-@ northwestward, entering its fourth hour of movement. The storm moved northwest and entered its sixth
"""

  def test_preprocess(self):
    results = wikitext_to_html.preprocess(self.raw_text)
    self.assertEqual(results, "=toronto raptors=\n\n\n===Hurricane Isabel===\n\nIn the tropical Pacific Ocean, the hurricane entered the Gulf of Mexico. It made landfall at about 0830 UTC on October 8. It was the strongest hurricane to strike the Atlantic Coast since 1878. The storm moved west @-@ northwestward at 10 knots ( 30 km / h ; 21 mph ) at an altitude of 4 @,@ 000 ft ( 2 @,@ 000 m ; 5 @,@ 500 m ). As a result of the hurricane's path, the United States Geological Survey classified the storm as having tropical storm strength and hurricane radius, respectively.\n\n===Tropical Depression===\n\nIn the Gulf of Mexico, the depression formed on October 10. The storm moved south @-@ southwest and entered its third hour of movement. It was named by U.S. President Franklin Delano Roosevelt as the Tropical Depression of the United States.\n\n===Tropical Storm Brenda and Hurricane Ike===\n\nOn October 11, the storm moved west @-@ northwestward, entering its fourth hour of movement. The storm moved northwest and entered its sixth")
