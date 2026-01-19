from src.db.db import SessionLocal
from src.services.chat_service import create_session, send_message

# 2. Відкриваємо сесію БД
db = SessionLocal()

# 3. Створюємо чат
chat = create_session(db)
print("Session created:", chat.id)

# 4. Надсилаємо повідомлення
chat = send_message(db, chat.id, "Привіт! Хто ти?")
print("Total tokens:", chat.total_tokens)
print("Total cost:", chat.total_cost)

# 5. Друкуємо історію
for msg in chat.messages:
    print(msg.role, "->", msg.content)

db.close()
