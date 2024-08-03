extends Node

var questions_data = []

func _ready():
	var file = FileAccess.open("res://Assets/questions_encoded.json", FileAccess.READ)
	questions_data = JSON.parse_string(file.get_as_text())
	file.close()

var current_question_id = 0
func next_question(answer_text):
	current_question_id = questions_data[current_question_id][1].get(answer_text, 0)
	var current_question = questions_data[current_question_id]
	var packed_return = [current_question[0], current_question[1].keys()]
	return packed_return
			
