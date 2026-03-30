import asyncio
import sys
from threading import Thread
from telegram.ext import Application


class ConsoleHandler:
    """Обработчик консольных команд"""

    def __init__(self, app: Application):
        self.app = app
        self.running = True

    def start(self):
        """Запускает обработку консольных команд в отдельном потоке"""
        thread = Thread(target=self._console_loop, daemon=True)
        thread.start()

    def _console_loop(self):
        """Цикл обработки команд"""
        print("\n" + "=" * 50)
        print("Консоль управления ботом")
        print("Доступные команды:")
        print("  help   - показать справку")
        print("  stop   - остановить бота")
        print("  status - показать статус")
        print("  exit   - выйти")
        print("=" * 50 + "\n")

        while self.running:
            try:
                command = input(">>> ").strip().lower()

                if command == "help":
                    print("\nДоступные команды:")
                    print("  help   - показать справку")
                    print("  stop   - остановить бота")
                    print("  status - показать статус")
                    print("  exit   - выйти\n")

                elif command == "stop":
                    print("\n🛑 Останавливаю бота...")
                    asyncio.run_coroutine_threadsafe(
                        self._stop_bot(),
                        asyncio.get_event_loop()
                    )
                    self.running = False
                    break

                elif command == "status":
                    print("\n✅ Бот работает")
                    print(f"📊 Статус: активен\n")

                elif command == "exit":
                    print("\n👋 До свидания!")
                    self.running = False
                    break

                else:
                    if command:
                        print(f"\n❌ Неизвестная команда: {command}")
                        print("Введите 'help' для списка команд\n")

            except EOFError:
                break
            except KeyboardInterrupt:
                print("\n\n👋 До свидания!")
                break

    async def _stop_bot(self):
        """Останавливает бота"""
        try:
            await self.app.stop()
            print("✅ Бот успешно остановлен")
        except Exception as e:
            print(f"❌ Ошибка при остановке: {e}")