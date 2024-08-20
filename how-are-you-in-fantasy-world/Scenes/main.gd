extends Node

@onready var question = $gameContent/HBoxContainer/Question
@onready var answers = $gameContent/VBoxContainer.get_children().map(func(button): return button.get_child(0)) as Array[Label]


func _ready():
	for answer in answers:
		answer.get_parent().connect("pressed", Callable(self, "_on_answer_question_pressed").bind(answer))
	update_state(questions.next_question(""))
	change_locale_button(TranslationServer.get_locale())

func _on_answer_question_pressed(answer):
	update_state(questions.next_question(answer.text))

func update_state(question_info):
	var text = question_info[0]
	var translated_text_len = len(tr(text))
	var font_size = 80
	if translated_text_len > 150:
		font_size = 60
	
	question.set("theme_override_font_sizes/font_size", font_size)
	question.text = text
	
	if not len(question_info[1]):
		question_info[1].append("Seek your people again")
		var dir = DirAccess.open("res://Assets/BackgroundsNew/")
		if dir:
			dir.list_dir_begin()
			var file_name = dir.get_next()
			while file_name != "":
				if file_name.substr(0, len(text) + 1) == text + "-" and file_name.substr(len(file_name)-4, len(file_name)) == ".png":
					%BG_main.texture = load("res://Assets/BackgroundsNew/"+file_name)
				file_name = dir.get_next()
			dir.list_dir_end()
		
	var shuffled_array = question_info[1].duplicate()
	shuffled_array.shuffle()
	 
	for i in range(len(answers)):
		text = ""
		if len(shuffled_array) > i:
			text = shuffled_array[i]
		answers[i].text = text
		
		font_size = 40
		translated_text_len = len(tr(text))
		if translated_text_len < 55:
			font_size = 60
		elif translated_text_len < 95:
			font_size = 50
			
		answers[i].set("theme_override_font_sizes/font_size", font_size)
		answers[i].get_parent().visible = text != ""

const max_width: float = 1242
const max_height: float = 2208

const max_width_wide: float = 3951

func _process(delta):
	var size = get_tree().root.size
	var width: float = size[0]
	var height: float = size[1]
	
	var ratio_change = (width / height) / (max_width/max_height)
	if ratio_change < 1:
		%BG_main.size = Vector2(max_width, max_height / ratio_change)
		%BG_main.position = Vector2(0, 0)
	else:
		var center = max_width * ratio_change / 2
		%BG_main.position = Vector2(center - max_width / 2, 0)
		%BG_main.size = Vector2(max_width, max_height)
		
		var new_max_width_wide = max_width_wide * max((width / height) / (max_width_wide / max_height), 1)
		print(new_max_width_wide)
		%BackgroundWide.size = Vector2(new_max_width_wide, max_height)
		%BackgroundWide.position = Vector2(center - new_max_width_wide / 2, 0)
	
	
func change_volume():
	if %MusicPlayer.playing:
		%VolumeButton.icon = preload("res://Assets/icons/volume_x.png")
		%MusicPlayer.stop()
	else:
		%VolumeButton.icon = preload("res://Assets/icons/volume_1.png")
		%MusicPlayer.play()
		
func change_lang():
	if TranslationServer.get_locale() == "ru":
		TranslationServer.set_locale("en")
	elif TranslationServer.get_locale() == "en":
		TranslationServer.set_locale("ru")
	change_locale_button(TranslationServer.get_locale())

func change_locale_button(locale):
	if locale == "en":
		%LangButton.icon = preload("res://Assets/icons/en_lang_icon.png")
	elif locale == "ru":
		%LangButton.icon = preload("res://Assets/icons/ru_lang_icon.png")
