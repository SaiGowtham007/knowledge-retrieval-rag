import openpyxl


def load_evaluation_questions(file_path: str):
    workbook = openpyxl.load_workbook(
        file_path,
        data_only=True
    )

    worksheet = workbook["Questions"]

    questions = []

    for row in worksheet.iter_rows(
        min_row=2,
        values_only=True
    ):
        question_id = row[0]

        if not question_id:
            continue

        questions.append({
            "id": row[0],
            "category": row[1],
            "type": row[2],
            "difficulty": row[3],
            "question": row[4],
            "expected_answer": row[5],
            "required_documents": row[6],
            "trap": row[7]
        })

    return questions