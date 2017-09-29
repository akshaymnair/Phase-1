System Requirements

•	Python 2
•	Pip
•	Pandas

Installation and Execution Instructions

Install Pip:
Download get-pip.py.
Run python get-pip.py

Install Pandas:
	Run pip install pandas

Task 1 

Run the python file print_actor_vector.py with actor_id and model as arguments.
		python print_actor_vector.py actor_id model
Running the file creates output_actor file which contains the tag vector for the given actor and model.

Task 2

Run the python file print_genre_vector.py with genre and model as arguments.
		python print_genre_vector.py genre model
Running the file creates output_genre file which contains the tag vector for the given actor and model.
Task 3

Run the python file print_user_vector.py with user_id and model as arguments.
		python print_user_vector.py user_id model
Running the file creates output_user file which contains the tag vector for the given actor and model.

Task 4

Run the python file differentiate_genre.py with actor_id and model as arguments.
		python differentiate_genre.py genre1 genre2 model
Running the file creates output_differentiate file which contains the tag vector for the given actor and model.
Sample output:
Actor id is: 1917810
Model is: tfidf
['brilliant', 1.0958229345381654]
['talking animals', 0.6183004819433]
['prostitution', 0.6021815039402841]
['child abuse', 0.562670125618651]
['disney animated feature', 0.5550901725201548]
['teenagers', 0.5506283315741418]
['dramatic', 0.538537323502579]
['funny', 0.5363518785340825]
['disney', 0.5211651612848374]
['heist', 0.4987266130364422]
['fun movie', 0.49741796670487726]

