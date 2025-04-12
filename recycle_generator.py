# recycle_generator.py
import csv
import openai

def load_top_posts(log_file="post_log.csv", top_n=3):
    posts = []
    with open(log_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                views = int(row.get("views", "0"))
                posts.append({
                    "title": row["title"],
                    "language": row["language"],
                    "category_id": row["category_id"],
                    "url": row["url"],
                    "views": views
                })
            except:
                continue
    posts.sort(key=lambda x: x["views"], reverse=True)
    return posts[:top_n]

def generate_related_article(title, category_id):
    prompt = f"""
    Based on the blog post titled "{title}", which is in the category ID {category_id},
    generate a new financial article on a similar topic. Focus on providing updated insights, professional tone, and investor-oriented analysis. Length: 1000+ words.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a financial content creator."},
            {"role": "user", "content": prompt.strip()}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()
