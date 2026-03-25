from AI.client_ai import ask_ai

print("Mini Chat Bot AI (KETIK EXIT UNTUK KELUAR/STOP)")

while True:
    user_input = input("Promt : ")

    if user_input.lower() == "exit":
        print("Bot : Sampai jumpa lagi")
        break

    reply, limit, remaining, reset = ask_ai(user_input)
    print(f"Bot : {reply}")
    print(f"\nQuota\nLimit : {limit}\nSisa : {remaining}\nReset : {reset}\n\n")