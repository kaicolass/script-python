import os
import json
import sys
import requests
import google.generativeai as genai

class QuizByteAgent:
    def __init__(self, base_url, username, password, gemini_api_key):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.session = requests.Session()
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def login(self):
        url = f"{self.base_url}/api/auth/login"
        payload = {"login": self.username, "password": self.password}
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.status_code == 200

    def generate_and_create_question(self, quiz_id, topic, order_index):
        prompt = f"""
        Gere uma questão de múltipla escolha sobre Java com foco no tópico '{topic}'.
        A resposta deve ser estritamente um objeto JSON válido, sem markdown, seguindo exatamente este formato:
        {{
            "topic": "{topic}",
            "questionText": "Enunciado da pergunta aqui",
            "optionA": "Opção A",
            "optionB": "Opção B",
            "optionC": "Opção C",
            "optionD": "Opção D",
            "correctOption": "A, B, C ou D",
            "explanation": "Explicação detalhada da resposta",
            "orderIndex": {order_index},
            "quiz": {{ "id": {quiz_id} }}
        }}
        """
        response = self.model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        question_data = json.loads(response.text)
        url = f"{self.base_url}/api/quizzes"
        res = self.session.post(url, json=question_data)
        res.raise_for_status()
        return res.json()

    def submit_and_explain_attempt(self, slug, answers):
        url = f"{self.base_url}/api/quizzes/themes/{slug}/attempts"
        payload = {"answers": answers}
        res = self.session.post(url, json=payload)
        res.raise_for_status()
        attempt_result = res.json()
        
        prompt = f"""
        Com base no resultado da tentativa do quiz fornecido abaixo, atue como um instrutor Java e gere uma análise de desempenho curta em texto corrido focado nos erros do aluno:
        {json.dumps(attempt_result, ensure_ascii=False)}
        """
        ai_response = self.model.generate_content(prompt)
        return {
            "backend_response": attempt_result,
            "ai_analysis": ai_response.text
        }

if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    base_url = os.getenv("QUIZBYTE_BASE_URL")
    user = os.getenv("QUIZBYTE_USER")
    pwd = os.getenv("QUIZBYTE_PASSWORD")
    
    if not all([api_key, base_url, user, pwd]):
        sys.exit(1)
        
    agent = QuizByteAgent(base_url, user, pwd, api_key)
    if agent.login():
        action = os.getenv("AGENT_ACTION", "generate")
        if action == "generate":
            q_id = int(os.getenv("QUIZ_ID", "1"))
            topic_name = os.getenv("QUIZ_TOPIC", "fundamentos")
            idx = int(os.getenv("QUIZ_ORDER_INDEX", "1"))
            result = agent.generate_and_create_question(q_id, topic_name, idx)
            print(json.dumps(result, indent=2))
        elif action == "submit":
            theme_slug = os.getenv("QUIZ_SLUG", "fundamentos")
            raw_answers = os.getenv("QUIZ_ANSWERS", "[]")
            answers_list = json.loads(raw_answers)
            result = agent.submit_and_explain_attempt(theme_slug, answers_list)
            print(json.dumps(result, indent=2))