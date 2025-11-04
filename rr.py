import subprocess
import argparse
import os
import sys

def get_changed_files(repo_path):
    """Проверка изменений в указанном Git-репозитории"""

    # Проверяем, существует ли указанный путь
    if not os.path.exists(repo_path):
        print(f"❌ Ошибка: путь '{repo_path}' не существует.")
        sys.exit(1)

    # Проверяем, является ли папка Git-репозиторием
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"❌ Ошибка: '{repo_path}' не является Git-репозиторием.")
        sys.exit(1)

    # Выполняем команду git status --short в указанном репозитории
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=repo_path,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("❌ Ошибка при выполнении команды Git.")
            print(result.stderr)
            sys.exit(1)

        output = result.stdout.strip()

        print(f"📁 Проверка репозитория: {os.path.abspath(repo_path)}\n")

        if not output:
            print("✅ Изменений нет. Репозиторий чист.")
        else:
            lines = output.split("\n")
            print("Изменённые файлы:")
            for line in lines:
                print(" ", line)
            print(f"\nВсего изменено: {len(lines)} файл(ов)")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт для проверки изменений в Git-репозитории."
    )
    parser.add_argument(
        "--path",
        default=".",
        help="Путь к репозиторию (по умолчанию — текущая папка)."
    )

    args = parser.parse_args()
    get_changed_files(args.path)