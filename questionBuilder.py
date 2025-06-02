# This script reads MCQ questions from questions.txt and generates an interactive HTML quiz file.
# This version will:

# Accept questions starting with 1., 1), or just 1
# Accept options like A), A., A-, a) etc.
# Accept answers like ✅ Answer: B, Correct Answer: b, Answer: C, etc.
# Ignore section headers and blank lines


def parse_questions(raw_input):
    import re
    questions = []
    # Remove section headers and empty lines
    lines = [line for line in raw_input.split('\n') if line.strip() and not line.strip().startswith('🔹')]
    question_blocks = []
    block = []
    for line in lines:
        # Start of a new question (number followed by . or ) or just a number)
        if re.match(r'^\d+[\.\)]?\s', line.strip()):
            if block:
                question_blocks.append(block)
            block = [line]
        else:
            block.append(line)
    if block:
        question_blocks.append(block)

    for block in question_blocks:
        q_text = ""
        options = []
        answer = None
        for idx, line in enumerate(block):
            # Question line
            if idx == 0:
                q_match = re.match(r'^(\d+)[\.\)]?\s*(.*)', line.strip())
                if q_match:
                    q_num = q_match.group(1)
                    q_text = q_match.group(2)
                else:
                    q_num = str(len(questions) + 1)
                    q_text = line.strip()
            # Option line
            opt_match = re.match(r'^([A-Da-d])[\)\.\-]?\s*(.*)', line.strip())
            if opt_match:
                options.append((opt_match.group(1).upper(), opt_match.group(2)))
            # Answer line (various formats)
            ans_match = re.search(r'(?:✅\s*)?(?:Correct\s*)?Answer\s*[:\-]?\s*([A-Da-d])', line, re.IGNORECASE)
            if ans_match:
                answer = ans_match.group(1).upper()
        if options and answer:
            questions.append({
                'number': q_num,
                'text': q_text,
                'options': options,
                'answer': answer
            })
    return questions

def generate_html(questions, title="SQL MCQ Practice – All Questions"):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; background: #f8f9fa; color: #222; }}
    .container {{ max-width: 900px; margin: 2rem auto; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #0001; padding: 2rem; }}
    h1 {{ text-align: center; margin-bottom: 1.5rem; }}
    .question-block {{ margin-bottom: 2rem; padding: 1rem 1.5rem; border-left: 4px solid #0074d9; background: #f4f8fb; border-radius: 4px; }}
    .question-text {{ font-weight: 500; margin-bottom: 0.7rem; }}
    .options {{ margin-bottom: 0.5rem; }}
    .option {{ display: block; margin: 0.2rem 0; padding: 0.4rem 0.8rem; border-radius: 3px; cursor: pointer; border: 1px solid transparent; }}
    .option.selected {{ background: #eaf6ff; border-color: #0074d9; }}
    .feedback {{ margin-top: 0.5rem; font-weight: bold; }}
    .correct {{ color: #27ae60; }}
    .incorrect {{ color: #c0392b; }}
    @media (max-width: 600px) {{
      .container {{ padding: 0.7rem; }}
      .question-block {{ padding: 0.7rem; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>{title}</h1>
"""
    for q in questions:
        html += f"""    <div class="question-block" data-answer="{q['answer']}">
      <div class="question-text">{q['number']}. {q['text']}</div>
      <div class="options">
"""
        for opt in q['options']:
            html += f'        <span class="option" data-option="{opt[0]}">{opt[0]}) {opt[1]}</span>\n'
        html += """      </div>
      <div class="feedback"></div>
    </div>
"""
    html += """  </div>
  <script>
    document.querySelectorAll('.question-block').forEach(function(block) {
      const options = block.querySelectorAll('.option');
      const feedback = block.querySelector('.feedback');
      const correct = block.getAttribute('data-answer');
      options.forEach(function(option) {
        option.addEventListener('click', function() {
          options.forEach(opt => opt.classList.remove('selected'));
          option.classList.add('selected');
          if (option.getAttribute('data-option') === correct) {
            feedback.textContent = '✅ Correct!';
            feedback.className = 'feedback correct';
          } else {
            feedback.textContent = '❌ Incorrect. Try again!';
            feedback.className = 'feedback incorrect';
          }
        });
      });
    });
  </script>
</body>
</html>
"""
    return html

def main():
    # Read questions from questions.txt
    try:
        with open("questions.txt", "r", encoding="utf-8") as f:
            raw_input = f.read()
    except FileNotFoundError:
        print("questions.txt file not found.")
        return
    questions = parse_questions(raw_input)
    if not questions:
        print("No questions found. Please check your questions.txt format.")
        return
    filename = input("Enter the output HTML filename (e.g., quiz.html): ").strip()
    html = generate_html(questions)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Quiz HTML file '{filename}' generated successfully.")

if __name__ == "__main__":
    main()