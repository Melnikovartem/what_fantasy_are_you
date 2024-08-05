extends Node

@onready var question = $CanvasLayer/HBoxContainer/Question
@onready var answers = $CanvasLayer/VBoxContainer.get_children().map(func(button): return button.get_child(0)) as Array[Label]


func _ready():
	for answer in answers:
		answer.get_parent().connect("pressed", Callable(self, "_on_answer_question_pressed").bind(answer))
	update_state(questions.next_question(""))

func _on_answer_question_pressed(answer):
	update_state(questions.next_question(answer.text))

func update_state(question_info):
	var ch_name = question_info[0]
	question.text = ch_name
	if not len(question_info[1]):
		question_info[1].append("New game")
		var dir = DirAccess.open("res://Assets/Backgrounds/")
		if dir:
			dir.list_dir_begin()
			var file_name = dir.get_next()
			while file_name != "":
				if file_name.substr(0, len(ch_name)) == ch_name:
					break
				file_name = dir.get_next()
			dir.list_dir_end()
		
	for i in range(len(answers)):
		var text := ""
		if len(question_info[1]) > i:
			text = question_info[1][i]
		answers[i].text = text
		answers[i].get_parent().visible = text != ""

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	
func change_volume():
	if $VolumeButton.icon == preload("res://Assets/icons/volume-1 1.png"):
		$VolumeButton.icon = preload("res://Assets/icons/volume-x 1.png")
		$MusicPlayer.stop()
	else:
		$VolumeButton.icon = preload("res://Assets/icons/volume-1 1.png")
		$MusicPlayer.play()
		
func change_lang():
	if $LangButton.icon == preload("res://Assets/icons/ru_lang_icon.png"):
		$LangButton.icon = preload("res://Assets/icons/en_lang_icon.png")
		TranslationServer.set_locale("en")
	else:
		$LangButton.icon = preload("res://Assets/icons/ru_lang_icon.png")
		TranslationServer.set_locale("ru")
