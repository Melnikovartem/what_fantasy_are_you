extends Node

@onready var question = $CanvasLayer/HBoxContainer/Question
@onready var answers = $CanvasLayer/VBoxContainer.get_children().map(func(button): return button.get_child(0)) as Array[Label]


func _ready():
	print(answers)
	for answer in answers:
		answer.get_parent().connect("pressed", Callable(self, "_on_answer_question_pressed").bind(answer))
	update_state(questions.next_question(""))

func _on_answer_question_pressed(answer):
	update_state(questions.next_question(answer.text))

func update_state(question_info):
	question.text = question_info[0]
	if not len(question_info[1]):
		question_info[1].append("New game")
		
	for i in range(len(answers)):
		var text := ""
		if len(question_info[1]) > i:
			text = question_info[1][i]
		answers[i].text = text
		answers[i].get_parent().visible = text != ""

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
