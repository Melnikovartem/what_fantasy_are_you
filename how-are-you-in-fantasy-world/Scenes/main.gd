extends Control

var q1 = "QUES_1"
var q2 = "QUES_2"

var question_info = ""
func next_question(prev_question, player_answer):
	return ["What do you like?", ["apple", "ice cream", "brocolli!","blood"]]
	

func update_state():
	question_info = next_question("", "")
	print(question_info[0])
	$MarginContainer/VBoxContainer/HBoxContainer/question.text = str(question_info[0])
	$AN1.text = str(question_info[1][0])
	$AN2.text = str(question_info[1][1])
	$AN3.text = str(question_info[1][2])
	$AN4.text = str(question_info[1][3])
# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
