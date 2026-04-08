import asyncio
import json
import os
import sys
from openai import AsyncOpenAI
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts import CLASSIFIER_SYSTEM_PROMPT

load_dotenv()

async def run_evaluation():
    """Runs evaluation on a predefined dataset and reports accuracy."""
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    with open("tests/eval_dataset.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)
    
    results = []
    correct_count = 0
    
    print(f"Running evaluation on {len(dataset)} conversations...")
    print("-" * 50)
    
    for entry in dataset:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": CLASSIFIER_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Analyze the following conversation context:\n\n{entry['text']}"}
                ],
                response_format={"type": "json_object"}
            )
            
            payload = json.loads(response.choices[0].message.content)
            prediction = payload.get("classification")
            
            is_correct = (prediction == entry["ground_truth"])
            if is_correct:
                correct_count += 1
            
            results.append({
                "id": entry["id"],
                "text_preview": entry["text"][:50] + "...",
                "ground_truth": entry["ground_truth"],
                "prediction": prediction,
                "correct": is_correct
            })
            
            status = "OK" if is_correct else "ERR"
            print(f"[{status}] {entry['id']} | GT: {entry['ground_truth']} | Pred: {prediction}")
            
        except Exception as e:
            print(f"[ERROR] {entry['id']}: {e}")
    
    print("-" * 50)
    accuracy = (correct_count / len(dataset)) * 100
    print(f"OVERALL ACCURACY: {accuracy}% ({correct_count}/{len(dataset)})")

if __name__ == "__main__":
    asyncio.run(run_evaluation())
