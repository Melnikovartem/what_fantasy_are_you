extends Node

var questions_data = []

func _ready():
	var file = FileAccess.open("res://Assets/questions_encoded", FileAccess.READ)
	questions_data = file.get_as_text().split("\n")
	file.close()

var current_question_id = 0
func next_question(answer_text):
	var current_question = JSON.parse_string(questions_data[current_question_id])
	current_question_id = current_question[1].get(answer_text, 0)
	
	current_question = JSON.parse_string(questions_data[current_question_id])
	var packed_return = [current_question[0], current_question[1].keys()]
	return packed_return
			
