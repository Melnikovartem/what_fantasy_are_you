extends Control

var q1 = "QUES_1"
var q2 = "QUES_2"
var list = ["q1","q2","q3","q4"]

# Called when the node enters the scene tree for the first time.
func _ready():
	print(questions.next_question(""))

func skip():
	$Label.text = tr(q2)
	print(list[2])
	
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
