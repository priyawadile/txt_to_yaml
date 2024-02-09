import yaml

def convert_text_to_yaml(input_file_path, output_file_path):
    questions = []
    current_question = None

    with open(input_file_path, 'r') as input_file:
        for line in input_file:
            line = line.strip()

            if line.startswith("question:"):
                if current_question:
                    questions.append(current_question)
                current_question = {"question": line.split(":", 1)[1].strip()}
            elif line.startswith("marks:"):
                current_question["marks"] = int(line.split(":", 1)[1].split(";")[0].strip())
            elif line.startswith("option:"):
                if "answers" not in current_question:
                    current_question["answers"] = []
                current_question["answers"].append(line.split(":", 1)[1].strip())
            elif line.startswith("correct:"):
                current_question["correct"] = line.split(":", 1)[1].strip()

    if current_question:
        questions.append(current_question)

    with open(output_file_path, 'w') as output_file:
        yaml.dump(questions, output_file, default_flow_style=False)


input_file_path = r'C:\Users\admin\Desktop\sample.txt'  
output_file_path = r'C:\Users\admin\Desktop\djpro\txtyaml\convertedyaml.yaml'
convert_text_to_yaml(input_file_path, output_file_path)
